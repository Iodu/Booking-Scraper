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
    's Gravesandestraat 55 Oost 1092 AA Amsterdam Netherlands',
    194,
    '8/4/2015',
    7.7,
    'Hotel Arena',
    'United Kingdom',
    'No Negative',
    0,
    1403,
    'The hotel is amazing beautiful old building and the rooms are very modern',
    15,
    1,
    9.2,
    "[' Leisure trip ', ' Group ', ' Duplex Double Room ', ' Stayed 5 nights ', ' Submitted from a mobile device ']",
    '730 day',
    '52.3605759',
    '4.9159683'
  )