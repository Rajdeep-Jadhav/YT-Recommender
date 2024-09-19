# S2Y
#Overview
This project allows users to input a Spotify playlist link and receive YouTube Music recommendations based on the songs in that playlist. The app also showcases the Spotify track details and corresponding album covers. It integrates Spotify and YouTube Music APIs to retrieve data and present it in an interactive Streamlit web interface.

#Features
Input a Spotify playlist link and retrieve track details from Spotify.
Display audio features like danceability, energy, tempo, and valence for each track.
Get YouTube Music song recommendations based on the songs in the Spotify playlist.
Show the album cover and Spotify link for recommended songs.
Interactive, user-friendly UI built with Streamlit.

#Prerequisites
Before you begin, ensure you have the following installed:
Python 3.x: Make sure Python is installed on your system. You can download it from python.org.
Spotify Developer Account: You'll need a Spotify Developer account to obtain client_id, client_secret, and redirect_uri.
Visit Spotify for Developers and create a new app to get the credentials.
YouTube Music API: The app uses the ytmusicapi Python library for YouTube Music data.
Spotipy: This project uses the Spotipy library for interacting with the Spotify API.

#***Spotify API Setup***
To use this app, you will need to create your own Spotify API credentials and configure a redirect URI.

#Steps to Create Spotify API Credentials:
Create a Spotify Developer Account:
Go to the Spotify Developer Dashboard and log in with your Spotify account.
If you don’t have a Spotify account, you will need to create one.

Create a New App:
In the Dashboard, click on Create an App.
Give your app a name and description. For example:
App Name: Spotify to YouTube Music Recommender
App Description: An app that recommends YouTube Music songs based on a Spotify playlist.
Click Create.

Get API Credentials:
After creating the app, you'll see your Client ID and Client Secret on the app dashboard. You will need these for the code to work.

Set the Redirect URI:
In your app settings, scroll down to the Redirect URIs section.
Add a URI that Spotify will use to redirect after authentication. For local development, you can use something like:

```
http://localhost:8501/callback
```


#First-Time Setup with Spotify Authentication
If this is your first time running the app, follow these additional steps to authenticate with Spotify:

***Run the Streamlit App: Start the Streamlit app via the terminal using the following command:***
```
streamlit run app.py
```
***Spotify Authentication:***
When you run the app for the first time, Spotify will ask you to authenticate your app.
After starting the app, a new browser tab will open where you will need to log in to Spotify and grant the necessary permissions.
Once you log in and approve access, Spotify will redirect you to a page with a URL that may show an error (this is expected).

***Provide the Redirect URL:***
Copy the URL from the browser's address bar after the redirection (even if it shows an error) and paste it back into the terminal where Streamlit is running.

