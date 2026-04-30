import requests
import json

# Ek dummy URL jahan se JSON data milta hai
url = "https://jsonplaceholder.typicode.com/users/1"

# Internet se data maangna (Request)
response = requests.get(url)

# Agar request successful rahi (Status 200)
if response.status_code == 200:
    # .json() function se direct Python dictionary mil jati hai
    user_data = response.json()
    
    print(f"User ka naam: {user_data['name']}")
    print(f"User ki email: {user_data['email']}")
    print(f"Shehar: {user_data['address']['city']}") # Nested JSON handle karna
else:
    print("Kuch gadbad ho gayi!")