import random
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from src.objects import Basic, Company, Contact


class Scrape:
    def __init__(self,
                 driver=None,
                 search_val=[],
                 success=False,
                 basic=[],
                 contact=[],
                 company=[],
                 section=[],
                 scraped=[],
                 google_url='https://www.google.com/'):
        self.driver = driver
        self.search_val = search_val
        self.success = success
        self.basic = basic
        self.contact = contact
        self.company = company
        self.section = section
        self.scraped = scraped
        self.google_url = google_url

    def add_basic(self, basic):
        for item in basic:
            self.basic.append(item)

    def add_contact(self, contact):
        for item in contact:
            self.contact.append(item)

    def add_company(self, company):
        for item in company:
            self.company.append(item)

    def add_section(self, section):
        self.section.append(section)

    def random_wait(self):
        timer = random.randrange(15, 30)
        time.sleep(timer)
        return True

    def reset(self):
        key_vars = [self.basic, self.contact, self.company]
        _ = [var.clear() for var in key_vars]
        return True

    def startstop(self):
        _ = self.get_info()
        scraped_info = self.basic + self.contact + self.company
        _ = self.reset()
        return scraped_info

    def get_info(self, timeout=10, max_try=0, page_err=None, wait=random_wait):
        while not self.success:
            if max_try == 10:
                print(f'({__name__}) Tries: {max_try}', page_err)
                _ = input(
                    'Please open your browser and resolve the problem, then press enter...'
                )
                max_try = 0

            try:
                elem = WebDriverWait(self.driver, timeout).until(
                    EC.element_to_be_clickable((By.NAME, 'q')))

                if elem and wait(self):
                    elem.clear()
                    elem.send_keys(' '.join(self.search_val))
                    elem.send_keys(Keys.ENTER)
                    _ = WebDriverWait(self.driver, timeout).until(
                        EC.element_to_be_clickable((By.CLASS_NAME, 'g')))

                if wait(self):
                    google_resutls = self.driver.find_elements_by_class_name(
                        'g')
                    google_resutls[0].find_element_by_tag_name('a').click()

                _ = WebDriverWait(self.driver, timeout).until(
                    EC.presence_of_element_located(
                        (By.ID, 'profile-nav-item')))
                self.success = True
            except Exception as e:
                max_try += 1
                page_err = str(e)
                if wait(self):
                    self.driver.get(self.google_url)

        if self.success:
            # Get basic information
            url = self.driver.current_url
            co_name_position = None
            try:
                title = WebDriverWait(self.driver, timeout).until(
                    EC.presence_of_element_located((
                        By.XPATH,
                        '/html/body/div[7]/div[3]/div/div/div/div/div[2]/main/div[1]/section/div[2]/div[2]/div[1]/h2'
                    )))
                title = title.text.strip()
            except:
                title = None

            self.driver.execute_script(
                'window.scrollTo(0, Math.ceil(document.body.scrollHeight/2));')

            try:
                _ = WebDriverWait(self.driver, timeout).until(
                    EC.presence_of_element_located(
                        (By.ID, 'experience-section')))
                exp = self.driver.find_element_by_id('experience-section')
            except:
                exp = None

            if exp is not None:
                pv_position = exp.find_elements_by_class_name(
                    'pv-position-entity')
                role = None
                try:
                    ul_tag = pv_position[0].find_element_by_tag_name('ul')
                    role = ul_tag.find_elements_by_tag_name(
                        'span')[2].text.strip()
                    roles_case = True
                except:
                    roles_case = False

                if roles_case:
                    try:
                        company_names = pv_position[
                            0].find_element_by_tag_name('h3')
                        co_name_position = company_names.find_elements_by_tag_name(
                            'span')[1]
                        company_name = co_name_position.text.strip()
                    except:
                        company_name = None
                    try:
                        company_locs = pv_position[
                            0].find_elements_by_tag_name('h4')[3]
                        company_loc = company_locs.find_elements_by_tag_name(
                            'span')[1].text.strip()
                    except:
                        company_loc = None
                else:
                    try:
                        role = pv_position[0].find_element_by_tag_name(
                            'h3').text.strip()
                    except:
                        role = None
                    try:
                        co_name_position = pv_position[
                            0].find_elements_by_tag_name('p')[1]
                        company_name = co_name_position.text.strip()
                    except:
                        company_name = None
                    try:
                        company_loc = pv_position[0].find_elements_by_tag_name(
                            'h4')[2].find_elements_by_tag_name(
                                'span')[1].text.strip()
                    except:
                        company_loc = None

                section = Basic(
                    url=url,
                    title=title,
                    role=role,
                    company_name=company_name,
                    company_loc=company_loc,
                )

                basic = [url, title, role, company_name, company_loc]
                self.add_section(section)
                self.add_basic(basic)

            self.driver.execute_script('window.scrollTo(0, 0);')

            # Get contact information
            try:
                _ = WebDriverWait(self.driver, timeout).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'mr5')))
                top_card = self.driver.find_elements_by_class_name('mr5')[0]
            except:
                top_card = None

            if top_card is not None:
                try:
                    _ = WebDriverWait(self.driver, timeout).until(
                        EC.presence_of_element_located((
                            By.XPATH,
                            '/html/body/div[7]/div[3]/div/div/div/div/div[2]/main/div[1]/section/div[2]/div[2]/div[1]/ul[2]/li[3]/a/span'
                        )))
                    contact_info = top_card.find_element_by_xpath(
                        '/html/body/div[7]/div[3]/div/div/div/div/div[2]/main/div[1]/section/div[2]/div[2]/div[1]/ul[2]/li[3]/a/span'
                    )
                    self.driver.execute_script('arguments[0].click();',
                                               contact_info)

                except:
                    contact_info = top_card.find_element_by_xpath(
                        '/html/body/div[8]/div[3]/div/div/div/div/div[2]/main/div[1]/section/div[2]/div[2]/div[1]/ul[2]/li[3]/a/span'
                    )
                    self.driver.execute_script('arguments[0].click();',
                                               contact_info)

                try:
                    _ = WebDriverWait(self.driver, timeout).until(
                        EC.presence_of_element_located(
                            (By.CLASS_NAME, 'artdeco-modal-overlay')))
                    modal_view = self.driver.find_element_by_class_name(
                        'artdeco-modal-overlay')
                except:
                    modal_view = None

                if modal_view is not None:
                    try:
                        website_section = self.driver.find_element_by_class_name(
                            'ci-websites')
                        hrefs = website_section.find_elements_by_tag_name('a')
                        website = [
                            href.get_attribute('href') for href in hrefs
                        ]
                    except:
                        website = None
                    try:
                        email_section = self.driver.find_element_by_class_name(
                            'ci-email')
                        hrefs = email_section.find_elements_by_tag_name('a')
                        email = [href.text for href in hrefs]
                    except:
                        email = None

                    try:
                        twitter_section = self.driver.find_element_by_class_name(
                            'ci-twitter')
                        a_tag = twitter_section.find_element_by_tag_name('a')
                        twitter = a_tag.get_attribute('href')
                    except:
                        twitter = None

                    close_button = self.driver.find_element_by_xpath(
                        '/html/body/div[4]/div/div/button/li-icon').click()

                    section = Contact(website=website,
                                      email=email,
                                      twitter=twitter)

                    contact = [(website), twitter, email]
                    self.add_section(section)
                    self.add_contact(contact)

            # Get company information
            org_url = None
            try:
                _ = WebDriverWait(self.driver, timeout).until(
                    EC.presence_of_element_located(
                        (By.ID, 'experience-section')))
                co_name_position.click()
            except:
                pass

            try:
                _ = WebDriverWait(self.driver, timeout).until(
                    EC.presence_of_element_located(
                        (By.CLASS_NAME, 'org-page-navigation')))
                org_page = self.driver.find_element_by_class_name(
                    'org-page-navigation')
            except:
                org_page = None

            if org_page is not None:
                org_url = self.driver.current_url
                _ = self.driver.get(org_url + '/about/')

            try:
                _ = WebDriverWait(self.driver, timeout).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'mb6')))
                about_page = self.driver.find_element_by_class_name('mb6')
            except:
                about_page = None

            if about_page is not None:
                industry = None
                company_size = None
                specialties = None

                overview = about_page.find_element_by_tag_name('dl')
                detail_terms = overview.find_elements_by_tag_name('dt')
                detail_texts = overview.find_elements_by_tag_name('dd')

                for term, text in zip(detail_terms, detail_texts):
                    term_index = detail_terms.index(term)
                    if term.text == 'Industry':
                        industry = text.text.strip()
                    if term.text == 'Company size':
                        company_size = text.text.strip()
                    if term.text == 'Specialties':
                        specialties = detail_texts[term_index + 1].text.strip()

                section = Company(org_url=org_url,
                                  industry=industry,
                                  company_size=company_size,
                                  specialties=specialties)
                company = [industry, org_url, company_size, specialties]
                self.add_section(section)
                self.add_company(company)

        self.driver.get(self.google_url)
        return None
