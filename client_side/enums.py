import os


class Intervals:
    POLL_REFRESH_INTERVAL = 1
    HEARTBEAT_INTERVAL = 30
    LOGIN_POLL_INTERVAL = 5000


class Host:
    HOST = 'dummy'
    LOGIN_PORT = os.getenv('HOST', '5557')
    PORT = os.getenv('HOST', '5555')  # TODO make it an actual system value
