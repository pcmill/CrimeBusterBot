# ML Wrapper Service
Yes another service ;)
This is basically a simple way to use the webshop_ml_serving and screenshot_service together to get a result.

## Starting the needed services
Start the screenshot service:
`cd screenshot_service` and then
`node server.js`. The service is now running on localhost:3456

Start the machine learning service:
`cd webshop_ml_serving` and then
`python app.py`. The service is now running on localhost:5000

## Starting service

To start the serve change directory back to the current folder and type `node server.js`
The current port the service will respond on is 4567.

## Creating a screenshot

Do a GET request to localhost:4567/mlwrapper, make sure that the 'u' param is filled.
An example of this: localhost:4567/mlwrapper/?u=http://example.com.
You will get something like this back:

{
    "success": true,
    "prediction": {
        "fake": 99.3,
        "good": 2.0,
        "normal": 0.2
    }
}

If you want to be sure that your URL does not break you can encode it. The python way to do this is apparently [docs](https://docs.python.org/3/library/urllib.parse.html#urllib.parse.quote)

Encoded the URL above looks like: http%3A%2F%2Fwww.speelgoed-telefoon.nl
