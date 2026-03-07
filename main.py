import argparse
import sys
import logging
import datetime
import os

from core.discovery import discover_provinces, discover_districts, discover_subdistricts
from core.extractor import fetch_poktan
from core.processor import parse_table
from core.cleaner import clean_rows
from core.hasher import hash_rows
from core.deduplicator import deduplicate

from state.progress_manager import load_progress, save_progress, reset_progress
from monitoring.telegram_notifier import send_telegram

from utils.delay_manager import delay_kecamatan, delay_kabupaten
from utils.csv_writer import write_csv
from utils.string_utils import slugify

# Setup basic logging
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename='logs/harvester.log',
    level=logging.INFO,
    format='%(asctime)s | %(message)s',
    datefmt='%Y-%m-%d %H:%M'
)

def log_progress(province, district, subdistrict, rows, status):
    logging.info(f"{province} | {district} | {subdistrict} | {rows} | {status}")
    print(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}] {province} | {district} | {subdistrict} | {rows} | {status}")

def run_harvester(target_province=None, resume=False):
    state = {}
    if resume:
        state = load_progress()
        print(f"Resuming from state: {state}")
    
    provinces = discover_provinces()
    if not provinces:
        print("Failed to discover provinces.")
        return
        
    for prov in provinces:
        raw_id = prov["id"]
        gov_id = prov["gov_id"]
        prov_name = prov["name"]
        
        # Determine if we should process this province
        # target_province usually expects the gov_id like '3500' or 'ALL'
        if target_province and target_province != "ALL" and gov_id != target_province:
            continue
            
        if resume and state.get("province") and state["province"] != gov_id:
            continue
            
        send_telegram(f"[AGRI HARVESTER]\n\nStart scraping\nProvince: {prov_name}")
        
        # Districts discovery requires the raw ID
        districts = discover_districts(raw_id)
        
        for d_idx, kab in enumerate(districts):
            kab_id = kab["id"]
            kab_name = kab["name"]
            
            if resume and state.get("province") == gov_id and state.get("district") and state["district"] != kab_id:
                continue
                
            subdistricts = discover_subdistricts(kab_id)
            
            for s_idx, kec in enumerate(subdistricts):
                kec_id = kec["id"]
                kec_name = kec["name"]
                
                if resume and state.get("province") == gov_id and state.get("district") == kab_id and state.get("subdistrict"):
                    if state["subdistrict"] != kec_id:
                        continue
                    else:
                        print(f"Resumed at: {kec_name}")
                        resume = False
                
                try:
                    html_data = fetch_poktan(raw_id, kab_id, kec_id)
                    raw_rows = parse_table(html_data, gov_id, prov_name, kab_name, kec_name)
                    cleaned = clean_rows(raw_rows)
                    hashed = hash_rows(cleaned)
                    
                    if hashed:
                        write_csv(prov_name, hashed)
                        
                    save_progress(gov_id, kab_id, kec_id)
                    log_progress(gov_id, kab_id, kec_id, len(hashed), "success")
                    delay_kecamatan()
                    
                except Exception as e:
                    err_msg = f"CRITICAL ERROR\n\nHTTP Exception detected: {str(e)}\nScraper stopped at {kec_name}"
                    log_progress(gov_id, kab_id, kec_id, 0, f"error: {str(e)}")
                    print(err_msg)
                    send_telegram(err_msg)
                    sys.exit(1)
            
            progress_msg = f"Batch Complete\n\nProvince: {prov_name}\nKabupaten: {kab_name}\nProgress: {d_idx+1}/{len(districts)} Kabupaten"
            send_telegram(progress_msg)
            print(progress_msg)
            
            delay_kabupaten()
            
        deduplicate(prov_name)
        slug = slugify(prov_name)
        send_telegram(f"Province Completed\n\n{prov_name}\n\nRows collected: deduplicated\nFile: data/data_prov_{slug}.csv")
        print(f"Finished province {prov_name}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AGRI-DATA HARVESTER")
    parser.add_argument("--all", action="store_true", help="Run all provinces")
    parser.add_argument("--province", type=str, help="Run single province ID (e.g., 3500)")
    parser.add_argument("--resume", action="store_true", help="Resume from progress.json")
    
    args = parser.parse_args()
    
    try:
        if args.resume:
            run_harvester(resume=True)
        elif args.all:
            run_harvester(target_province="ALL")
        elif args.province:
            run_harvester(target_province=args.province)
        else:
            parser.print_help()
    except KeyboardInterrupt:
        print("\n[!] KeyboardInterrupt detected. State was automatically saved after the last successful batch. System exiting cleanly.")
        sys.exit(0)
