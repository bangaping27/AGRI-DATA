import pandas as pd
import os
from config import OUTPUT_FOLDER, CSV_ENCODING
from utils.string_utils import slugify

def deduplicate(province_name):
    slug = slugify(province_name)
    file_path = os.path.join(OUTPUT_FOLDER, f"data_prov_{slug}.csv")
    if not os.path.exists(file_path):
        return
        
    try:
        df = pd.read_csv(file_path, dtype=str)
        df = df.drop_duplicates(subset=["row_hash"])
        df.to_csv(file_path, index=False, encoding=CSV_ENCODING)
    except Exception as e:
        print(f"Failed to deduplicate {file_path}: {e}")
