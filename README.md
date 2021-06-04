## Installation

`docker build -t crypto_final .`

`docker run -d -p 8888:3306 --name crypto_final -e MYSQL_ROOT_PASSWORD=supersecret crypto_final`

`pip3 install -r requirements.txt`

## Usage

`python3 server.py`

`python3 ballot_client.py`

`python3 vote_client.py`

`python3 check_client.py`
