from collections import defaultdict
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from ytmusicapi import YTMusic

# You need to replace these with your actual credentials from Spotify Developer and YouTube Music
SPOTIPY_CLIENT_ID = '88877ed106c94563ae58b06033ae55ac'
SPOTIPY_CLIENT_SECRET = '47118fc261b542cdbf4f7784f7928423'
SPOTIPY_REDIRECT_URI = 'https://localhost:5000/callback'

# Setup Spotify API authentication
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
        print("No tracks found in the playlist.")
        return song_list

    for item in tracks:
        track = item.get('track')

        if track is None:
            continue

        song_name = track.get('name', 'Unknown Song')
        artist_name = track['artists'][0].get('name', 'Unknown Artist') if track.get('artists') else 'Unknown Artist'

        song_list.append({'name': song_name, 'artist': artist_name})

    return song_list


# Function to get song recommendations from YouTube Music
def get_youtube_music_recommendations(song_name, artist_name):
    search_results = ytmusic.search(f'{song_name}', filter='songs')

    recommendations = []
    if search_results:
        for result in search_results[:20]:  # Fetch up to 20 results
            if 'artists' in result and result['artists']:
                artist = result['artists'][0]['name']
            else:
                artist = 'Unknown Artist'

            if result['title'].lower() == song_name.lower() and artist.lower() == artist_name.lower():
                continue

            recommendations.append({
                'title': result['title'],
                'artist': artist,
                'album': result.get('album', {}).get('name', 'N/A')
            })

    return recommendations


# Replace this with your Spotify Playlist ID
Link = input("Enter Playlist Link : ")
SPOTIFY_PLAYLIST_ID = Link
# Dictionary to store song counts
song_count = defaultdict(int)

# Fetching songs from the Spotify playlist
spotify_tracks = get_spotify_tracks(SPOTIFY_PLAYLIST_ID)

# Set to track the playlist songs for exclusion
playlist_songs = set(f"{track['name'].lower()} by {track['artist'].lower()}" for track in spotify_tracks)

# Get YouTube Music recommendations for each song from the Spotify playlist
for track in spotify_tracks:
    song_name = track['name']
    artist_name = track['artist']

    #print(f"\nSpotify Song: {song_name} by {artist_name}")
    #print("YouTube Music Recommendations:")

    youtube_recommendations = get_youtube_music_recommendations(song_name, artist_name)

    for rec in youtube_recommendations:
        rec_title = rec['title']
        rec_artist = rec['artist']
        rec_key = f"{rec_title.lower()} by {rec_artist.lower()}"

        if rec_key not in playlist_songs:
            song_count[rec_key] += 1  # Increment the count for this song

        #print(f"- {rec_title} by {rec_artist} (Album: {rec['album']})")

# Zero out counts for songs that are in the playlist
for track in spotify_tracks:
    song_key = f"{track['name'].lower()} by {track['artist'].lower()}"
    song_count[song_key] = 0

# Sort the dictionary by value and get the top 10 new songs
top_songs = sorted(song_count.items(), key=lambda item: item[1], reverse=True)[:10]

print("\nTop 10 New Recommended Songs (not in the playlist):")
for song, count in top_songs:
    if count > 0:  # Only display songs that are not in the playlist
        print(f"{song}: {count} times")
