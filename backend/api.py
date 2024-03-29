import os
import joblib
from dotenv import load_dotenv
from flask import Flask, request, jsonify
import requests
from flask_cors import CORS

load_dotenv()
app = Flask(__name__)
CORS(app)

#get authorization for spotify
AUTH_URL = 'https://accounts.spotify.com/api/token'
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
auth_response = requests.post(AUTH_URL, {
    'grant_type': 'client_credentials',
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET,
})

auth_response_data = auth_response.json()
access_token = auth_response_data['access_token']
headers = {
    'Authorization': 'Bearer {token}'.format(token=access_token)
}

#find song info method
def get_song_info(id):
    url = "https://api.spotify.com/v1/audio-features/" + id
    res = requests.get(url, headers=headers)
    res = res.json()
    song_info = [[res['danceability'], res['energy'], res['key'], res['loudness'], res['mode'], 
    res['speechiness'], res['acousticness'], res['instrumentalness'], res['liveness'], res['valence'],
    res['tempo'], res['duration_ms']/60000, res['time_signature']]]
    return song_info

#find genre method
def find_genre(id):
    song_features = get_song_info(id)
    #run ml model on song features:
    model = joblib.load('./model/genre-finder')
    genre_num = model.predict(song_features)
    genre_num = genre_num[0]
    genres = ["acoustic", "alternative", "blues", "bollywood", "country", "hip-hop", "indie", "instrumental", "metal", "pop", "rock"];
    genre = genres[genre_num]
    return genre


#get recommendations method
@app.route('/api/rec', methods=['GET'])
def get_recommendations():
    if 'id' in request.args:
        id = request.args['id']
    else:
        return "Error: No id field provided. Please specify an id."
    if 'genre' in request.args:
        genre = request.args['genre']
    else:
        return "Error: No gnre field provided. Please specify a genre."

    #get recommendations based on spotify api:
    url = "https://api.spotify.com/v1/recommendations?seed_genres=" + genre + "&seed_tracks=" + id 
    res = requests.get(url, headers=headers)
    res = res.json()
    rec_list = res['tracks'][0]['id'];
    print(rec_list)
    return jsonify({"rec": str(rec_list)})

@app.route('/api/genre', methods=['GET'])
def get_songbyid():
    if 'id' in request.args:
        id = request.args['id']
    else:
        return "Error: No id field provided. Please specify an id."

    genre = find_genre(id) # call function to find genre
    print(genre);
    return jsonify({"genre": str(genre)})

app.run()
