<h1 align="center"> My Sound Archive </h1> <br>

<p align="center">
  <a href="http://mysoundarchive.com/">
    <img alt="MySoundArchive" title="MySoundArchive" src="https://github.com/aniakonie/My_Sound_Archive/assets/112773165/b92cfdc9-42b2-4744-8ac1-4f3691d15dc7/logo-inkscape-svg.png" width="200">
  </a>
</p>

A web application that displays Spotify user's library organized into artists, genres and subgenres folders, offering a convenient way to browse through the music collection.

## What problem does it solve

Spotify is renowned for its highly effective music recommendation algorithm, yet the user's library lacks methods for organizing its content. While it's easy to discover new music to add to your collection, it becomes increasingly challenging to keep track of it.

Unless you search through a long list of liked songs or artists when selecting something to listen to there's a risk of missing a significant portion of your content. While it's possible to organize songs into playlists, adding them all to playlists isn't a practical solution. Playlists can be organized into folders but unfortunately this feature is not extended to artists whom the user follows.

## In what way does it solve this problem

My Sound Archive app retrieves liked songs and all tracks from a user's playlists through the Spotify API. It then consolidates them and organizes the collection into corresponding artists and genres folders. Users can play songs on Spotify by using the links provided within the app.

<p align="center">
    <img alt="MySoundArchive" title="MySoundArchive" src="https://github.com/aniakonie/My_Sound_Archive/assets/112773165/7732115e-dce4-400b-b908-4ba6d3d386a9/Capture.png" width="700">
</p>

## Technologies used

* Python 3.9
* Flask 2.2
* SQLAlchemy 1.4
* PostgreSQL 16
* Jinja2 3.1
* Bootstrap 5.3
* Pytest 8.1
* WTForms 3.1

## APIs used

My Sound Archive app uses Spotify API (REST API) with OAuth 2.0 standard.
The authorization code flow used in the app is shown in the following Whimsical schema:

https://whimsical.com/vml-s-oauth-2-0-AK9SEvFpFv4AvF9nLMGuSb

## Whimsical mockup designs

Mockup designs for the app can be found in the following link:

https://whimsical.com/vml-mockups-3bYjFTHMP4NWSAbbUh7khH

## Deployed website

You can access the live version of the web app here: http://mysoundarchive.com/

## Project status

Project is currently in development mode, which means that it can serve up to 25 users (according to Spotify's rules).

Some of the improvements on the horizon:

* submitting an extension request to Spotify for the app (to serve more users),
* addressing library retrieval failures caused by temporary issues in Spotify's backend,
* improving the algorithm for assigning genres to artists,
* adding an option to modify genres assigned by the app,
* integrating Google authentication.

## What I'm currently working on

You can check what I am currently working on here:
http://github.com/users/aniakonie/projects/1

## Setup

1. Clone repository<br>
    `git clone https://github.com/aniakonie/My_Sound_Archive.git`
2. Install Python3.9 if you haven't already. Download it from https://www.python.org/downloads/.

3. Set up a virtual environment with Python3.9<br>
    `python3.9 -m venv venv_name`<br>
    Replace `venv_name` with the desired name for the environment.
    If this command does not work, try providing the full path to your Python executable:<br>
    `C:\Users\Name\AppData\Local\Programs\Python\Python39\python3.9 -m venv venv_name`
4. Navigate to the root directory of the project, activate it and install all dependencies from     requirements.txt file.<br>
    `venv_name\Scripts\activate`<br>
    `python -m pip install -r requirements.txt`
5. Create a new .env file and save it in the root directory of the project.<br>

    Add the following variables in the file (values to be added in the next steps):<br>
    `CLIENT_ID = ""`<br>
    `CLIENT_SECRET = ""`<br>
    `SECRET_KEY = ""`<br>
    `DATABASE_URL = ""`<br>
    `APP_SETTINGS = "config.DevelopmentConfig"`<br>
    `REDIRECT_URI_SPOTIFY = "http://127.0.0.1:5000/spotify/callback"`<br>
    <br>
    (`SECRET_KEY` should be a long random bytes or str)

6. Head over to Spotify for developers: http://developer.spotify.com/<br>
    Go to your dashboard and create a new app.<br>
    In "Redirect URIs" field paste the following link: http://127.0.0.1:5000/spotify/callback<br>
    Copy your Client ID and Client Secret to your .env file (`CLIENT_ID` and `CLIENT_SECRET`).

7. Install PostgreSQL and create a new database. It will store users' login credentials and data retrieved from Spotify.<br>
    Add your database url to your .env file (`DATABASE_URL`).<br>
    The URI scheme can be of the following form:<br>
    `"postgresql://[username]:[password]@[host]:[port]/[database_name]"`<br>
    Replace the placeholders in square brackets with your actual PostgreSQL credentials.

8. Navigate to the root directory of the project, activate your environment and initialize database migrations with the following command:<br>

    `flask --app main db init --directory website/database/migrations`<br>

    `"--directory website/database/migrations"` part is optional - if not included, migrations folder will be created in the root directory<br>

    Create tables in your database with the following commands:<br>

    `flask --app main db migrate --directory website/database/migrations`<br>
    `flask --app main db upgrade --directory website/database/migrations`<br>

9. With your environment activated, run the application using `main.py`<br>

    With the development server running, visit the following URL in your browser:<br>
    http://127.0.0.1:5000/


## Testing

In order to perform tests navigate to the root folder of the project and run tests with the following command:
`pytest tests\test_library.py`