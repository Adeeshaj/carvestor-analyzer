import pandas as pd
from datetime import datetime

def preprocess(data):
    listings = pd.DataFrame(data, columns=["id", "listing_url", 'title', 'location', 'price', 'price_currency', 'listing_date', 'properties', 'description', 'scraped_date'])
    listings = pd.concat([listings, listings['properties'].apply(pd.Series)], axis=1).drop('properties', axis=1)
    listings = listings.loc[~listings['price'].isna()]
    listings = listings.rename(columns={"Brand: ": "brand", "Model: ": "model", "Mileage: ": "mileage", "Body type: ": "body_type", "Condition: ": "condition", "Fuel type: ": "fuel_type", "Transmission: ": "transmission", "Engine capacity: ": "engine_capacity", "Year of Manufacture: ": "year_of_manufacture", "Trim / Edition: ": "trim_edition"})
    listings = listings.loc[:,['listing_url','price', 'price_currency', 'brand', 'model', 'mileage', 'body_type', 'condition', 'fuel_type', 'transmission', 'engine_capacity', 'year_of_manufacture', 'trim_edition', 'listing_date', 'scraped_date']]
    listings = listings.drop_duplicates('listing_url')
    listings['listing_date'] = listings['listing_date'].apply(convert_to_datetime)
    return listings


def convert_to_datetime(posted_string):
    """
    Custom function to convert the string to a datetime object
    """
    date_format = "%Y %d %b %I:%M %p"
    current_year = datetime.now().year
    posted_string_with_year = posted_string.replace("Posted on ", f"{current_year} ")
    date_time = datetime.strptime(posted_string_with_year, date_format)
    return date_time.strftime("%Y-%m-%d")