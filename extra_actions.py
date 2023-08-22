import os
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from linkedin_scraper import Person 


Linkedin_URL = "https://www.linkedin.com/"
Linkedin_PEAOPLE_SEARCH_URL = Linkedin_URL+"search/results/people/"


def search(driver, search_text, max=10):

    # search_container = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.search-global-typeahead')))
    # if 'focused' not in search_container.get_attribute('class'):
    #     WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.search-global-typeahead button'))).click()
    # WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#global-nav-typeahead input'))).send_keys(search_text)
        
    # search_results = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.search-global-typeahead-hit__text')))
    # if 'focused' not in search_results.get_attribute('class'):
    #     WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.search-global-typeahead-hit__text'))).click()

    # return search_results
    pages = max//10
    profiles = []
    for page in range(1, pages+1):
        driver.get(f"{Linkedin_PEAOPLE_SEARCH_URL}?keywords={search_text}&origin=SWITCH_SEARCH_VERTICAL&page={page}")
        src = driver.page_source
        # Now using beautiful soup
        soup = BeautifulSoup(src, 'lxml')
        profils = soup.find_all('span', {'class': 'entity-result__title-text'})
        for p in profils:
            ref = p.find('a').get('href')
            #print(ref)
            if ref != 'https://www.linkedin.com/search/results/people/headless?origin=SWITCH_SEARCH_VERTICAL&keywords=ceo%20retail%20company':
                profiles.append(ref)
        #print(profils)
    return profiles


def get_mail(profil, driver):
    my_network_emails = []
    url = os.path.join(profil, "overlay/contact-info/")
    driver.get(url)
    src = driver.page_source
    contact_page = BeautifulSoup(src, 'lxml')
    content_contact_page = contact_page.find('section', {'class': 'ci-email'})
    mail = content_contact_page.find('a').get('href').removeprefix('mailto:') if content_contact_page else ""
    # for contact in content_contact_page:
    #     print("[+]", contact.get('href')[7:])
        #my_network_emails.append(contact.get('href')[7:])
    print(mail)
    return mail



class PersonContact(Person):

    __WAIT_FOR_ELEMENT_TIMEOUT = 50
    
    def __init__(self, linkedin_url=None, name=None, about=None, experiences=None, educations=None, interests=None, accomplishments=None, company=None, job_title=None, contacts=None, driver=None, get=True, scrape=True, close_on_complete=True, time_to_wait_after_login=0):
        super().__init__(linkedin_url, name, about, experiences, educations, interests, accomplishments, company, job_title, contacts, driver, get, scrape, close_on_complete, time_to_wait_after_login)
        self.email = get_mail(self.linkedin_url, self.driver)
        self.open_to_work = None

    def to_dict(self):
        return {
            "name":self.name,
            "location":self.location,
            "about":self.about,
            "email":self.email,
            "linkedin_url":self.linkedin_url,
            "open": self.open_to_work,
            #"experiences":self.experiences,
            "educations":self.educations,
            #"interests":self.interests,
            #"accomplishments":self.accomplishments,
            #""conn"=self.contacts,
            
        }
