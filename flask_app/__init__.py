from flask import Flask

app = Flask(__name__)

app.secret_key = "secretkey"
#change the secret key each project