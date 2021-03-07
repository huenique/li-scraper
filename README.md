# Li Scraper

A LinkedIn scraper written to scrape specific parts of a user's profile and organization.

### Logic Sequence
  - Takes the name, surname, company from a pandas dataframe row (.csv file) and
  - Finds the LinkedIn profile with these three fields (Google search for public profiles).
  - From the profile, we take: URL, Title, Current Role, Current Company, Company Location.
  - Take contact information; Website, Twitter, Email.
  - From the company the person is currently under: Industry, Organization URL, Company size and Specialties.
  - Finally, we add the scraped information to the dataframe columns.

## Setup
From the package's root directory, run:
```sh
pip install -e .
```

## Usage
```python
from src.settings import Settings

email = 'myemail@email.com'
password = 'mypassword'
file = 'dataframe.csv'
driver_path = r'C:\Program Files\webdrivers\msedgedriver.exe'
scraper = Settings.start_scraper(email, password, file, driver_path)
```
