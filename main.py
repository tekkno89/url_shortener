from flask import Flask, request, jsonify
import hashlib
import os


app = Flask(__name__)
url_mapping = {}
shortener_domain = os.environ.get('SHORTENER_DOMAIN', 'localhost:5000')


def encode_url(original):
    url_hash = hashlib.sha256(original.encode()).hexdigest()[:8]
    url_mapping[url_hash] = original

    return url_hash


@app.post('/encode')
def encode():
    data = request.get_json()
    original_url = data.get('url')

    if not original_url:
        return jsonify({'error': 'Missing URL parameter'}), 400
    
    short_url = encode_url(original_url)

    return jsonify({'short_url': f'{shortener_domain}/{short_url}'}), 200


@app.get('/decode')
def decode():
    data = request.get_json()
    short_url = data.get('short_code')

    if not short_url:
        return jsonify({'error': 'missing URL parameter'}), 400
    
    if short_url in url_mapping:
        return jsonify({'original_url': f'{url_mapping[short_url]}'}), 200
    else:
        return jsonify({'error': 'URL not found', 'url': f'{short_url}'}), 404



if __name__ == '__main__':
    app.run(debug=True)