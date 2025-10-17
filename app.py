"""
Roast My Spotify - Complete Web App
"""

from flask import Flask, request, redirect, jsonify, session, render_template_string
from flask_cors import CORS
import requests
import os
from collections import Counter
from dotenv import load_dotenv
load_dotenv()


app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-change-this')
CORS(app)

# Configuration
SPOTIFY_CLIENT_ID = os.environ.get('SPOTIFY_CLIENT_ID', 'your_spotify_client_id')
SPOTIFY_CLIENT_SECRET = os.environ.get('SPOTIFY_CLIENT_SECRET', 'your_spotify_client_secret')
ANTHROPIC_API_KEY = os.environ.get('ANTHROPIC_API_KEY', 'your_anthropic_api_key')
REDIRECT_URI = os.environ.get('REDIRECT_URI', 'http://localhost:5000/callback')



@app.route('/')
def home():
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Roast My Spotify 🔥</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 20px;
            }
            .container {
                background: white;
                border-radius: 20px;
                padding: 60px 40px;
                max-width: 500px;
                text-align: center;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            }
            h1 {
                font-size: 3em;
                margin-bottom: 20px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }
            p {
                color: #666;
                font-size: 1.2em;
                margin-bottom: 40px;
                line-height: 1.6;
            }
            .login-btn {
                background: #1DB954;
                color: white;
                border: none;
                padding: 18px 50px;
                font-size: 1.2em;
                border-radius: 50px;
                cursor: pointer;
                font-weight: bold;
                transition: all 0.3s;
                text-decoration: none;
                display: inline-block;
            }
            .login-btn:hover {
                background: #1ed760;
                transform: scale(1.05);
                box-shadow: 0 10px 30px rgba(29, 185, 84, 0.3);
            }
            .fire { font-size: 2em; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="fire">🔥</div>
            <h1>Roast My Spotify</h1>
            <p>Get a brutally honest, hilarious AI-powered analysis of your music taste</p>
            <a href="/login" class="login-btn">🎵 Log in with Spotify</a>
        </div>
    </body>
    </html>
    """
    return render_template_string(html)

@app.route('/login')
def login():
    scope = 'user-top-read user-read-recently-played'
    auth_url = f"https://accounts.spotify.com/authorize?client_id={SPOTIFY_CLIENT_ID}&response_type=code&redirect_uri={REDIRECT_URI}&scope={scope}"
    return redirect(auth_url)

@app.route('/callback')
def callback():
    code = request.args.get('code')
    if not code:
        return "Error: No authorization code", 400
    
    token_data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI,
        'client_id': SPOTIFY_CLIENT_ID,
        'client_secret': SPOTIFY_CLIENT_SECRET
    }
    
    token_response = requests.post('https://accounts.spotify.com/api/token', data=token_data)
    if token_response.status_code != 200:
        return f"Error: {token_response.text}", 400
    
    session['access_token'] = token_response.json()['access_token']
    return redirect('/analyze')

@app.route('/analyze')
def analyze():
    if not session.get('access_token'):
        return redirect('/login')
    
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Analyzing...</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 20px;
            }
            .container {
                background: white;
                border-radius: 20px;
                padding: 60px 40px;
                max-width: 800px;
                width: 100%;
                text-align: center;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            }
            .loader {
                border: 5px solid #f3f3f3;
                border-top: 5px solid #667eea;
                border-radius: 50%;
                width: 60px;
                height: 60px;
                animation: spin 1s linear infinite;
                margin: 30px auto;
            }
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
            h2 { color: #333; margin-bottom: 20px; font-size: 2em; }
            p { color: #666; line-height: 1.6; }
            #result {
                text-align: left;
                white-space: pre-wrap;
                line-height: 1.8;
                color: #333;
                font-size: 1.05em;
            }
            .home-btn {
                margin-top: 30px;
                background: #667eea;
                color: white;
                border: none;
                padding: 12px 30px;
                border-radius: 50px;
                cursor: pointer;
                font-size: 1em;
                text-decoration: none;
                display: inline-block;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="loader"></div>
            <h2>🔍 Analyzing your music taste...</h2>
            <p>This will take about 10 seconds...</p>
            <div id="result"></div>
            <a href="/" class="home-btn" id="homeBtn" style="display:none;">Roast Someone Else</a>
        </div>
        <script>
            fetch('/api/roast')
                .then(r => r.json())
                .then(data => {
                    document.querySelector('.loader').style.display = 'none';
                    document.querySelector('h2').textContent = '🔥 Your Roast';
                    document.querySelector('p').textContent = '';
                    document.getElementById('result').innerHTML = data.roast.replace(/\\n/g, '<br>');
                    document.getElementById('homeBtn').style.display = 'inline-block';
                })
                .catch(error => {
                    document.querySelector('.loader').style.display = 'none';
                    document.querySelector('h2').textContent = '❌ Error';
                    document.querySelector('p').textContent = error.toString();
                });
        </script>
    </body>
    </html>
    """
    return render_template_string(html)

@app.route('/api/roast')
def get_roast():
    if not session.get('access_token'):
        return jsonify({'error': 'Not authenticated'}), 401
    
    headers = {'Authorization': f"Bearer {session['access_token']}"}
    
    try:
        tracks_r = requests.get('https://api.spotify.com/v1/me/top/tracks',
                                headers=headers, params={'time_range': 'medium_term', 'limit': 50})
        tracks = tracks_r.json().get('items', [])
        
        artists_r = requests.get('https://api.spotify.com/v1/me/top/artists',
                                 headers=headers, params={'time_range': 'medium_term', 'limit': 50})
        artists = artists_r.json().get('items', [])
        
        prompt = f"""Roast this person's Spotify taste! Be funny, creative, insightful. Keep it under 500 words.

TOP 10 TRACKS:
"""
        for i, t in enumerate(tracks[:10], 1):
            prompt += f"{i}. \"{t['name']}\" by {', '.join(a['name'] for a in t['artists'])} ({t['album']['release_date'][:4]}, pop: {t['popularity']})\n"
        
        prompt += "\nTOP 10 ARTISTS:\n"
        for i, a in enumerate(artists[:10], 1):
            genres = ', '.join(a.get('genres', [])[:3]) or 'No genres'
            prompt += f"{i}. {a['name']} ({genres})\n"
        
        all_genres = [g for a in artists for g in a.get('genres', [])]
        genre_counts = Counter(all_genres).most_common(8)
        prompt += "\nTOP GENRES:\n"
        for g, c in genre_counts:
            prompt += f"• {g}: {c}\n"
        
        artist_counts = Counter()
        for t in tracks:
            for a in t['artists']:
                artist_counts[a['name']] += 1
        top_artist = artist_counts.most_common(1)[0] if artist_counts else None
        if top_artist:
            prompt += f"\nMost repeated: {top_artist[0]} ({top_artist[1]} tracks)\n"
        
        avg_pop = sum(t['popularity'] for t in tracks) / len(tracks) if tracks else 0
        prompt += f"Avg popularity: {avg_pop:.1f}/100\n"
        prompt += "\nGive: 1) Personality type 2) Roast 3) Patterns 4) Rating/10"
        
        # Call Anthropic API directly with requests
        anthropic_response = requests.post(
            'https://api.anthropic.com/v1/messages',
            headers={
                'x-api-key': ANTHROPIC_API_KEY,
                'anthropic-version': '2023-06-01',
                'content-type': 'application/json'
            },
            json={
                'model': 'claude-sonnet-4-20250514',
                'max_tokens': 2000,
                'messages': [{'role': 'user', 'content': prompt}]
            }
        )
        
        if anthropic_response.status_code != 200:
            return jsonify({'error': f'Anthropic API error: {anthropic_response.text}'}), 500
        
        roast = anthropic_response.json()['content'][0]['text']
        
        return jsonify({'roast': roast})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500



if __name__ == '__main__':
    app.run(debug=True, port=5000)
