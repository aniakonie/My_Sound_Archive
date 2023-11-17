import mysql.connector

def db_connect():

    vml = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "password",
    database = "virtual_music_library"
    )

    cursor = vml.cursor()

    return vml, cursor