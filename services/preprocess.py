import pandas as pd

def preprocess(data):
    listings = pd.DataFrame(data, columns=["id", "listing_url", 'title', 'location', 'price', 'price_currency', 'listing_date', 'properties', 'description', 'scraped_date'])
    listings = pd.concat([listings, listings['properties'].apply(pd.Series)], axis=1).drop('properties', axis=1)
    listings = listings.loc[~listings['price'].isna()]
    listings = listings.rename(columns={"Brand: ": "brand", "Model: ": "model", "Mileage: ": "mileage", "Body type: ": "body_type", "Condition: ": "condition", "Fuel type: ": "fuel_type", "Transmission: ": "transmission", "Engine capacity: ": "engine_capacity", "Year of Manufacture: ": "year_of_manufacture", "Trim / Edition: ": "trim_edition"})
    listings = listings.loc[:,['listing_url','price', 'price_currency', 'brand', 'model', 'mileage', 'body_type', 'condition', 'fuel_type', 'transmission', 'engine_capacity', 'year_of_manufacture', 'trim_edition', 'listing_date', 'scraped_date']]
    listings = listings.drop_duplicates('listing_url')
    return listings