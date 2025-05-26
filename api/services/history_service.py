import pandas as pd
from utils.db import get_collection

def get_history_data(symbol):
    collection = get_collection()
    data = list(collection.find({'symbol': symbol.upper()}, {'_id': 0}))
    df = pd.DataFrame(data)
    if not df.empty:
        df['scraped_at'] = pd.to_datetime(df['scraped_at'])
        df = df.sort_values('scraped_at')
    return df

def get_all_symbols_data():
    collection = get_collection()
    return sorted(collection.distinct("symbol"))
