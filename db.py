# from sqlite3 import OperationalError
import sqlite3

DB_NAME = "JobScraperDB.sqlite"


sql_create_table_competences_results = """CREATE TABLE IF NOT EXISTS competences_results (
ID INTEGER PRIMARY KEY,
filename TEXT,
jobsource TEXT,
search_filter TEXT,
day INTEGER,
competency_name TEXT,
competency_frequency INTEGER)"""

sql_insert_into_competences_results = "INSERT INTO competences_results VALUES (?,?,?,?,?,?,?)"


def __get_competencies_stats(filestring: str) -> dict():
    competencies_stats = dict()
    with open(f"output_files\\{filestring}") as f:
        for line in f:
            splitted_line = line.split(",")
            competencies_stats[splitted_line[0]] = splitted_line[1].replace("\n", "")
    return competencies_stats


def __parse_filename(filestringname: str) -> dict:
    splitted_filestringname = filestringname.split("__")
    parsed_filestringname = dict()
    parsed_filestringname["jobsource"] = splitted_filestringname[0]
    parsed_filestringname["search_filter"] = splitted_filestringname[1].replace("_", "+")
    parsed_filestringname["day"] = splitted_filestringname[2]

    return parsed_filestringname


def initialize_db():
    with sqlite3.connect(DB_NAME) as db_conn:
        c = db_conn.cursor()
        c.execute(sql_create_table_competences_results)


def update_db(filestringname: str) -> None:
    parsed_filestringname = __parse_filename(filestringname)
    jobsource = parsed_filestringname["jobsource"]
    search_filter = parsed_filestringname["search_filter"]
    day = parsed_filestringname["day"]

    competency_stats = __get_competencies_stats(filestringname)
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    for k, v in competency_stats.items():
        c.execute(sql_insert_into_competences_results, (None, filestringname, jobsource, search_filter, day, k, v))

    conn.commit()
    conn.close()


if __name__ == "__main__":
    pass
