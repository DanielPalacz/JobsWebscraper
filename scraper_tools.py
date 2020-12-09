from datetime import date


class JobsFileHandler:

    def __init__(self, source: str):
        self.filebasename = source
        self.filename = ""

    def initiate_filedb(self, *scraping_rules):
        self.filename = self.filebasename
        for rule in scraping_rules:
            self.filename += "_" + rule
        today = date.today()
        self.filename += "__" + str(today.strftime("%d%m%Y")) + ".txt"

        with open(self.filename, "w") as opened_dbfile:
            opened_dbfile.write("")

    def update_filedb(self, line: str):
        with open(self.filename, "a") as opened_dbfile:
            opened_dbfile.writelines(line)
            opened_dbfile.writelines("\n")
