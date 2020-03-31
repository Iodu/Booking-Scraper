import time
from datetime import datetime

import pandas as pd
from sqlalchemy import create_engine

from config import db_pass, db_user


def create_db_connection():
    return create_engine(
        f"mysql+mysqlconnector://{db_user}:{db_pass}@localhost/Hotel_reviews"
    )


def csv_to_df(file_name, seperator):
    file_name = r"Hotel_Reviews.csv"
    df = pd.read_csv(file_name, sep=seperator)
    df.head()
    return df


def sql_to_df(table_name):
    connection = create_db_connection()
    df = pd.read_sql_table(table_name, con=connection)
    return df


def _parse_tags(values):
    csv_parsed = values.copy()
    length = len(csv_parsed)
    del csv_parsed[-3:length]
    del csv_parsed[0:13]
    tags_string = ""
    for x in csv_parsed:
        tags_string += x
    return tags_string


def _parse_to_single_sql_insert_values(csv_row):
    values = csv_row.split(",")
    tags_str = _parse_tags(values)

    return f"""\'{values[0].strip()}\',
    {values[1].strip()},
    \'{values[2].strip()}\',
    {values[3].strip()},
    \'{values[4].strip()}\',
    \'{values[5].strip()}\',
    \'{values[6].strip()}\',
    {values[7].strip()},
    {values[8].strip()},
    {values[10].strip()},
    \'{values[9].strip()}\',
    {values[11].strip()},
    {values[12].strip()},
    {tags_str},
    \'{values[-3].strip()}\',
    \'{values[-2].strip()}\',
    \'{values[-1].strip()}\'
    """


def create_single_sql_insert():
    file = open(r"../Hotel_Reviews.csv", "r")
    file.readline()
    line = file.readline()
    values = _parse_to_single_sql_insert_values(line)

    return f"""
    USE Hotel_reviews;
    INSERT INTO reviews (
        Hotel_Address,
        Additional_Number_of_Scoring,
        Review_Date,
        Average_Score,
        Hotel_Name,
        Reviewer_Nationality,
        Negative_Review,
        Review_Total_Negative_Word_Counts,
        Total_Number_of_Reviews,
        Positive_Review,
        Review_Total_Positive_Word_Counts,
        Total_Number_of_Reviews_Reviewer_Has_Given,
        Reviewer_Score,
        Tags,
        days_since_review,
        lat,
        lng
    )
    VALUES
    (
        {values}
    )
    """
current_milli_time = lambda: int(round(time.time() * 1000))
