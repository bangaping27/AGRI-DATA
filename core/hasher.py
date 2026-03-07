import hashlib

def generate_row_hash(row):
    desa = str(row.get('desa', '')).strip()
    id_poktan = str(row.get('id_poktan', '')).strip()
    nama_poktan = str(row.get('nama_poktan', '')).strip()
    
    hash_str = f"{desa}|{id_poktan}|{nama_poktan}"
    return hashlib.md5(hash_str.encode("utf-8")).hexdigest()

def hash_rows(rows):
    for r in rows:
        r['row_hash'] = generate_row_hash(r)
    return rows
