import requests
import urllib3
import time
from utils.user_agent_rotator import get_random_user_agent
from config import BASE_URL, ENDPOINT_POKTAN

def fetch_poktan(prov_id, kab_id, kec_id):
    url = f"{BASE_URL}{ENDPOINT_POKTAN}"
    
    headers = {
        "User-Agent": get_random_user_agent(),
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    payload = {
        "cmbNegara": prov_id,
        "cmbProvinsi": kab_id,
        "cmbKecamatan": kec_id
    }
    
    session = requests.Session()
    max_retries = 3
    
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    for attempt in range(max_retries):
        try:
            r = session.post(
                url,
                headers=headers,
                data=payload,
                timeout=(10, 30),
                verify=False
            )
            
            if r.status_code == 403:
                raise Exception("HTTP 403 Forbidden")
                
            if r.status_code == 429:
                time.sleep(60)
                continue
                
            if r.status_code == 500:
                time.sleep(10)
                continue
                
            r.raise_for_status()
            return r.text
            
        except requests.exceptions.Timeout:
            if attempt == max_retries - 1:
                raise
            time.sleep(10)
        except Exception as e:
            if attempt == max_retries - 1 or "403" in str(e):
                raise
            time.sleep(10)
            
    return ""
