
# WebSockets Security

In this repo 3 services are available:
* Python WebSocket Server
* **XSS Vulnerable** WebSocket Client
* **XSS Secure** WebSocket Client

## Installation

Clone this repo with `git clone https://github.com/christianfe/WebSocket-ICT`

### Python WebSocket Server

* Go inside project folder with `cd API`
* Install dependencies with `pip install -r requirements.txt`
* Run `python server.py`

### XSS Vulnerable WebSocket Client

* Go inside project folder with `cd vuln-client`
* Install Flash `pip install Flask`
* Install dependencies with `pip install -r requirements.txt`
* Run `flask run` or `python -m flask run` in case of error
* Visit http://localhost:8800

### XSS Secure WebSocket Client

* Go inside project folder with `cd secure-client`
* Install project with `npm install`
* Run `ng serve`
* Visit http://localhost:4200


## Project info

Author: [Christian Felicione](https://github.com/christianfe/)

Code written to provide an example of the Web Sockets XSS vulnerability
