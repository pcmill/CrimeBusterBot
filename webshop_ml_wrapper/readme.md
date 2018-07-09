# ML Wrapper Service

## Starting service

To start the serve use `node server.js`
The current port the service will respond on is 4567.

## Creating a screenshot

Do a GET request to localhost:3456/mlwrapper, make sure that the 'u' param is filled.
An example of this: localhost:3456/mlwrapper/?u=http://example.com.
You will get something like this back:

{
    "success": true,
    "prediction": {
        "fake": 99.3,
        "good": 2.0,
        "normal": 0.2
    },
    "imageLocation": "app/routes/prediction/images/speelgoed-telefoon-6f40.png"
}

If you want to be sure that your URL does not break you can encode it. The python way to do this is apparently [docs](https://docs.python.org/3/library/urllib.parse.html#urllib.parse.quote)

Encoded the URL above looks like: http%3A%2F%2Fwww.speelgoed-telefoon.nl
