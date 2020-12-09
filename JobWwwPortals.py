from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
from scraper_tools import JobsFileHandler


class WwwItJobPortal:
    def __init__(self, www_name: str):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.www_address = www_name

    def start_session_with_def_configuration(self, implicit_timeout=5):
        self.driver.get(self.www_address)
        self.driver.implicitly_wait(implicit_timeout)
        time.sleep(2)
        self.driver.maximize_window()


class NoFluffJobsPl(WwwItJobPortal):

    def __init__(self):
        super().__init__("https://nofluffjobs.com/pl")
        self.__file_session_repository = JobsFileHandler(NoFluffJobsPl.__name__)
        self.__subpages_webelements = []
        self.__job_links = []
        self.__scrapping_details = []

    def __pass_initial_cookies(self):
        cookie_xpath = "//nfj-cookie-information/div/div/button"
        self.driver.find_element_by_xpath(cookie_xpath).click()

    def __get_subpages_objects(self):
        paging_xpath = "//nfj-search-results/div/nfj-pagination/ul/li/a"
        num_of_pages = len(self.driver.find_elements_by_xpath(paging_xpath))
        for n in range(1, num_of_pages-1):
            n_page_xpath = paging_xpath + "[text()=' " + str(n) + " ']"
            self.__subpages_webelements.append(self.driver.find_element_by_xpath(n_page_xpath))

    def __choose_testing_category(self):
        category_element_xpath = "//nfj-filter-trigger[4]/div/button/span"
        self.driver.find_element_by_xpath(category_element_xpath).click()
        testing_xpath = "//nfj-filter-universal-section/section[1]/div/nfj-filter-control[5]/button"
        self.driver.find_element_by_xpath(testing_xpath).click()
        approve_xpath = "/html/body/ngb-popover-window/div[2]/nfj-filters-wrapper/div/div[3]/div[1]/button[2]"
        self.driver.find_element_by_xpath(approve_xpath).click()

    def __choose_python_technology(self):
        technology_xpath = "//nfj-filters/div/nfj-filter-trigger[1]/div/button"
        self.driver.find_element_by_xpath(technology_xpath).click()
        python_xpath = "//nfj-filter-universal-section/section[1]/div/nfj-filter-control[7]/button"
        self.driver.find_element_by_xpath(python_xpath).click()
        approve_xpath = "/html/body/ngb-popover-window/div[2]/nfj-filters-wrapper/div/div[3]/div[1]/button[2]"
        self.driver.find_element_by_xpath(approve_xpath).click()

    def __choose_selenium_technology(self):
        technology_xpath = "//nfj-filters/div/nfj-filter-trigger[1]/div/button"
        self.driver.find_element_by_xpath(technology_xpath).click()
        selenium_xpath = "//nfj-filter-universal-section/section[2]/div/nfj-filter-control[2]/button"
        self.driver.find_element_by_xpath(selenium_xpath).click()
        approve_xpath = "/html/body/ngb-popover-window/div[2]/nfj-filters-wrapper/div/div[3]/div[1]/button[2]"
        self.driver.find_element_by_xpath(approve_xpath).click()

    def __set_scrapping_details(self, *args):
        for arg in args:
            if arg == "python":
                self.__choose_python_technology()
                self.__scrapping_details.append(arg)
                time.sleep(2)
            if arg == "selenium":
                self.__choose_selenium_technology()
                self.__scrapping_details.append(arg)
                time.sleep(2)
            if arg == "testing":
                self.__choose_testing_category()
                self.__scrapping_details.append(arg)
                time.sleep(2)

    def __get_all_www_links(self):
        # get subpages first
        self.__get_subpages_objects()

        i = 1
        for subpage in self.__subpages_webelements:
            time.sleep(1)
            subpage.click()
            time.sleep(1)
            job_objects = self.driver.find_elements_by_xpath("//nfj-search-results/nfj-postings-list/a")
            for job_obj in job_objects:
                self.__job_links.append(job_obj.get_attribute("href"))

    def __get_technologies_from_single_www(self, link: str) -> list():
        pass

    def __save_technologies_from_single_www(self, technologies: list()):
        pass

    def __store_all_scraped_data_in_filedb(self):
        self.__file_session_repository.initiate_filedb()
        for job_advertisement in self.__job_links:
            pass

    def start_session_with_def_configuration(self, implicit_timeout=5):
        self.driver.get(self.www_address)
        self.driver.implicitly_wait(implicit_timeout)
        self.driver.maximize_window()
        self.__pass_initial_cookies()

    def run_data_scraper(self):
        time.sleep(1)
        scrapping_args = ["testing", "python", "selenium"]
        self.__set_scrapping_details(*scrapping_args)
        time.sleep(2)
        self.__get_all_www_links()
        for link in self.__job_links:
            print(link)


if __name__ == "__main__":
    pass
