#!/usr/bin/env python3.7
from server import Server
import os.path

db = 'database.db'
put = os.getcwd()
print(put)
server = Server('*', 5555, db)
#try:
server.server_run()
#except(KeyboardInterrupt, SystemExit):
#   server.context.destroy()
