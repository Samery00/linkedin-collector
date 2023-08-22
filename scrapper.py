import csv
import datetime
import time
from linkedin_scraper import actions
from selenium import webdriver
import extra_actions
from extra_actions import PersonContact
from webdriver_manager.chrome import ChromeDriverManager


class ScrapTest :


    def __init__(self) -> None:
        print("START")
        super().__init__()
        print("START1")
        #service = webdriver.ChromeService()
        print("START2")
        self.driver = webdriver.Chrome(service=webdriver.ChromeService(ChromeDriverManager().install()))
        print("START3")
        
    def setLogin(self, email, password):

        actions.login(self.driver, email, password)

    def search(self, search_keywords, max=100):

        return extra_actions.search(self.driver, search_keywords, max=max)

    def scrap_data(self, profiles=[]):
        results = []
        header = ["Name", "Location", "About", "Email", "Linkedin_url", "Open to work", "Experiences", "Educations"]
        filename = '100_ceo_retail_industry.csv'
        path = f'{filename}'
        with open(path, 'w') as file:
            writer = csv.DictWriter(file, fieldnames=header)
            writer.writeheader()
            
            for profil in profiles:
                time.sleep(5)

                data = PersonContact(profil, driver=self.driver, close_on_complete=False)
                plain_data = {
                    "Name":data.name,
                    "Location":data.location,
                    "About":data.about,
                    "Email":data.email,
                    "Linkedin_url":data.linkedin_url,
                    "Open to work": data.open_to_work,
                    "Experiences":data.experiences,
                    "Educations":data.educations,
                    #"interests":self.interests,
                    #"accomplishments":self.accomplishments,
                    #""conn"=self.contacts,
                }
                results.append(plain_data)
                print(f"name : {data.name}")
                writer.writerow(plain_data)
        # print(f"location : {data.location}")
        # print(f"About : {data.about}")
        # print(f"Open : {data.is_open_to_work}")
        # print(f"Open : {data.email}")
        #mail_data = extra_actions.get_mail(profil, self.driver)
            #results.append(data)
        #print(results)
        return results

    def to_csv(self, extracted_data):
        header = ["Name", "Location", "About", "Email", "linkedin_url", "Open to work", "educations"]
        filename = '100_ceo_retail_industry_copy.csv'
        path = f'{filename}'
        with open(path, 'w') as file:
            writer = csv.DictWriter(file, fieldnames=header)
            writer.writeheader()
            writer.writerows(extracted_data)
    
    def test(self):
        return self.driver.get("http://www.python.org")


#person = Person("https://www.linkedin.com/in/joey-sham-aa2a50122", driver=driver)

def main():

    test = ScrapTest()
    #print(test.test())
    print("HI")
    test.setLogin("your-email", "your-password")
    print("HI")
    search_results = test.search("ceo retail company", max=130)
    print("HI")
    print(search_results)
    scraped_data = test.scrap_data(search_results)
    print(f" scaped {scraped_data}")

    test.to_csv(scraped_data)
    




main()
