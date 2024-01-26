import os
import sys
import time

from utils.PalRcon.module import PalRcon

from utils import json_operation

module_path = os.path.split(sys.modules[__name__].__file__)[0]
config_path = os.path.join(module_path, r"../config.json")
config = json_operation.load_json(config_path)

rcon_addr = config["rcon_addr"]
rcon_port = config["rcon_port"]
rcon_password = config["rcon_password"]

command = "showplayers"

"""
pal_rcon = PalRcon(rcon_addr, rcon_port, rcon_password)
pal_rcon.connect()

result = pal_rcon.command(command)
print(result)"""


rcon_client = PalRcon(rcon_addr, rcon_port, rcon_password)
rcon_client.connect()
rcon_client.login()
print(True)
time.sleep(3)
print(rcon_client.check_connect())