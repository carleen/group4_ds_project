-- Table: listings
DROP TABLE IF EXISTS listings;
CREATE TABLE listings(
    id int PRIMARY KEY,
    host_id int,
    host_since varchar(255),
    host_response_time varchar(255),
    host_response_rate varchar(255),
    host_acceptance_rate varchar(255),
    host_is_superhost varchar(255),
    property_type varchar(255),
    room_type varchar(255),
    accomodates int,
    bathrooms float,
    bedrooms int,
    beds int,
    price float,
    minimum_nights int,
    maximum_nights int
    number_of_reviews int,
    review_scores_rating float,
    instant_bookable varchar(255)
);

-- Table: listings-2
DROP TABLE IF EXISTS listings_2;
CREATE TABLE listings(
    id int PRIMARY KEY,
    host_id int,
    neighbourhood_group varchar(255),
    neighbourhood varchar(255),
    latitude float,
    longitude float,
    room_type varchar(255),
    price float,
    minimum_nights int,
    number_of_reviews int
);

-- Table: calendar
DROP TABLE IF EXISTS calendar;
CREATE TABLE calendar(
    id int PRIMARY KEY,
    listing_id int,
    adjusted_price float,
    date varchar(255),
    available varchar(255),
    price float,
    minimum_nights int,
    maximum_nights int
);

-- Table: neighborhoods
DROP TABLE IF EXISTS neighborhoods;
CREATE TABLE neighborhoods(
    id int PRIMARY KEY,
    neighborhood varchar(255)
);

-- Table: reviews
DROP TABLE IF EXISTS reviews;
CREATE TABLE reviews(
    id int PRIMARY KEY,
    listing_id int
);

-- Table: reviews-2
DROP TABLE IF EXISTS reviews_2;
CREATE TABLE reviews_2(
    listing_id int,
    date varchar(255)
);
