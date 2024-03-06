# Virtual Music Library

A web application that displays Spotify user's library organized into artists, genres and subgenres folders, offering a convenient way to browse through their music collection.

## What problem does it solve

Spotify is renowned for its highly effective music recommendation algorithm, yet the user's library lacks methods for organizing its content. While it's easy to discover new music to add to your collection, it becomes increasingly challenging to keep track of it.

Unless you search through a long list of liked songs or artists when selecting something to listen to there's a risk of missing a significant portion of your content. While it's possible to organize songs into playlists, adding them all to playlists isn't a practical solution. Playlists can be organized into folders but unfortunately this feature is not extended to artists whom the user follows.

## In what way does it solve this problem

Virtual Music Library app retrieves liked songs and all tracks from a user's playlists through the Spotify API. It then consolidates them and organizes the collection into corresponding artists and genres folders. Users can play songs on Spotify by using the links provided within the app.

![My Remote Image](https://private-user-images.githubusercontent.com/112773165/310471953-823d24fe-d5b7-4f28-b3eb-45ccfff8ba76.PNG?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MDk3MjM4MjIsIm5iZiI6MTcwOTcyMzUyMiwicGF0aCI6Ii8xMTI3NzMxNjUvMzEwNDcxOTUzLTgyM2QyNGZlLWQ1YjctNGYyOC1iM2ViLTQ1Y2NmZmY4YmE3Ni5QTkc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjQwMzA2JTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI0MDMwNlQxMTEyMDJaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT1iYzgyM2U0YmRiOWM2OThhZGMzMjg3MDI4YmNiMDRmODBiZDA5YTNhNzU4N2YxYmYyMGMyOTgyYjAzYTdmMjlmJlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCZhY3Rvcl9pZD0wJmtleV9pZD0wJnJlcG9faWQ9MCJ9.Am96wh2khtK2uSOmD_KtjetJm_FlSMP3xuDY8VUU8As)

## Technologies used

* Python 3.9.7
* Flask 2.2.2
* SQLAlchemy 1.4.42
* PostgreSQL 16.1
* Jinja2 3.1.2
* Bootstrap 5.3.2

## API's used

Virtual Music Library app uses Spotify API (REST API) with OAuth 2.0 standard.
The authorization code flow used in the app is shown in the following Whimsical schema:

https://whimsical.com/vml-s-oauth-2-0-AK9SEvFpFv4AvF9nLMGuSb

## Whimsical mockup designs

Mockup designs for the app can be found in the following link:

https://whimsical.com/vml-mockups-3bYjFTHMP4NWSAbbUh7khH

## Project status
The project is currently in the development phase, with deployment scheduled in the near future.

Some of the improvements on the horizon:

* Google user authentication
* the same functionality for different music platforms
