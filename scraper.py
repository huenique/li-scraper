from src.settings import Settings

email = 'myemail@email.com'
password = 'mypassword'
file = 'dataframe.csv'
driver_path = r'C:\Program Files\webdrivers\msedgedriver.exe'
scraper = Settings.start_scraper(email, password, file, driver_path)
