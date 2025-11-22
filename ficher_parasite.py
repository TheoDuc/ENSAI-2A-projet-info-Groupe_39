import requests

url = "http://localhost:5432/admin/crediter/Théo/100"
params = {"est_admin": True}

response = requests.put(url, params=params)
print(response.json())
