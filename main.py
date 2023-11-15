from flask import Flask, request, jsonify, redirect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import hashlib
import os


shortener_domain = os.environ.get('SHORTENER_DOMAIN', 'localhost:5000')
default_rate_limit = os.environ.get('DEFAULT_RATE_LIMIT', '2 per second')

app = Flask(__name__)
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=[default_rate_limit]
)
url_mapping = {}


def encode_url(original):
    url_hash = hashlib.sha256(original.encode()).hexdigest()[:8]
    url_mapping[url_hash] = original

    return url_hash


@app.post('/encode')
@limiter.limit(default_rate_limit)
def encode():
    data = request.get_json()
    original_url = data.get('url')

    if not original_url:
        return jsonify({'error': 'Missing URL parameter'}), 400
    
    short_url = encode_url(original_url)

    return jsonify({'short_url': f'{shortener_domain}/{short_url}'}), 200


@app.get('/decode')
@limiter.limit(default_rate_limit)
def decode():
    data = request.get_json()
    short_code = data.get('short_code')

    if not short_code:
        return jsonify({'error': 'missing URL parameter'}), 400
    
    if short_code in url_mapping:
        return jsonify({'original_url': f'{url_mapping[short_code]}'}), 200
    else:
        return jsonify({'error': 'URL not found', 'url': f'{short_code}'}), 404


@app.get('/<short_code>')
@limiter.limit(default_rate_limit)
def redirect_to(short_code):
    if short_code in url_mapping:
        url = url_mapping[short_code]
        return redirect(url, code=302)
    else:
        return jsonify({'error': 'URL not found', 'url': f'{short_code}'}), 404


if __name__ == '__main__':
    app.run()