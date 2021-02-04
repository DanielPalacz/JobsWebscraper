from JobWwwPortals import NoFluffJobsPl
from scraper_tools import TechDomainAnalyzer

import db

from datetime import date
from datetime import datetime
import time
import logging


if __name__ == "__main__":
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    # define file logname:
    filelogname = "LogSession_" + str(date.today().strftime("%Y%m%d"))
    filelogname += "_" + str(datetime.now().hour) + str(datetime.now().minute) + ".log"

    # create file handler which logs even debug messages
    fh = logging.FileHandler(filelogname)
    fh.setLevel(logging.DEBUG)

    # create formatter and add it to the handler
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    # add the handlers to the logger
    logger.addHandler(fh)

    logger.info("Creating TechDomainAnalyzer object for: f-scrapper with 'python,selenium' filters.")
    technologies_analyzer = TechDomainAnalyzer("f", "python,selenium")

    if technologies_analyzer.get_job_source() == "f":
        logger.info("Creating NoFluffJobsPl object (f-scrapper object).")
        jobscraper_nofluff1 = NoFluffJobsPl()
        jobscraper_nofluff1.start_session_with_def_configuration()
        time.sleep(1)
        jobscraper_nofluff1.run_data_scraper(technologies_analyzer.get_tech_filters())

        popularity_report_name = technologies_analyzer.generate_tech_popularity_report()
        logger.info("Popularity report was just generated: " + popularity_report_name + ".")

        db.initialize_db()
        db.update_db(popularity_report_name)
        logger.info("SQLiteDB was updated with Popularity report result.")

    else:
        print("Sorry, this technologies-scrapper is not implemented.")
