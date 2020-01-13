**#Library request**


There are 2 endpoints exposed here:

/request
and 
/request/<request_id>

Pre-requiste:
git and python3 and libraries listed in requirements.txt

Steps to run

`git clone https://github.com/Lionelkris/liquidnet-devtest.git`

`python3 -m unittest discover`

you can also start the app by running the below command:

`python3 run.py`

For docker

`docker-compose build`

`docker-compose up `

Data population is done via app start up from a script "create_book()". Only data for Books needs to be populated.

For user, on each request if the user exists in the system we go ahead with the request OR we will create it.

Please note that the application is running on port 8000

sample end point : http://127.0.0.1:8000/request

