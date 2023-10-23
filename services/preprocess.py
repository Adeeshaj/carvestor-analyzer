import pandas as pd

def preprocess(data):
    listings = pd.DataFrame(data, columns=["id", "listing_url", 'title', 'location', 'price', 'price_currency', 'listing_date', 'properties', 'description'])
    listings = listings.loc[~listings['price'].isna()]
    return listings