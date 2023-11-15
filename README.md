# url_shortener
Simple Python URL Shortener Built on Flask

## Summary
This app runs with Flask and exposes 3 endpoints: `/encode`, `/decode`, `/<short_code.`
For more information about the endpoints and how to use them, see the `Usage` section

## Installation
This app requires:
- python 3.11
- pipenv

### Pipenv Setup
To install pipenv, run the following query:
```
pip install pipenv
```

Before running the app you will need to install the required packages. You can use the following command once you have pipenv installed:
```
pipenv install --ignore-pipfile
```

## Usage
All endpoints require JSON content and return JSON, with the exception of the `/<short_code>` endpoint. The `/encode` and `/decode` endpoints have a rate limit of 2 queries per second.

You can change the domain URL that the endpoints are tied to by setting the `SHORTENER_DOMAIN` Environment Variable. It will default to `http://localhost:5000` if it is not set.

You can also set the Rate Limit window by setting the `DEFAULT_RATE_LIMIT` Environment Variable. It will default to 2 queries per second, if not set.

### Running the App
You will need to be in the virtualenv created by pipenv. You can do so by running `pipenv shell`.

To run the app, you only need to run the following command, assuming you are in the root of the repo `python shortener/main.py`. This will run the application on your localhost and can be reached at `http://localhost:5000`

### Encode Endpoint
`/encode` requires a data object that contains a URL - `{'url': 'google.com'}`. The endpoint only accepts the `POST` method. This endpoint will return a JSON object with a short code and short url that you can use with the `/dedcode` and `/<short_code>` endpoints. This endpoint will return a JSON object that looks like the following: `{'short_url': 'http://localhost/d4c9d902', 'short_code': 'd4c9d902'}`

### Decode Endpoint
`/decode` requires a short_code that you receive from the `encode` endpoint - `{'short_code': 'd4c9d902'}`. This endpoint only accepts the `GET` method. If the short code exists, it will return the original URL that was shortened - `{'original_url': 'google.com'}`

### Redirect Endpoint
`/<short_code>` requires a valid short code that has been generated via the `/encode` endpoint. If the short code is valid, you will be redirected to the original endpoint that was created for that code. Example in a browser - http://localhost:5000/d4c9d902. By inputing the following in your browser, you should be redirected to google.com, assuming you created the short url for google.com

## Testing
This application uses pytest for testing the application. It will test each of the endpoints. You can run the tests by running the following command from the root of the repo:
```
pytest
```