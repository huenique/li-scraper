import io
import os
import pkgutil
import time
from typing import Optional

import pandas as pd
import requests
from msedge.selenium_tools import Edge, EdgeOptions
from selenium.webdriver.firefox.options import Options

from src.scraper import Scrape
from src.session import SignIn


class Settings:
    """Defines the prerequisites and starts the scraping process.
    
    The arguments represent the default values for each instance variable.

    Setting the user's LinkedIn credentials directly from the class variables 
    is allowed, they're also accessible via an external module, or use 
    the os module to access them from your system environment variables.

    Args:
        df_dir(str): Directory of the original file containing the dataframe.
        df_read(str): Relative path of the original dataframe file.
        df_file_name(str): Name for the dataframe output file.
        cookies_path(str): Path where your LinkedIn session cookies are stored.
        driver_path(str): Webdriver's path.

    Attributes:
        email(str): User's LinkedIn email or phone number.
        password(str): User's LinkedIn password.
        self.read_file(str): Existing file containing pandas readable dataframe.
    """
    email: Optional[str] = None
    password: Optional[str] = None
    read_file: Optional[str] = None
    driver_path: Optional[str] = None

    def __init__(self,
                 df_dir='src/data',
                 df_path='data/dataframe.csv',
                 df_file_name='new_dataframe.csv',
                 cookies_path='src/cookies/cookies.pkl',
                 driver_path='',
                 _driver=None,
                 _check=False):
        self.df_dir = df_dir
        self.df_path = df_path if self.read_file is None else f'data/{self.read_file}'
        self.df_file_name = df_file_name
        self.cookies_path = cookies_path
        self.driver_path = driver_path
        self.driver = _driver
        self.check = _check

        if self.driver is None:
            # Selenium capabilities and other settings
            options = Options()

            # Options for microsoft edge (chromium)
            edge_options = EdgeOptions()
            edge_options.use_chromium = True
            edge_options.add_argument('log-level=3')
            edge_options.add_argument('lang=en')
            edge_options.add_argument('--start-maximized')

            # Main webdriver
            self.driver = Edge(executable_path=self.driver_path,
                               options=edge_options)

        self._check_connection()

    def _check_connection(self, tries=0, max_try=10, err=None):
        """Make initial network stability check.
        """
        while not self.check:
            if tries == max_try:
                break
            try:
                requests.get('https://www.google.com/')
                self.driver.get('https://www.google.com/')
                while 'Google' not in self.driver.title:
                    time.sleep(0.1)
                self.check = True
            except Exception as e:
                err = e
                tries += 1

        if not self.check:
            print(f'({__name__}) Tries: {max_try}', err)
            self.driver.close()
        else:
            self.scraper_logic_handler()

    def csv_to_df(self, row):
        """Convert bytes in memory buffer (i.e. csv file data) to a pandas dataframe.
        """
        output = pd.read_csv(io.BytesIO(row))
        return output

    def edit_dataframe(self, row, df, scraped_info):
        """Edit the active dataframe with the scraped information.
        """
        headers = [
            'URL', 'title', 'role', 'current company', 'location', 'website',
            'twitter', 'email', 'industry', 'company url', 'company size',
            'specialties'
        ]
        for header, info in zip(headers, scraped_info):
            info_index = scraped_info.index(info)
            if info_index == 4 and any(map(str.isdigit, str(info))):
                scraped_info[info_index] = 'None'
            df.at[row, header] = str(scraped_info[info_index])
        return df

    def define_search(self, row, df, site='site:linkedin.com', search=[]):
        """Take a row from the dataframe and convert it to a search value.
        """
        search.clear()
        search = df.iloc[row]
        name = search[:].values[0]
        search = (f'\t{search[:].values[1]}\t{search[:].values[2]}').split()
        search.insert(0, name)
        search.insert(len(search) - 1 + 1, site + f' intitle:{name}')
        return search

    def select_pandas_io(self, df_file):
        """Determine the df_file extention for which pandas I/O to use.
        """
        pandas_io_dict = {'.csv': self.csv_to_df}
        _, ext = os.path.splitext(df_file)
        row = pkgutil.get_data('src', df_file)
        df = pandas_io_dict[ext](row)
        return df

    def repack_to_csv(self, df):
        """Write the dataframe to a file.
        """
        try:
            new_df_path = os.path.join(self.df_dir, self.df_file_name)
            _ = df.to_csv(new_df_path, index=False)
            return True
        except Exception as e:
            print(e)
        return False

    def scraper_logic_handler(self):
        """Main handler for the entire scraping process.
        """
        username = self.email
        password = self.password
        cookies = self.cookies_path
        driver = self.driver
        ready = self.check
        scraped_info = None

        if ready:
            print('''\nGeneral tip: 
                Do not minimize the webdriver while it is running.
                This will allow some elements to properly load.''')
            df = self.select_pandas_io(self.df_path)

            session = SignIn.sign_in(driver, username, password, cookies)
            while session is None:
                time.sleep(0.1)

            for row in df.index:
                if df.at[row, 'URL'] == 'None':
                    search = self.define_search(row, df)
                    scraped_info = Scrape(driver, search).startstop()
                    df = self.edit_dataframe(row, df, scraped_info)
                else:
                    pass

            if self.repack_to_csv(df):
                driver.close()

    @classmethod
    def start_scraper(cls,
                      user_email=None,
                      user_password=None,
                      read_file='',
                      driver_path=''):
        if isinstance(user_email,
                      str) and isinstance(user_password, str) and isinstance(
                          read_file, str) and isinstance(driver_path, str):
            cls.email = user_email
            cls.password = user_password
            cls.read_file = read_file
            cls.driver_path = driver_path
            row = cls()
            return row
        else:
            print(
                f'({__name__}) Invalid DataType: {user_email, type(user_email)}, {user_password, type(user_password)}, {read_file, type(read_file)}, {driver_path, type(driver_path)}'
            )


if __name__ == '__main__':
    _ = Settings()
