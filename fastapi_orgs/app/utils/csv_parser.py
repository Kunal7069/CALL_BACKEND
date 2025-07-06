import csv
import os
from typing import Dict, List

import pandas as pd
from fastapi import UploadFile


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
        df = pd.DataFrame([summary])

        if not os.path.exists(CSV_PATH):
            df.to_csv(CSV_PATH, index=False)
        else:
            df.to_csv(CSV_PATH, mode="a", header=False, index=False)

    except Exception as e:
        print("Error while writing summary to CSV:", e)
        import traceback

        traceback.print_exc()
