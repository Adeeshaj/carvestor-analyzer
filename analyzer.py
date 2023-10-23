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
table_name="listings"


try:
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()

    query = f"SELECT * FROM {table_name}"
    cur.execute(query)
    rows = cur.fetchall()

    logging.info(f"Read {len(rows)} listings from database")

    #get preprocessed df
    listings_df = preprocess(rows)


except Exception as e:
    logging.exception(e)

finally:
    if 'cur' in locals() and cur:
        cur.close()
    if 'conn' in locals() and conn:
        conn.close()
