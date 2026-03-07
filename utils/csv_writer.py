import pandas as pd
import os
from config import OUTPUT_FOLDER, CSV_ENCODING
from utils.string_utils import slugify

def write_csv(province_name, rows):
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)
        
    slug = slugify(province_name)
    file = os.path.join(OUTPUT_FOLDER, f"data_prov_{slug}.csv")
    df = pd.DataFrame(rows)
    
    df.to_csv(
        file,
        mode="a",
        index=False,
        header=not os.path.exists(file),
        encoding=CSV_ENCODING
    )
