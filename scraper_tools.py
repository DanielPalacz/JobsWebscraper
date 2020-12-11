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


class TechDomainAnalyzer:

    def __init__(self, src: str = "f", technologies: str = "testing,python,selenium"):
        self.__technologies_filter = technologies
        self.__source = src
        self.__report_name = ""

    def get_tech_filters(self) -> list():
        return self.__technologies_filter.split(",")

    def get_job_source(self) -> str:
        return self.__source

    def setup_tech_filters(self):
        pass

    def setup_job_source(self):
        pass

    def __set_report_name(self, day=date.today()):
        used_day = day
        scrapped_data_report = ""
        if self.__source == "f":
            scrapped_data_report += "NoFluffJobsPl__"
        scrapped_data_report += self.__technologies_filter.replace(",", "_")
        scrapped_data_report += "__" + str(used_day.strftime("%d%m%Y")) + ".txt"
        self.__report_name = scrapped_data_report

    def __get_all_unique_technologies(self) -> set():
        self.__set_report_name()
        all_competencies = []
        try:
            for line in open(self.__report_name, "r"):
                splitted_line_table = line.split(",")
                for i, v in enumerate(splitted_line_table):
                    if i != 0 and len(v) != 0:
                        all_competencies.append(v.replace("\n", ""))
        except FileNotFoundError as e:
            print(str(e))
            return set()

        return set(all_competencies)

    def generate_tech_popularity_report(self):
        unique_tech_set = self.__get_all_unique_technologies()
        if len(unique_tech_set) == 0:
            exit()
        tech_popularity = dict()
        for competency in unique_tech_set:
            tech_popularity[competency] = 0
        for line in open(self.report_name, "r"):
            for competency in unique_tech_set:
                if line.count(competency) > 0:
                    tech_popularity[competency] += 1
        sorted_x = sorted(tech_popularity.items(), key=lambda kv: kv[1], reverse=True)

        popularity_report_name = self.report_name.replace(".txt", "__popularity_report.csv")
        with open(popularity_report_name, "w") as popularity_report_file:
            for k, v in sorted_x:
                line = str(k) + ",", str(v)
                popularity_report_file.writelines(line)
                popularity_report_file.writelines("\n")


if __name__ == "__main__":
    pass
