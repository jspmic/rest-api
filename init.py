import os
from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from datetime import datetime
from pathlib import Path
from googleapiclient.discovery import build
from google.oauth2 import service_account
import logging

# Google drive scopes

SCOPES = ['https://www.googleapis.com/auth/drive.file']

# Changing to the current file path

PATH = str(Path(__file__).parent)  # Working in the same folder as the file
os.chdir(PATH)

# Enablig debugging for the google api client

logging.basicConfig(
    filename='google_api.log',
    filemode='a',
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logging.getLogger('googleapiclient').setLevel(logging.DEBUG)


# Authenticate to drive

def authenticate_drive():
    service_account_json_key = './starlit-byway-323113-7086966c4c67.json'
    credentials = service_account.Credentials.from_service_account_file(
                              filename=service_account_json_key,
                              scopes=SCOPES)
    return build('drive', 'v3', credentials=credentials)


# Logger function to register events


def logger(event: str) -> bool:
    """ Function to log a given event to a file called `log` """

    now = datetime.now().strftime("%d/%m/%y %H:%M:%S")
    log_mssg = f"{now} - {event}\n"
    with open("log", "a") as log:
        log.write(log_mssg)
    print(log_mssg)

# Constants section
# This section consists of the setup variables of the environment


load_dotenv()

CODE: str = os.getenv("CODE")
USER: str = os.getenv("_USER")
PASSWD: str = os.getenv("PASSWD")
HOST: str = os.getenv("HOST")
DB_NAME: str = os.getenv("DB_NAME")
API_ID: str = os.getenv("API_ID")
SECRET: str = os.getenv("COLLECTOR_SECRET")

# Initialization section

app = Flask(__name__)  # Flask app initialization

try:
    app.config["SQLALCHEMY_DATABASE_URI"] = \
            f"mysql://{USER}:{PASSWD}@{HOST}/{DB_NAME}"
    db = SQLAlchemy(app)
    api = Api(app)
except Exception as e:
    logger(f"Couldn't load database: {e}")
