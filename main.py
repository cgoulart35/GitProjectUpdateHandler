#region IMPORTS
import pathlib
import os
import logging
import time
import threading
import asyncio
import git
import json
from urllib.error import URLError
from urllib.request import urlopen
from flask import Flask, request, abort
from flask_restful import Api, Resource
from flask_cors import CORS
#endregion

# get parent directory
parentDir = str(pathlib.Path(__file__).parent.parent.absolute()).replace("\\",'/')

if not os.path.exists(parentDir + '/GitProjectUpdateHandler/Logs'):
    os.mkdir(parentDir + '/GitProjectUpdateHandler/Logs')
LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
file_handler = logging.FileHandler(filename = parentDir + '/GitProjectUpdateHandler/Logs/GitProjectUpdateHandler.log')
logging.basicConfig(handlers = [file_handler],
                    format = LOG_FORMAT,
                    level = logging.INFO)
logger = logging.getLogger()

def waitForInternet():
    while True:
        try:
            urlopen('http://google.com')
            logger.info('Internet connection established.')
            return
        except URLError:
            time.sleep(2)
            logger.info('Waiting for internet connection...')
            pass

# don't start update handler API until internet connection established
waitForInternet()

# define supported projects
supported_projects = ["GBot"]
async def callUpdateScript(name):
    await asyncio.sleep(10)
    os.system(parentDir + "/GitProjectUpdateHandler/Scripts/Update" + name + ".sh")

# start flask API
app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})
api = Api(app)

class GitProjectUpdateHandler(Resource):
    def post(self):
        try:
            data = request.get_data()
            value = json.loads(data)

            if "application" in value and value["application"] in supported_projects:
                projectName = value["application"]
                projectDirectory = parentDir + "/" + projectName
                g = git.cmd.Git(projectDirectory)

                # reset any current changes
                g.reset('--hard')
                # pull latest code
                msg = g.pull()
                # stage property files and rebuild the docker container
                if msg != "Already up to date.":
                    def entryFunction(name):
                        asyncio.run(callUpdateScript(name))

                    threading.Thread(target = entryFunction, args = (projectName,)).start()

                responseObj = { "status": "success", "message": msg }
                logger.info(json.dumps({ "application": projectName, "reponse": responseObj }))
                return responseObj

            responseObj = { "status": "error", "message": "Error: Invalid request." }
            logger.info(json.dumps({ "application": projectName, "reponse": responseObj }))
            return responseObj
        except:
            abort(400, "Error: Unhandled exception.")

api.add_resource(GitProjectUpdateHandler, '/GitProjectUpdateHandler/')
app.run(host='0.0.0.0', port=5005, debug=True, use_reloader=False)