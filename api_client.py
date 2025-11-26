import requests
from config import REGISTER_API_URL, HTTP_TIMEOUT

def api_call(serial: str, action:str):
    try:
        payload = {
            "serial": serial,
            "action": action
        }

        r = requests.post(REGISTER_API_URL, data=payload, timeout=HTTP_TIMEOUT)

        if r.status_code == 200:
            return True, r.text
        else:
            return False, f"HTTP {r.status_code}: {r.text}"

    except Exception as e:
        return False, str(e)