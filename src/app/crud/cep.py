import http.client
import json

def get_address_by_postal_code(postal_code: str):
    """
    Retorna um dicionário contendo informações sobre um endereço a partir do seu CEP.

    Args:
        postal_code (str): o CEP do endereço desejado.

    Returns:
        Optional[Dict[str, Union[str, Any]]]: um dicionário contendo as informações do endereço correspondente
        ao CEP informado, ou None caso o CEP seja inválido ou não seja encontrado.
    """

    conn = http.client.HTTPSConnection("viacep.com.br")
    payload = ""
    conn.request("GET", f"/ws/{postal_code}/json/", payload)
    res = conn.getresponse()
    data = res.read()
    data = json.loads(data.decode("utf-8"))
    
    if "erro" in data:
        return None
    
    return data

