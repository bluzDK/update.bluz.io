from particle_api import *
from api_version import version as api_version
import time
import json
import uuid
import urllib
import os

from flask import Flask, request, session, g, url_for, request, jsonify

# create our app
app = Flask(__name__)

# enable CORS on everything
from flask_cors import CORS
CORS(app)

# helper function to get the current time in millis()
current_milli_time = lambda: int(round(time.time() * 1000))

# url to send commmands to
url = 'https://api.particle.io'

# will return 400 when called
@app.errorhandler(400)
def bad_request(error=None):
        """
        Handle 400 cases
        :param error: String, the error to return
        :return:
        """
        message = {
            'status': 400,
            'message': 'BadRequest: ' + request.url + (". Error: " + error if error is not None else ''),
        }
        resp = jsonify(message)
        resp.status_code = 400

        return resp

# will return 500 when called
@app.errorhandler(500)
def internal_error(error=None):
        """
        Handle 500 cases
        :param error: String, the error to return
        :return:
        """
        message = {
            'status': 500,
            'message': 'ServerError: ' + request.url + (". Error: " + error if error is not None else ''),
        }
        resp = jsonify(message)
        resp.status_code = 500

        return resp

# Routes
# ------------------------------------------------------------------------------
@app.route('/version')
def version():
    return json.dumps({'version': api_version})

@app.route('/update', methods=['POST'])
def update():
    try:
        params = get_payload(request)

        device = params['device']
        access_token = params['accessToken']
        urls = params["files"]

        env = "staging" if request.base_url.startswith("https://staging.particle.io") else "production"
    except:
        return bad_request("Invalid parameters")

    try:
        dir = create_dir()

        for url in urls:
            # download file
            local_file = dir+'/'+filename_from_url(url)
            urllib.urlretrieve(url, local_file)

            #call particle flash for this file and device
            particle = ParticleAPI(env)
            started = particle.particle_flash(device, local_file, access_token)

            if not started:
                raise Exception("Unable to start update")

            os.rm(local_file)

        # finally, delete the directory
        os.rmdir(dir)
    except Exception as ex:
        return internal_error(ex.message)

    return json.dumps({})

# Helper functions
# ------------------------------------------------------------------------------
def get_payload(request):

    if request.method == 'POST':
        # if POST, the data may be in the data array as json or form, depending on how it was handed in
        # Postman seems to hand it in as json while others seem to hand it in through form data
        data = request.get_json(force=True, silent=True)
        return data if data is not None else request.form
    else:
        return request.args

def create_dir():
    path = '/tmp/'+str(uuid.uuid4())
    if not os.path.exists(path):
        os.makedirs(path)
    return path

def filename_from_url(url):
    return url.split("/")[-1]

# Main
# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run()