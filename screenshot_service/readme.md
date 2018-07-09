# Screenshot service

## Starting service

To start the serve use `node server.js`
The current port the service will respond on is 3456.

## Creating a screenshot

Do a GET request to localhost:3456/screenshot, make sure that the 'u' param is filled.
An example of this: localhost:3456/screenshot/?u=http://example.com.
You will get something like this back:

{
    "success": true,
    "imageName": "speelgoed-telefoon-6f40.png",
    "imageLocation": "app/routes/screenshot/temp/speelgoed-telefoon-6f40.png"
}

If you want to be sure that your URL does not break you can encode it. The python way to do this is apparently [docs](https://docs.python.org/3/library/urllib.parse.html#urllib.parse.quote)

Encoded the URL above looks like: http%3A%2F%2Fwww.speelgoed-telefoon.nl
