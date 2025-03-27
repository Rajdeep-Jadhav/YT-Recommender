# *Youtube Recommendations for spotify playlist*
## 📌 Project Overview

This Flask-based web application allows users to input a Spotify playlist URL and receive personalized YouTube Music recommendations based on the tracks in the playlist.

## ✨ Features

- Authenticate with Spotify
- Fetch tracks from a Spotify playlist
- Generate YouTube Music recommendations
- Filter and rank recommendations based on similarity and popularity

<div align="center">
  <img src="https://github.com/user-attachments/assets/03aa3e17-6326-4f1d-a068-c386773afd1a" alt="Project Image" width="750"/>
</div>

## 🛠 Prerequisites

- Python 3.8+
- Spotify Developer Account
- YouTube Music Account

## 🔧 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/spotify-youtube-recommender.git
cd spotify-youtube-recommender
```

### 2. Create Virtual Environment
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables
Create a `.env` file in the project root with the following:
```
SECRET_KEY=your_flask_secret_key
SPOTIPY_CLIENT_ID=your_spotify_client_id
SPOTIPY_CLIENT_SECRET=your_spotify_client_secret
SPOTIPY_REDIRECT_URI=http://localhost:5000/callback
```

### 5. Spotify Developer Setup
1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/)
2. Create a new application
3. Set Redirect URI to `http://localhost:5000/callback` and `http://localhost:5000`
4. Copy Client ID and Client Secret to `.env`

## 🚀 Running the Application for first time

```bash
python recommender.py
```

Navigate to `http://localhost:5000` in your web browser.

## 📝 How to Use

1. Enter a Spotify playlist URL
2. Click "Get Recommendations"
3. Authenticate with Spotify
4. View YouTube Music recommendations

## 🔍 Technologies Used

- Flask
- Spotipy (Spotify API Wrapper)
- YTMusicAPI
- FuzzyWuzzy (String Matching)




