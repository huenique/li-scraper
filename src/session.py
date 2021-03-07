import pickle

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class SignIn():
    """Session handler for the scraping process.

    Attributes:
        driver (obj): The passed Selenium driver.
        session_key (str): User's LinkedIn email or username.
        session_pass (str): User's LinkedIn password.
        cookies_path (str): Relative path of the pickle file.
    """
    driver = None
    session_key = None
    session_pass = None
    cookies_path = None
    _singed_in = False
    _linkedin_iurl = 'https://www.linkedin.com/login'

    def __init__(self):
        try:
            # Load cookies if available
            cookies = pickle.load(open(self.cookies_path, 'rb'))
            self.driver.get(self._linkedin_iurl)
            for cookie in cookies:
                self.driver.add_cookie(cookie)
            self.driver.refresh()
            self._singed_in = True
        except:
            self.process_login(self.driver)
        self._return_status()

    def _return_status(self):
        return self.driver

    def save_cookies(self, driver):
        cookies = driver.get_cookies()
        pickle.dump(cookies, open(self.cookies_path, 'wb'))

    def process_login(self,
                      driver,
                      timeout=10,
                      tries=0,
                      max_try=10,
                      page_err=None):
        while not self._singed_in:
            if tries == max_try:
                print(f'({__name__}) Tries: {max_try}', page_err)
                _ = input(
                    'Please open your browser and resolve the problem, then press enter...'
                )
                tries = 0

            try:
                driver.get(self._linkedin_iurl)
                if 'Login' not in driver.title:
                    self._singed_in = True
                _ = WebDriverWait(self.driver, timeout).until(
                    EC.presence_of_element_located((By.ID, 'username')))

                username = self.driver.find_element_by_id('username')
                password = self.driver.find_element_by_id('password')
                if username and password:
                    username.clear()
                    username.send_keys(self.session_key)
                    password.clear()
                    password.send_keys(self.session_pass)
                driver.find_element_by_xpath(
                    '/html/body/div/main/div[2]/form/div[3]/button').click()

                _ = WebDriverWait(driver, timeout).until(
                    EC.presence_of_element_located(
                        (By.ID, 'profile-nav-item')))
                self.save_cookies(driver)
                self._singed_in = True
            except Exception as e:
                tries += 1
                page_err = f'({__name__}) Error: {str(e)}'

    @classmethod
    def sign_in(cls, driver, session_key, session_pass, cookies_path):
        cls.driver = driver
        cls.session_key = session_key
        cls.session_pass = session_pass
        cls.cookies_path = cookies_path
        result = cls()
        return result
