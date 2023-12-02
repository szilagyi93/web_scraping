import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait   # only for syncroniztios. Wait for N sec for done 
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from profession_wsc_class.ProfessionWebScraper  import ProfessionWebScraper
import numpy as np
def main():
    try:
        #Start indicator
        print('The code has stated!')
        #Open the given URL in the web browser
        url = r'https://www.profession.hu/'
        print('Sherching on: '+url)
        PWSC = ProfessionWebScraper(url=url,headless= False,browser_name='Chrome')
        
        #Accept cukies
        PWSC.conset_cookies()
        print('Cookies accepted!')
        
        #Search for given keyword
        job_keyword = r'python'
        print('Searching for: '+ job_keyword)
        PWSC.fill_out_sraching_are(keyword=job_keyword)
        PWSC.search_click()
        
        #Print the result of searching 
        print('The sreaching process has been ended:\n'+PWSC.driver.current_url)
        
        nOAJ = PWSC.found_jobs()
        print('The total number of found jobs: \n' + str(nOAJ)) 
        (jobs_on_page,nOPJ)=PWSC.job_cards()
        print('The number of found jobs per page: \n' + str(nOPJ))
        
        data = list
        for job in jobs_on_page:
            data.append((job.text).split('\n'))
        #Load jobcards into a pandas frame
        
        #load the pd[] to an SQL database
        
        #Scrape the     
    except Exception as e:
        print(f"An error occurred: {e}")
        
    finally:
        PWSC.driver.quit()
         
if __name__ == "__main__":
    main()













