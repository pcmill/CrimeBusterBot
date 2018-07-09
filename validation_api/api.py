#!/usr/bin/env python3

from flask_api import FlaskAPI

from cert_check.cert_check import CertChecker


app = FlaskAPI(__name__)


@app.route("/<string:url>/", methods=['GET'])
def validate_certificate(url):
    return {'isvalid': CertChecker(url).check()}

if __name__ == "__main__":
    app.run(debug=True)
