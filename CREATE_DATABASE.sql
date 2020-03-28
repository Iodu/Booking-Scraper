CREATE DATABASE IF NOT EXISTS Hotel_reviews;
USE Hotel_reviews;
CREATE TABLE IF NOT EXISTS uncleaned(
  id BIGINT NOT NULL AUTO_INCREMENT,
  Hotel_Address TEXT NOT NULL,
  Additional_Number_of_Scoring BIGINT,
  Review_Date TEXT,
  Average_Score DOUBLE,
  Hotel_Name TEXT NOT NULL,
  Reviewer_Nationality TEXT,
  Negative_Review TEXT,
  Review_Total_Negative_Word_Counts BIGINT,
  Total_Number_of_Reviews BIGINT,
  Positive_Review TEXT,
  Review_Total_Positive_Word_Counts BIGINT,
  Total_Number_of_Reviews_Reviewer_Has_Given BIGINT,
  Reviewer_Score DOUBLE,
  Tags TEXT,
  days_since_review TEXT,
  lat DOUBLE,
  lng DOUBLE,
  PRIMARY KEY (id)
);