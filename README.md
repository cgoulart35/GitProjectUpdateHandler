# Git Project Update Handler
Git Project Update Handler is a Flask API project to make the deployment process easier for working on my personal projects. The program executes scripts that each take down a docker container for a specific project, and then bring it back up after being rebuilt. Projects are rebuilt with the latest code pulled from its Git repository.

## Supported Projects
- [GBot](https://github.com/cgoulart35/GBot) - A Dockerized Python Discord bot, for fun!

## API

### <ins>Development</ins>
<details>
<summary>POST</summary>

*  Description:
    * `Triggers update scripts for the specified application.`
*  Syntax:
    * `POST - http://localhost:5005/GitProjectUpdateHandler`
*  Body:
    * `{"application": "GBot"}`
*  Response:
    * `{ "status": "success", "message": "Hi my name is Git!" }`
</details>