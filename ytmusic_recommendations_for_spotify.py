import streamlit as st
from collections import defaultdict
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from ytmusicapi import YTMusic
from fuzzywuzzy import fuzz

sofia_font = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Nunito:ital,wght@0,200..1000;1,200..1000&display=swap');
    html, body, [class*="css"] {
        font-family: 'Nunito', sans-serif;
    }
    </style>
    """
st.markdown(sofia_font, unsafe_allow_html=True)

# Add custom HTML for the header
st.markdown('<div class="header">S2Y</div>', unsafe_allow_html=True)
SPOTIPY_CLIENT_ID = '88877ed106c94563ae58b06033ae55ac'
SPOTIPY_CLIENT_SECRET = '47118fc261b542cdbf4f7784f7928423'
SPOTIPY_REDIRECT_URI = 'https://localhost:5000/callback'

scope = "playlist-read-private"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                               client_secret=SPOTIPY_CLIENT_SECRET,
                                               redirect_uri=SPOTIPY_REDIRECT_URI,
                                               scope=scope))

# YouTube Music API initialization
ytmusic = YTMusic()


# Function to get tracks from a Spotify playlist
def get_spotify_tracks(playlist_id):
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


# Function to get Spotify song's audio features
def get_audio_features(spotify_tracks):
    track_ids = [track['id'] for track in spotify_tracks]
    audio_features = sp.audio_features(track_ids)

    features_dict = {}
    for track, features in zip(spotify_tracks, audio_features):
        if features:
            features_dict[track['id']] = {
                'danceability': features['danceability'],
                'energy': features['energy'],
                'tempo': features['tempo'],
                'valence': features['valence']
            }
    return features_dict


# Function to get song recommendations from YouTube Music
def get_youtube_music_recommendations(song_name, artist_name):
    search_results = ytmusic.search(f'{song_name} {artist_name}', filter='songs')
    recommendations = []

    if search_results:
        for result in search_results[:10]:
            if 'artists' in result and result['artists']:
                artist = result['artists'][0]['name']
            else:
                artist = 'Unknown Artist'

            if fuzz.ratio(result['title'].lower(), song_name.lower()) > 90 and fuzz.ratio(artist.lower(),
                                                                                          artist_name.lower()) > 90:
                continue  # Skip exact matches

            thumbnail = result['thumbnails'][0]['url'] if 'thumbnails' in result else None

            recommendations.append({
                'title': result['title'],
                'artist': artist,
                'album': result.get('album', {}).get('name', 'N/A'),
                'thumbnail': thumbnail,
                'views': result.get('views', '0')  # You can use views as a proxy for popularity
            })

    # Sort recommendations by popularity (views)
    recommendations = sorted(recommendations, key=lambda x: int(x['views'].replace(',', '')), reverse=True)

    return recommendations[:5]  # Return top 5 recommendations


# Streamlit App Interface
st.title("YouTube Music Recommendations for Spotify")
st.markdown("""
    <style>
    .big-font {
        font-size:30px !important;
        color: #FFA500;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<p class="big-font">Unleash Music Across Platforms</p>', unsafe_allow_html=True)

# Input for Spotify playlist link
playlist_link = st.text_input('',placeholder="Paste your Spotify playlist link here...")

if playlist_link:
    try:
        # Extract the playlist ID from the URL
        SPOTIFY_PLAYLIST_ID = playlist_link.split("/")[-1].split("?")[0]

        # Fetch tracks from the Spotify playlist
        spotify_tracks = get_spotify_tracks(SPOTIFY_PLAYLIST_ID)
        if not spotify_tracks:
            st.write("No tracks found in the playlist.")
        else:
            # Get audio features of the Spotify tracks
            spotify_audio_features = get_audio_features(spotify_tracks)

            # Dictionary to store song counts
            song_count = defaultdict(int)
            playlist_songs = set(f"{track['name'].lower()} by {track['artist'].lower()}" for track in spotify_tracks)

            # Get YouTube Music recommendations for each song from the Spotify playlist
            for track in spotify_tracks:
                song_name = track['name']
                artist_name = track['artist']

                youtube_recommendations = get_youtube_music_recommendations(song_name, artist_name)

                for rec in youtube_recommendations:
                    rec_title = rec['title']
                    rec_artist = rec['artist']
                    rec_key = f"{rec_title.lower()} by {rec_artist.lower()}"

                    if rec_key not in playlist_songs:
                        song_count[rec_key] += 1  # Increment the count for this song

            # Zero out counts for songs that are in the playlist
            for track in spotify_tracks:
                song_key = f"{track['name'].lower()} by {track['artist'].lower()}"
                song_count[song_key] = 0

            # Sort the dictionary by value and get the top 10 new songs
            top_songs = sorted(song_count.items(), key=lambda item: item[1], reverse=True)[:10]

            # Display Top 10
            st.subheader("Youtube Recommendation")

            for song, count in top_songs:
                if count > 0:
                    # Extract the title and artist from the song key
                    song_title, song_artist = song.split(" by ")

                    # Search for the song on Spotify to get album cover and Spotify link
                    search_results = sp.search(q=f"{song_title} {song_artist}", type='track', limit=1)
                    if search_results['tracks']['items']:
                        track_info = search_results['tracks']['items'][0]
                        album_cover = track_info['album']['images'][0]['url']  # Get album cover URL
                        spotify_url = track_info['external_urls']['spotify']  # Get Spotify URL

                        # Use columns to display the album cover and the song info side by side
                        col1, col2 = st.columns([1, 4])
                        with col1:
                            # Display album cover
                            st.image(album_cover, width=100)

                        with col2:
                            # Display song information and link to Spotify
                            st.markdown(f"**[{song_title}]({spotify_url})** by {song_artist}")
                    else:
                        st.write(f"🎵 {song}")

    except Exception as e:
        st.write(f"Error: {e}")

# CSS for footer styling
footer = """
    <style>
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: transparent;
        color: white    ;
        text-align: right;
        padding: 10px;
        font-size: 16px;
    }
    </style>
    <div class="footer">
        <p>Made By: <b>Rajdeep Jadhav</b></p>
    </div>
    """
st.markdown(footer, unsafe_allow_html=True)
