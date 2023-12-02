from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait   # only for syncroniztios. Wait for N sec for done 
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from jobCard.JobCard import JobCard

class ProfessionWebScraper: 
    def __init__(self, url='https://www.profession.hu/',headless=True,browser_name ='Chrome'):
        self.url = url
        self.driver = self.initialize_webdriver(url,headless, browser_name)
        
    def initialize_webdriver(self, url, headless, browser_name):
        """
        Initializes a Chrome WebDriver instance with specified settings.

        Parameters:
            self (object): The instance of the class.
            url (str): The URL to open after initializing the WebDriver.
            headless (bool): Flag indicating whether to run the browser in headless mode.
            browser_name (str): The name of the browser.

        Returns:
            webdriver.Chrome: The initialized Chrome WebDriver instance.
        """
        
        chrome_options = Options()
        
        # Settings for headless mode
        if headless:
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--headless=new')
            chrome_options.headless = True
        else:
            chrome_options.add_experimental_option("detach", True)
        
        chrome_options.add_argument('--ignore-certificate-errors') 
        
        # Open Chrome Webbrowser
        if browser_name == 'Chrome':
            driver = webdriver.Chrome(options=chrome_options)
            driver.get(url)
            return driver
        else: 
            raise ValueError('Only for Chrome yet!')
    
    def conset_cookies(self,by_type=By.ID,type_value = "elfogad"):
        """
        Handles cookie consent.

        Parameters:
            self (object): The instance of the class.
            by_type (selenium.webdriver.common.by): The type of locator strategy (e.g., By.ID, By.CLASS_NAME).
            type_value (str): The value of the locator.

        Returns:
            webdriver.Chrome: The Chrome WebDriver instance.
        """
        conset_button = self.driver.find_element(by=by_type,value = type_value)
        conset_button.click()
        self.driver.refresh()
    
    def fill_out_sraching_are(self,keyword_id = 'header_keyword',keyword = 'python'):
        """
        Fills out the search input field with the specified keyword.

        Parameters:
            driver (webdriver.Chrome): The Chrome WebDriver instance.
            keyword_id (str): The ID of the search input field. Default is 'header_keyword'.
            keyword (str): The value to be entered into the search input field. Default is 'python'.

        Returns:
            webdriver.Chrome: The Chrome WebDriver instance after filling out the search input field.
        """
        keyword_area = self.driver.find_element(by=By.ID,value = keyword_id)
        keyword_area.send_keys(keyword)
    
    def search_click(self, search_button_id = 'search-bar-search-button'):
        """
        Clicks the search button on the webpage.

        Parameters:
            driver (webdriver.Chrome): The Chrome WebDriver instance.
            button_id (str): The ID attribute value of the search button.

        Returns:
            webdriver.Chrome: The Chrome WebDriver instance.
        """
        search_button = self.driver.find_element(by= By.ID, value= search_button_id)
        search_button.click()
        
    def found_jobs(self, id = "jobs_block_count"):
        """
        Parameters:
            driver (webdriver.Chrome): The Chrome WebDriver instance.
            id (str): The ID attribute value of the HTML element containing the number of found jobs.
                Default is 'jobs_block_count'.

        Returns:
            int: The number of found jobs if successfully extracted, or -1 if the element is not found or the count cannot be determined.
        """
        import re # for using regex 
        number_of_jobs = self.find_element_by_id_with_wait(id)
        
        if number_of_jobs:
            match = re.search( r'\d+\w', number_of_jobs.text)
            return int(match.group()[::])
        return -1
    
    def find_element_by_id_with_wait(self, element_id, timeout=10):
        """
        Waits for the presence of an HTML element with a specified ID on a webpage using explicit wait.

        This function utilizes Selenium's WebDriverWait to wait for the specified amount of time (timeout)
        until an HTML element with the given ID is present on the webpage. If the element is found within
        the timeout period, the function returns the WebElement; otherwise, it prints an error message
        and returns None.

        Parameters:
            self (object): The instance of the class.
            element_id (str): The ID attribute value of the HTML element to be located.
            timeout (int): The maximum time to wait for the element to be present, in seconds. Default is 10 seconds.

        Returns:
            WebElement or None: The located HTML element if found within the specified timeout, or None if the element is not found.
        """
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((By.ID, element_id))
            )
            return element
        except TimeoutException:
            print(f"Element with ID '{element_id}' not found within {timeout} seconds.")
            return None

    def find_element_by_class_with_wait(self, class_name, timeout=10):
        """
        Waits for the presence of HTML elements with a specified class name on a webpage using explicit wait.

        This function utilizes Selenium's WebDriverWait to wait for the specified amount of time (timeout)
        until HTML elements with the given class name are present on the webpage. If the elements are found within
        the timeout period, the function returns the list of WebElements; otherwise, it prints an error message
        and returns None.

        Parameters:
            self (object): The instance of the class.
            class_name (str): The class name of the HTML elements to be located.
            timeout (int): The maximum time to wait for the elements to be present, in seconds. Default is 10 seconds.

        Returns:
            List[WebElement] or None: The list of located HTML elements if found within the specified timeout,
            or None if the elements are not found.
        """
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME,class_name))
            )
            return element
        except TimeoutException:
            print(f"Element with CLASS_NAME: '{class_name}' not found within {timeout} seconds.")
            return None

    def get_hyperlink(self,job):
        # Assuming 'driver' is your WebDriver instance
        # You need to locate the element using its CSS selector or XPath
        job_card_element = job.find_element(By.CSS_SELECTOR, 'h2.job-card__title a')

        # Now, get the 'href' attribute value
        href_value = job_card_element.get_attribute('href')
        
        if not href_value:
            return None
        else:
            return href_value
    
    def job_cards(self,class_name='card-body',timeout=10):
        """
        Finds job cards on a webpage using the specified class name and explicit wait.

        This function uses the find_element_by_class_with_wait method to locate job cards on a webpage
        based on the specified class name. If job cards are found within the specified timeout, the function
        returns a tuple containing the list of job cards and the count of job cards. If no job cards are found,
        it returns -1.

        Parameters:
            self (object): The instance of the class.
            class_name (str): The class name of the HTML elements representing job cards. Default is 'card-body'.
            timeout (int): The maximum time to wait for the elements to be present, in seconds. Default is 10 seconds.

        Returns:
            Tuple[List[WebElement], int] or int: If job cards are found, returns a tuple containing the list of job cards
            and the count of job cards. If no job cards are found, returns -1.
        """
        list_of_job_cards = self.find_element_by_class_with_wait(class_name, timeout)
        if len(list_of_job_cards) <= 0: 
            return -1
        else:
            jobCards = list([])
            for job in list_of_job_cards:  
                hyperlink = self.get_hyperlink(job)
                job = job.text.split('\n')
                job_name = job[0]
                company_name = job[1]
                location = job[2] #later could be useful
                job_description = job[3]
                jobCards.append(JobCard(company=company_name,job_name= job_name,job_description =job_description,job_hyperlink= hyperlink))
        return jobCards, len(jobCards)