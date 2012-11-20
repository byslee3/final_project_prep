

create table Sets(
    id INTEGER PRIMARY KEY,
    set_id VARCHAR(64),
    seo_title VARCHAR(64),
    title VARCHAR(64),
    anchor VARCHAR(64),
    set_type VARCHAR(64),
    creator_id VARCHAR(64),
    creator_name VARCHAR(64),
    created_on VARCHAR(64),
    imgurl TEXT,
    score REAL,
    pageviews INTEGER,
    num_fans INTEGER,
    num_items_all INTEGER,
    num_items_valid INTEGER,
    level REAL
);


create table Sets_Fans(
    id INTEGER PRIMARY KEY,
    set_id VARCHAR(64),
    fan_id VARCHAR(64),
    fan_name VARCHAR(64),
    level REAL
);


create table Sets_Items(
    id INTEGER PRIMARY KEY,
    set_id VARCHAR(64),
    item_id VARCHAR(64),
    item_seo_title VARCHAR(64),
    level REAL
);


create table Fans_Sets(
    id INTEGER PRIMARY KEY,
    fan_id VARCHAR(64),
    set_id VARCHAR(64),
    set_seo_title VARCHAR(64),
    level REAL
);


create table Users_Items(
    id INTEGER PRIMARY KEY,
    user_id VARCHAR(64),
    item_id VARCHAR(64),
    item_seo_title VARCHAR(64),
    level REAL
);


create table Items_Sets(
    id INTEGER PRIMARY KEY,
    item_id VARCHAR(64),
    set_id VARCHAR(64),
    set_seo_title VARCHAR(64),
    level REAL
);


create table Items(
    id INTEGER PRIMARY KEY,
    item_id VARCHAR(64),
    seo_title VARCHAR(64),
    title VARCHAR(64),
    anchor VARCHAR(64),
    age INTEGER,
    imgurl TEXT,
    save_count INTEGER,
    category_id VARCHAR(64),
    brand_id VARCHAR(64),
    brand_name VARCHAR(64),
    usd_price REAL,
    retailer VARCHAR(64),
    level REAL
);


create table Users(
    id INTEGER PRIMARY KEY,
    user_id VARCHAR(64),
    user_name VARCHAR(64),
    country VARCHAR(30),
    createdon_ts VARCHAR(64),
    level REAL
);



















