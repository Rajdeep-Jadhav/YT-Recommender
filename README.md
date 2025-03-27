# Spotify Playlist YouTube Music Recommender

## 📌 Project Overview

This Flask-based web application allows users to input a Spotify playlist URL and receive personalized YouTube Music recommendations based on the tracks in the playlist.

## ✨ Features

- Authenticate with Spotify
- Fetch tracks from a Spotify playlist
- Generate YouTube Music recommendations
- Filter and rank recommendations based on similarity and popularity

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
pip install flask spotipy ytmusicapi fuzzywuzzy python-dotenv
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

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## ⚠️ Limitations

- Requires active internet connection
- Recommendation accuracy depends on track metadata
- Limited by Spotify and YouTube Music API constraints

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

## 🐛 Issues

Report issues at [GitHub Issues](https://github.com/yourusername/spotify-youtube-recommender/issues)

## 📞 Contact

Your Name - your.email@example.com

Project Link: [https://github.com/yourusername/spotify-youtube-recommender](https://github.com/yourusername/spotify-youtube-recommender)
