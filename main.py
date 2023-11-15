from flask import Flask, request, jsonify
import hashlib
import os


app = Flask(__name__)
url_mapping = {}
shortener_domain = os.environ.get('SHORTENER_DOMAIN', 'localhost')


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

    return jsonify({'short_url': f'{shortener_domain}:5000/{short_url}'}), 200



if __name__ == '__main__':
    app.run(debug=True)