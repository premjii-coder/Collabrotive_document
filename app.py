import os

from flask import Flask, request, jsonify, render_template, redirect, url_for,send_file
from faker import Faker
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import SyncGrant
from werkzeug.utils import secure_filename

app = Flask(__name__)
fake = Faker()


@app.route('/')
def index():
    return render_template('index.html')

# Add your Twilio credentials
@app.route('/token')
def generate_token():
    TWILIO_ACCOUNT_SID = "ACc51c51034a3327693f478e7dcfcc9709"
    TWILIO_SYNC_SERVICE_SID = "ISf778fa7d54f069e6cf8c27262d0c78bb"
    TWILIO_API_KEY = "SK6a78100683323d01d76d1721bc8fa084"
    TWILIO_API_SECRET = "X1XBz80kED8ZqwGXaGoMkZjx0anLHmlP"

    username = request.args.get('username', fake.user_name())

    # create access token with credentials
    token = AccessToken(TWILIO_ACCOUNT_SID, TWILIO_API_KEY, TWILIO_API_SECRET, identity=username)
    # create a Sync grant and add to token
    sync_grant_access = SyncGrant(TWILIO_SYNC_SERVICE_SID)
    token.add_grant(sync_grant_access)
    return jsonify(identity=username, token=token.to_jwt().decode())

# Write the code here
@app.route('/', methods=['POST'])
def download_text():
    text_from_notepad= request.form["text"]
    with open("work_file.txt","w") as f:
        f.write(text_from_notepad)
        path_to_store_file="work_file.txt"
        return send_file(path_to_store_file,as_attachment=True)
    
    
        

    

    


if __name__ == "__main__":
    app.run(host='localhost', port='5001', debug=True)
