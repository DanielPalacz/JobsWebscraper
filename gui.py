from tkinter import *
from tkinter import ttk

from JobWwwPortals import NoFluffJobsPl
from scraper_tools import TechDomainAnalyzer
import db

import time
import logging


class GuiForJobsWebscraper:

    def __init__(self, root):
        """...."""

        root.title("Jobs Webscraper")
        mainframe = ttk.Frame(root, padding="3 3 12 12")
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        #
        ttk.Button(mainframe, text="JobsWebscraper", command=self.run_jobswebscraper).grid(column=3, row=3, sticky=W)
        #
        filter_names = ["testing", "selenium", "python"]
        cnames = StringVar(value=filter_names)
        self.lbox = Listbox(mainframe, selectmode=MULTIPLE, listvariable=cnames, height=3)
        self.lbl = ttk.Label(mainframe, text="Choose Job Filters:")
        self.lbox.grid(column=0, row=1, rowspan=1, sticky=(N, S, E, W))
        self.lbl.grid(column=0, row=0, padx=10, pady=5, sticky=(W,))
        #
        for child in mainframe.winfo_children():
            child.grid_configure(padx=5, pady=5)
        #
        self.logger = logging.getLogger()
        self.jobscraper = None
        self.technologies_analyzer = None

    def run_jobswebscraper(self):
        selected_filters = [self.lbox.get(idx) for idx in self.lbox.curselection()]
        selected_filters_str = ",".join(selected_filters)
        self.jobscraper = NoFluffJobsPl()
        self.logger.info("Creating TechDomainAnalyzer object for: f-scrapper with" + selected_filters_str + "filter.")
        self.technologies_analyzer = TechDomainAnalyzer("f", selected_filters_str)
        self.jobscraper.start_session_with_def_configuration()
        time.sleep(1)
        self.jobscraper.run_data_scraper(self.technologies_analyzer.get_tech_filters())
        popularity_report_name = self.technologies_analyzer.generate_tech_popularity_report()
        self.logger.info("Popularity report was just generated: " + popularity_report_name + ".")

        db.initialize_db()
        db.update_db(popularity_report_name)
        self.logger.info("SQLiteDB was updated with Popularity report result.")


if __name__ == "__main__":
    root = Tk()
    GuiForJobsWebscraper(root)
    root.mainloop()
