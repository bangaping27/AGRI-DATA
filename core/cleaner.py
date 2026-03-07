def clean_rows(rows):
    cleaned = []
    for row in rows:
        # Remove Header Rows
        # Jika row berisi "No", "Nama Poktan", "Ketua"
        nama = str(row.get("nama_poktan", "")).strip()
        ketua = str(row.get("ketua", "")).strip()
        
        if nama.lower() == "nama poktan" or ketua.lower() == "ketua" or nama.lower() == "no":
            continue
            
        # Remove Empty Rows (all col empty)
        if all(not str(v).strip() for v in row.values()):
            continue
            
        # Normalize Whitespace
        cleaned_row = {k: str(v).strip() if v else "" for k, v in row.items()}
        
        # Additional empty check after strip
        if all(v == "" for v in cleaned_row.values()):
            continue
            
        cleaned.append(cleaned_row)
        
    return cleaned
