# S2Y: Spotify to YouTube Music Recommender

S2Y is a web-based application that allows users to input a Spotify playlist link and receive YouTube Music recommendations based on the tracks in that playlist. The app also displays detailed information about each Spotify track, including audio features like danceability, energy, tempo, and valence, along with album covers. It integrates Spotify and YouTube Music APIs to provide a seamless experience, all through an interactive Streamlit interface.

## Table of Contents
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Spotify API Setup](#spotify-api-setup)
- [First-Time Setup with Spotify Authentication](#first-time-setup-with-spotify-authentication)
- [Contributing](#contributing)
- [License](#license)

## Features
- **Spotify Playlist Analysis:** Input a Spotify playlist link to retrieve track details such as artist, album, and audio features.
- **Audio Features Display:** Show attributes like danceability, energy, tempo, and valence for each track in the playlist.
- **YouTube Music Recommendations:** Get song recommendations on YouTube Music based on the tracks in the Spotify playlist.
- **Album Art and Track Information:** Display the album cover and provide a Spotify link for each recommended track.
- **Interactive User Interface:** A user-friendly web app built with Streamlit, designed for easy navigation and interaction.

## Prerequisites
Before you begin, ensure you have the following:
- **Python 3.x**: Make sure Python is installed on your system. [Download Python](https://www.python.org/downloads/)
- **Spotify Developer Account**: Required for obtaining `client_id`, `client_secret`, and `redirect_uri`. Sign up [here](https://developer.spotify.com/) and create a new app to get the credentials.
- **YouTube Music API**: This app uses the `ytmusicapi` library for retrieving YouTube Music data.
- **Spotipy**: The app interacts with the Spotify API using the `Spotipy` library.

## Installation
1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/S2Y.git

2. **Navigate to Project Directory:**
   ```bash
   cd S2Y

3. **Install the Required Python Libraries:**
   ```bash  
   pip install -r requirements.txt
   
The requirements.txt file should include libraries such as spotipy, ytmusicapi, and streamlit.

## Spotify API Setup
To use this app, you need to create Spotify API credentials and configure a redirect URI.

### Steps to Create Spotify API Credentials
1. **Create a Spotify Developer Account:**
   - Go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/) and log in with your Spotify account. If you don’t have an account, create one.

2. **Create a New App:**
   - In the Dashboard, click on **Create an App**.
   - Provide an app name and description. For example:
     - **App Name:** Spotify to YouTube Music Recommender
     - **App Description:** An app that recommends YouTube Music songs based on a Spotify playlist.
   - Click **Create**.

3. **Get API Credentials:**
   - After creating the app, you'll see your **Client ID** and **Client Secret** on the app dashboard. These are necessary for the code to work.

4. **Set the Redirect URI:**
   - In your app settings, scroll down to the **Redirect URIs** section.
   - Add a URI that Spotify will use to redirect after authentication. For local development, you can use:
     ```
     http://localhost:8501/callback
     ```
## First-Time Setup with Spotify Authentication
If this is your first time running the app, follow these additional steps to authenticate with Spotify:

1. **Spotify Authentication:**
   - When you run the app for the first time, Spotify will prompt you to authenticate your app.
   - A new browser tab will open, where you must log in to Spotify and grant the necessary permissions.
   - After logging in and approving access, Spotify will redirect you to a page with a URL. This may show an error, which is expected.

2. **Provide the Redirect URL:**
   - Copy the URL from the browser's address bar after the redirection (even if it shows an error).
   - Paste it back into the terminal where Streamlit is running.

