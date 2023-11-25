import psycopg2
import logging
import sys
from dotenv import load_dotenv
import os
from services.preprocess import preprocess

logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load the .env file
load_dotenv()

DB_URL =  os.environ.get("PSQL_DB_URL")
listings_table="listings"
processed_listings_table = "processed_listings"



try:
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()

    query = f"SELECT * FROM {listings_table}"
    cur.execute(query)
    rows = cur.fetchall()

    logging.info(f"Read {len(rows)} listings from database")

    #get preprocessed df
    listings_df = preprocess(rows)
    listings = listings_df.to_dict(orient='records')
    for listing in listings:
        # Insert data from each dictionary into the database
        columns = ', '.join(listing.keys())
        values = ', '.join(['%s' for _ in listing])
        insert_query = f"INSERT INTO {processed_listings_table} ({columns}) VALUES ({values})"
        try:
            cur.execute(insert_query, list(listing.values()))
        except Exception as e:
            logging.error(str(e))


    # Commit the transaction after inserting all the data
    conn.commit()

    logging.info("Data inserted successfully.")

except Exception as e:
    logging.exception(e)

finally:
    if 'cur' in locals() and cur:
        cur.close()
    if 'conn' in locals() and conn:
        conn.close()
