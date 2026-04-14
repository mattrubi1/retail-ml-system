import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

SCOPE = ["https://www.googleapis.com/auth/spreadsheets"]

CREDS = Credentials.from_service_account_file("credentials.json", scopes=SCOPE)

client = gspread.authorize(CREDS)

sheet = client.open("Retail_AI_DB").sheet1

def write_rows(rows):
    sheet.clear()
    sheet.append_row(["sku","price","drop_pct","velocity","ml_score","timestamp"])

    for r in rows:
        sheet.append_row([
            r["sku"], r["price"], r["drop_pct"],
            r["velocity"], r["ml_score"], r["timestamp"]
        ])

def read_data():
    return pd.DataFrame(sheet.get_all_records())
