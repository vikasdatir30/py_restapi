import requests as req

print(req.get('http://127.0.0.1:5000/get').json())
