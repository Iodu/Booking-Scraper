CREATE DATABASE IF NOT EXISTS Hotel_reviews;
USE Hotel_reviews;
CREATE TABLE IF NOT EXISTS cleaned(
  id BIGINT NOT NULL AUTO_INCREMENT,
  Negative_Review TEXT,
  Positive_Review TEXT,
  PRIMARY KEY (id)
);