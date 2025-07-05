import csv
from typing import List, Dict
from fastapi import UploadFile
import os
import pandas as pd

async def parse_csv_files(files: List[UploadFile]) -> Dict[str, list]:
    result = {}
    for file in files:
        content = await file.read()
        decoded = content.decode("utf-8").splitlines()
        reader = csv.reader(decoded)
        result[file.filename] = list(reader)
    return result


CSV_PATH = "log.csv"

async def save_summary_to_csv(summary: dict):
    try:
        print("➡️ Received summary to write:", summary)  # Debug print

        df = pd.DataFrame([summary])

        if not os.path.exists(CSV_PATH):
            print("📝 Creating new CSV file.")
            df.to_csv(CSV_PATH, index=False)
        else:
            print("📎 Appending to existing CSV file.")
            df.to_csv(CSV_PATH, mode='a', header=False, index=False)

        print(f"✅ Call summary saved to {CSV_PATH}")

    except Exception as e:
        print("❌ Error while writing summary to CSVVVVVVVVVVVVVVVVVVVVVVVVVVVV:",e)
        import traceback
        traceback.print_exc()