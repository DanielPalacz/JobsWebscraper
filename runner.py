from JobWwwPortals import NoFluffJobsPl
import time


if __name__ == "__main__":
    jobscraper_nofluff1 = NoFluffJobsPl()
    jobscraper_nofluff1.start_session_with_def_configuration()
    time.sleep(1)
    jobscraper_nofluff1.run_data_scraper()
