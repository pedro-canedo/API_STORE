import http.client
import json

def get_address_by_postal_code(postal_code: str):

    conn = http.client.HTTPSConnection("viacep.com.br")
    payload = ""
    conn.request("GET", f"/ws/{postal_code}/json/", payload)
    res = conn.getresponse()
    data = res.read()
    data = json.loads(data.decode("utf-8"))
    
    if "erro" in data:
        return None
    
    return data

