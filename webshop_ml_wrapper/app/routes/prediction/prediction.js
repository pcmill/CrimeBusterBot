const request = require('request');
const rp = require('request-promise-native');
const fs = require('fs');
const path = require('path');

function Prediction() {
    this.predict = async (website, res) => {
        if(website) {
            // Do a request to the screenshot service
            try {
                let url = encodeURIComponent(website);
                let screenshot = await rp(`http://localhost:3456/screenshot/?u=${url}`);
                screenshot = JSON.parse(screenshot);

                try {
                    // Doe de check op de ml service
                    await rp({
                        url: 'http://localhost:5000/predict',
                        headers: {
                            'content-type': 'multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW'
                        },
                        cache: false,
                        contentType: false,
                        processData: false,
                        async: true,
                        method: 'POST',
                        formData: {
                            file: {
                                value: fs.createReadStream(path.normalize(screenshot.imageLocation)),
                                options: {
                                    filename: path.normalize(screenshot.imageLocation),
                                    contentType: null
                                }
                            }
                        }
                    }, (error, response, body) => {
                        if (error) {
                            console.log(error);
                        } else {
                            // Delete the image from the folder
                            // fs.unlink(`${imageFolder}/${imageName}.${extension}`);
                            // Send back json from api
                            res.status(200);
                            res.send({ success: true, prediction: response.body.toString()});
                        }
                    });
                } catch(error) {
                   res.status(500);
                   res.send({ success: false, message: 'Something went wrong with the ml', error: error});
                }
            } catch(error) {
                res.status(500);
                res.send({ success: false, message: 'We could not get a screenshot'});
            }
        } else {
            res.status(500);
            res.send({ success: false, message: 'There is no URL defined'});
        }
    }
}

module.exports = new Prediction();