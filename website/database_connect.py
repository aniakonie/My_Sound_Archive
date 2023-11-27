import mysql.connector
from dotenv import load_dotenv
import os

def db_connect():

    load_dotenv()

    vml = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = os.getenv("PASSWORD"),
    database = "virtual_music_library"
    )

    cursor = vml.cursor()

    return vml, cursor