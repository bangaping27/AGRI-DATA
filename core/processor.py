import pandas as pd
import datetime
import gc
from io import StringIO

def parse_table(html_text, prov_id, prov_name, kab_name, kec_name):
    try:
        tables = pd.read_html(StringIO(html_text))
        if not tables or len(tables) == 0:
            return []
        # Usually the new endpoint stores actual poktan list in tables[1] or tables[0] based on structure. Let's get the largest table or one with specific columns.
        df = None
        for t in tables:
            if not t.empty and ('Id Poktan' in t.iloc[0].values or 'Nama Poktan' in t.iloc[0].values):
                df = t
                break
        if df is None:
            df = tables[-1] if len(tables) > 1 else tables[0]

        if df.empty:
            del tables
            gc.collect()
            return []

        # Convert to string types entirely
        df = df.astype(str)

        header_row_idx = 0
        df.columns = df.iloc[header_row_idx].fillna('').str.strip()
    except Exception:
        return []
        
    raw_rows = df.to_dict(orient="records")
    del df
    del tables
    gc.collect()
    
    results = []
    now = datetime.datetime.now().isoformat()
    
    for row in raw_rows:
        parsed = {
            "id_prov_gov": prov_id,
            "nama_prov": prov_name,
            "nama_kab": kab_name,
            "nama_kec": kec_name,
            "desa": "",
            "id_poktan": "",
            "nama_poktan": "",
            "ketua": "",
            "penyuluh": "",
            "scraped_at": now
        }
        
        for k, v in row.items():
            k_lower = str(k).lower()
            val = str(v) if pd.notna(v) else ""
            
            if "desa" in k_lower or "alamat" in k_lower:
                parsed["desa"] = val
            elif "id" in k_lower and "poktan" in k_lower:
                parsed["id_poktan"] = val
            elif "nama" in k_lower and "poktan" in k_lower:
                parsed["nama_poktan"] = val
            elif "ketua" in k_lower:
                parsed["ketua"] = val
            elif "penyuluh" in k_lower:
                parsed["penyuluh"] = val
            elif "nik" in k_lower:
                parsed["nik"] = val
                
        results.append(parsed)
        
    return results
