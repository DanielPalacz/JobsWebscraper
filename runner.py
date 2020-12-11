from JobWwwPortals import NoFluffJobsPl
import time
from scraper_tools import TechDomainAnalyzer


if __name__ == "__main__":
    technologies_analyzer = TechDomainAnalyzer()
    if technologies_analyzer.get_job_source() == "f":
        print("Scrapping techonologies related data based on 'https://nofluffjobs.com/pl'")
        print("We will get data based on following filters: ", ",".join(technologies_analyzer.get_tech_filters()))
        jobscraper_nofluff1 = NoFluffJobsPl()
        jobscraper_nofluff1.start_session_with_def_configuration()
        time.sleep(1)
        jobscraper_nofluff1.run_data_scraper(technologies_analyzer.get_tech_filters())
        technologies_analyzer.generate_tech_popularity_report()

    else:
        print("Sorry, this technologies-scrapper is not implemented.")
