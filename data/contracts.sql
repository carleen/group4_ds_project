-- Table: listings
DROP TABLE IF EXISTS listings;
CREATE TABLE listings(
    id int PRIMARY KEY,
);

-- Table: listings-2
DROP TABLE IF EXISTS listings_2;
CREATE TABLE listings(
    id int PRIMARY KEY,
    host_id int,
);

-- Table: calendar
DROP TABLE IF EXISTS calendar;
CREATE TABLE calendar(
    listing_id int,
    adjusted_price float
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
