from tkinter import Tk
from gui import GuiForJobsWebscraper

from datetime import date
from datetime import datetime
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

    root = Tk()
    GuiForJobsWebscraper(root)
    root.mainloop()
