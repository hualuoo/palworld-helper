from utils.PalRcon.module import PalRcon
from rcon.source import rcon

rcon_addr = "127.0.0.1"
rcon_port = 25575
rcon_password = "8b1JrmCL5VxwG"

pal_rcon = PalRcon(rcon_addr, rcon_port, rcon_password)
flag, message = pal_rcon.send_command(" ")
print(flag, message)
