from flask import Flask, request, render_template, redirect, url_for, session
from collections import defaultdict
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from ytmusicapi import YTMusic
from fuzzywuzzy import fuzz
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Flask app initialization
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")  # Use the secret key from .env

# Spotify credentials
SPOTIPY_CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
SPOTIPY_REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI")

scope = "playlist-read-private"
sp_oauth = SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                        client_secret=SPOTIPY_CLIENT_SECRET,
                        redirect_uri=SPOTIPY_REDIRECT_URI,
                        scope=scope)

# YouTube Music API initialization
ytmusic = YTMusic()

# Function to get tracks from a Spotify playlist
def get_spotify_tracks(playlist_id, sp):
    results = sp.playlist_tracks(playlist_id)
    tracks = results.get('items', [])

    song_list = []
    if not tracks:
        return song_list

    for item in tracks:
        track = item.get('track')
        if track is None:
            continue
        song_name = track.get('name', 'Unknown Song')
        artist_name = track['artists'][0].get('name', 'Unknown Artist') if track.get('artists') else 'Unknown Artist'
        song_list.append({'name': song_name, 'artist': artist_name, 'id': track['id']})

    return song_list

# Function to get song recommendations from YouTube Music
def get_youtube_music_recommendations(song_name, artist_name, track_id):
    search_results = ytmusic.search(f'{song_name} {artist_name}', filter='songs')
    recommendations = []

    if search_results:
        for result in search_results[:10]:
            if 'artists' in result and result['artists']:
                artist = result['artists'][0]['name']
            else:
                artist = 'Unknown Artist'

            if fuzz.ratio(result['title'].lower(), song_name.lower()) > 90 and fuzz.ratio(artist.lower(), artist_name.lower()) > 90:
                continue  # Skip exact matches

            thumbnail = result['thumbnails'][0]['url'] if 'thumbnails' in result else None

            # Construct Spotify URL using the provided track_id
            spotify_url = f"https://open.spotify.com/track/{track_id}"

            recommendations.append({
                'title': result['title'],
                'artist': artist,
                'album': result.get('album', {}).get('name', 'N/A'),
                'thumbnail': thumbnail,
                'views': result.get('views', '0'),  # Use views as a proxy for popularity
                'spotify_url': spotify_url  # Add Spotify URL here
            })

    return recommendations

# Function to filter out duplicates and get top recommendations
def filter_and_get_top_recommendations(spotify_tracks, all_recommendations):
    recommendation_count = defaultdict(int)
    playlist_songs = set(f"{track['name'].lower()} by {track['artist'].lower()}" for track in spotify_tracks)

    for rec in all_recommendations:
        rec_key = f"{rec['title'].lower()} by {rec['artist'].lower()}"
        if rec_key not in playlist_songs:
            recommendation_count[rec_key] += 1

    # Get top 10 recommendations based on count
    top_recommendations = sorted(recommendation_count.items(), key=lambda x: x[1], reverse=True)[:10]

    # Prepare the final list of recommendations
    final_recommendations = []
    for rec_key, _ in top_recommendations:
        song_title, song_artist = rec_key.split(" by ")
        rec_info = next((rec for rec in all_recommendations if rec['title'].lower() == song_title and rec['artist'].lower() == song_artist), None)
        if rec_info:
            final_recommendations.append(rec_info)

    return final_recommendations

# Home route
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        playlist_link = request.form.get('playlist_link')

        if playlist_link:
            try:
                # Store the playlist link in the session
                session['playlist_link'] = playlist_link

                # Get Spotify authorization URL
                auth_url = sp_oauth.get_authorize_url()
                return redirect(auth_url)

            except Exception as e:
                return render_template('index.html', error=f"Error: {str(e)}")

    return render_template('index.html')

@app.route('/callback')
def callback():
    try:
        # Get the playlist link from the session
        playlist_link = session.get('playlist_link')
        if not playlist_link:
            return render_template('index.html', error="Playlist link not found in session.")

        session_token = sp_oauth.get_access_token(request.args['code'])
        sp = spotipy.Spotify(auth=session_token['access_token'])

        # Use the Spotify client to fetch tracks from the Spotify playlist
        SPOTIFY_PLAYLIST_ID = playlist_link.split("/")[-1].split("?")[0]
        spotify_tracks = get_spotify_tracks(SPOTIFY_PLAYLIST_ID, sp)

        if not spotify_tracks:
            return render_template('index.html', error="No tracks found in the playlist.")
        else:
            all_recommendations = []

            # Get YouTube Music recommendations for each song from the Spotify playlist
            for track in spotify_tracks:
                song_name = track['name']
                artist_name = track['artist']
                track_id = track['id']
                youtube_recommendations = get_youtube_music_recommendations(song_name, artist_name, track_id)
                all_recommendations.extend(youtube_recommendations)

            top_recommendations = filter_and_get_top_recommendations(spotify_tracks, all_recommendations)

            # Display only the top 10 recommendations
            return render_template('index.html', recommendations=top_recommendations)

    except Exception as e:
        return render_template('index.html', error=f"Error: {str(e)}")

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
