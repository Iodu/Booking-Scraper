import pandas as pd

from helper import create_db_connection, csv_to_df, sql_to_df

engine = create_db_connection()

# file_name = input("What reviews csv file to import into db? ")
file_name = r"Hotel_Reviews.csv"


# Remove all columns but Positive_Review and Negative_Review
def _remove_all_but_review_texts(df):
    columns = list(df.columns)
    if "Positive_Review" in columns:
        columns.remove("Positive_Review")
    if "Negative_Review" in columns:
        columns.remove("Negative_Review")
    return df.drop(columns=columns)


def _concat_all_reviews_with_label_column(df):
    negative_reviews = df.loc[:, ["Negative_Review"]]
    positive_reviews = df.loc[:, ["Positive_Review"]]

    positive_reviews["label"] = 1
    negative_reviews["label"] = 0

    renamed_positive_reviews = positive_reviews.rename(
        {"Positive_Review": "review"}, axis=1
    )
    renamed_negative_reviews = negative_reviews.rename(
        {"Negative_Review": "review"}, axis=1
    )

    return pd.concat([renamed_positive_reviews, renamed_negative_reviews], axis=0)

def uncleaned_csv_to_cleaned_df():
    df = csv_to_df(file_name, ",")
    df = uncleaned_df_to_cleaned_df(df)
    return df

def uncleaned_df_to_cleaned_df(uncleaned_df):
    df = _remove_all_but_review_texts(uncleaned_df)
    concated_df = _concat_all_reviews_with_label_column(df)

    # Remove all 'No Negative" and 'No Positive" reviews-texts
    cleaned_df = concated_df.loc[lambda x: x["review"] != "No Negative"].loc[
        lambda x: x["review"] != "No Positive"
    ]
    return cleaned_df


def uncleaned_sql_to_cleaned_df():
    df = sql_to_df("uncleaned_reviews")
    cleaned_df = uncleaned_df_to_cleaned_df(df)
    return cleaned_df


def uncleaned_csv_to_sql():
    df = csv_to_df(file_name, ",")
    df.to_sql(
        name="uncleaned_reviews",
        con=engine,
        chunksize=1000,
        if_exists="replace",
    )


def cleaned_sql_to_df():
    df = sql_to_df("cleaned_reviews")
    return df


def cleaned_df_to_sql(cleaned_df):
    cleaned_df.to_sql(
        name="cleaned_reviews",
        con=engine,
        chunksize=1000,
        if_exists="replace",
    )


def uncleaned_sql_to_cleaned_sql():
    cleaned_df = uncleaned_sql_to_cleaned_df()
    cleaned_df_to_sql(cleaned_df)


df = cleaned_sql_to_df()
