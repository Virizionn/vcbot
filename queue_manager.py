import gspread
import pandas as pd
import traceback
from dotenv import load_dotenv
import os

load_dotenv()

#credential is an env variable containing a dict
credential = os.getenv("GOOGLE_SERVICE_ACCOUNT")

#convert string to dict
credential = eval(credential)

gc = gspread.service_account_from_dict(credential)

def get_queue():

  try:
    sh = gc.open_by_url(
      """https://docs.google.com/spreadsheets/d/1j-Ny43mj9cY_Im4N9mOrLfIYpDTK-4Jk90OKdcASgfA/edit?usp=sharing"""
    )
    worksheets = sh.worksheets()
    format = ""
    for ws in worksheets:
      if ws.title != "Example Format":
        game = ws.title
        #get sheet as a dataframe
        df = pd.DataFrame(ws.get_all_records())

        format = format + f"**{game}**\n\n"
        for index, row in df.iterrows():
          format = format + f"{row['Time Period']}: {row['Host']}\n"
          if row['Time Period'] == "Current":
            format = format + '\n'
        format = format + '\n'
        

    return (format)
  except:
    traceback.print_exc()
    return (
      "Google API rate limit exceeded, or API credential fail. Wait a few minutes before updating."
    )