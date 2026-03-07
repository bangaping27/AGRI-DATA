import random
import time
from config import DELAY_KECAMATAN_MIN, DELAY_KECAMATAN_MAX, DELAY_KABUPATEN

def delay_kecamatan():
    time.sleep(random.uniform(DELAY_KECAMATAN_MIN, DELAY_KECAMATAN_MAX))

def delay_kabupaten():
    time.sleep(DELAY_KABUPATEN)
