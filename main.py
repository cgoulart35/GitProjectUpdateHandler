#region IMPORTS
import pathlib
import os
import threading
import asyncio
import git
import json
from flask import Flask, request, abort
from flask_restful import Api, Resource
from flask_cors import CORS
#endregion

# get parent directory
parentDir = str(pathlib.Path(__file__).parent.parent.absolute()).replace("\\",'/')

# define supported projects
supported_projects = ["GBot"]
async def callUpdateScript(name):
    await asyncio.sleep(10)
    os.system(parentDir + "/GitProjectUpdateHandler/scripts/Update" + name + ".sh")

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
                msg = g.pull()

                if msg != "Already up to date.":
                    def entryFunction(name):
                        asyncio.run(callUpdateScript(name))

                    threading.Thread(target = entryFunction, args = (projectName,)).start()

                return { "status": "success", "message": msg }

        except:
            abort(400, "Error: Unhandled exception.")

api.add_resource(GitProjectUpdateHandler, '/GitProjectUpdateHandler/')
app.run(host='0.0.0.0', port=5005, debug=True, use_reloader=False)