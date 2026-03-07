import requests
import urllib3
from bs4 import BeautifulSoup
from config import BASE_URL
from utils.user_agent_rotator import get_random_user_agent

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def discover_provinces():
    url = f"{BASE_URL}/monpetanikec.php"
    headers = {"User-Agent": get_random_user_agent()}
    session = requests.Session()
    
    try:
        r = session.get(url, headers=headers, timeout=(10, 30), verify=False)
        soup = BeautifulSoup(r.text, "html.parser")
        
        provinces = []
        for option in soup.select("#cmbNegara option"):
            val = option.get("value")
            name = option.text.strip()
            if val and val != "":
                gov_id = val + "00" if len(val) == 2 else val
                provinces.append({"id": val, "gov_id": gov_id, "name": name})
        return provinces
    except Exception as e:
        print(f"Discovery Error: {e}")
        return []

def discover_districts(province_id):
    url = f"{BASE_URL}/getProvinsi.php"
    headers = {"User-Agent": get_random_user_agent()}
    session = requests.Session()
    
    try:
        # Note: the new platform uses POST and 'idNegara' for fetching districts ('cmbProvinsi')
        payload = {"idNegara": province_id}
        r = session.post(url, data=payload, headers=headers, timeout=(10, 30), verify=False)
        soup = BeautifulSoup(r.text, "html.parser")
        
        districts = []
        for option in soup.find_all("option"):
            val = option.get("value")
            name = option.text.strip()
            if val and val != "" and val.startswith(province_id[:2]):
                districts.append({"id": val, "name": name})
        return districts
    except Exception as e:
        print(f"District Discovery Error: {e}")
        return []

def discover_subdistricts(district_id):
    url = f"{BASE_URL}/getKecamatan.php"
    headers = {"User-Agent": get_random_user_agent()}
    session = requests.Session()
    
    try:
        # Note: the new platform uses POST and 'idProvinsi' for fetching subdistricts ('cmbKecamatan')
        payload = {"idProvinsi": district_id}
        r = session.post(url, data=payload, headers=headers, timeout=(10, 30), verify=False)
        soup = BeautifulSoup(r.text, "html.parser")
        
        subdistricts = []
        for option in soup.find_all("option"):
            val = option.get("value")
            name = option.text.strip()
            if val and val != "" and val.startswith(district_id):
                subdistricts.append({"id": val, "name": name})
        return subdistricts
    except Exception as e:
        print(f"Subdistrict Discovery Error: {e}")
        return []
