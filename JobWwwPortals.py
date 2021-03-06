"""JobWwwwPortals module

The given module implements Scrapping for Job Portals:
--- NoFluffJobsPl: https://nofluffjobs.com/pl/
"""

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

from scraper_tools import JobsFileHandler

import time
import logging


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
        self.__file_session_repository = JobsFileHandler(NoFluffJobsPl.__name__ + "_")
        self.__subpages_webelements = []
        self.__job_links = []
        self.__scrapping_details = []
        self.logger = logging.getLogger()

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
        approve_xpath = "//nfj-filters-wrapper/div/div[3]/div[1]/button[2][text()=' Zatwierdź ']"
        self.driver.find_element_by_xpath(approve_xpath).click()

    def __choose_python_technology(self):
        technology_xpath = "//nfj-filters/div/nfj-filter-trigger[1]/div/button"
        self.driver.find_element_by_xpath(technology_xpath).click()
        python_xpath = "//nfj-filter-universal-section/section[1]/div/nfj-filter-control[7]/button"
        self.driver.find_element_by_xpath(python_xpath).click()
        approve_xpath = "//nfj-filters-wrapper/div/div[3]/div[1]/button[2][text()=' Zatwierdź ']"
        self.driver.find_element_by_xpath(approve_xpath).click()

    def __choose_selenium_technology(self):
        technology_xpath = "//nfj-filters/div/nfj-filter-trigger[1]/div/button"
        self.driver.find_element_by_xpath(technology_xpath).click()
        selenium_xpath = "//nfj-filter-universal-section/section[2]/div/nfj-filter-control[2]/button"
        self.driver.find_element_by_xpath(selenium_xpath).click()
        approve_xpath = "//nfj-filters-wrapper/div/div[3]/div[1]/button[2][text()=' Zatwierdź ']"
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
        for index, subpage in enumerate(self.__subpages_webelements):
            if index != 0:
                time.sleep(2)
                subpage.click()
            time.sleep(1)
            job_objects = self.driver.find_elements_by_xpath("//nfj-search-results/nfj-postings-list/a")
            for job_obj in job_objects:
                self.__job_links.append(job_obj.get_attribute("href"))

    def __store_technologies_from_single_www(self, link: str):
        job_adv_technologies = [link]
        time.sleep(2)
        self.driver.get(link)
        time.sleep(2)
        skills_list = \
            self.driver.find_elements_by_xpath("//nfj-posting-requirements/common-posting-item-tag/button")
        skills_list += self.driver.find_elements_by_xpath("//nfj-posting-requirements/common-posting-item-tag/object/a")
        for competency in skills_list:
            job_adv_technologies.append(competency.text.replace(",", ""))
        self.__file_session_repository.update_filedb(",".join(job_adv_technologies))

    def __scrap_and_store_all_data_in_filedb(self):
        for job_advertisement in self.__job_links:
            self.__store_technologies_from_single_www(job_advertisement)

    def start_session_with_def_configuration(self, implicit_timeout=5):
        self.logger.info("Starting session with def configuration. Opening: " + self.www_address)
        self.driver.get(self.www_address)
        self.driver.implicitly_wait(implicit_timeout)
        time.sleep(2)
        self.driver.maximize_window()
        self.__pass_initial_cookies()

    def run_data_scraper(self, scrapping_args):
        self.logger.info("Running F-Data scraper with the following filters: " + str(scrapping_args))
        time.sleep(1)
        self.__set_scrapping_details(*scrapping_args)
        time.sleep(2)
        self.logger.info("Collecting www links for all matching job advertisements.")
        self.__get_all_www_links()
        self.logger.info("In total was collected " + str(len(self.__job_links)) + " job links.")

        self.logger.info("Saving all Jobs related data into filedb.")
        self.__file_session_repository.initiate_filedb(*self.__scrapping_details)
        self.__scrap_and_store_all_data_in_filedb()
        self.driver.quit()


if __name__ == "__main__":
    pass
