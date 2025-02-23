import requests

def conectar_ha(config):
    url = config['ha']['url']
    token = config['ha']['token']
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        # Realiza una petición de prueba a la API de Home Assistant
        response = requests.get(f"{url}/api/", headers=headers)
        if response.status_code == 200:
            print("Conexión con Home Assistant exitosa.")
        else:
            print(f"Error en la conexión con Home Assistant: {response.status_code}")
    except Exception as e:
        print(f"Excepción al conectar con Home Assistant: {e}")
