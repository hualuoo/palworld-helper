from utils.PalRcon.module import PalRcon

rcon_addr = "127.0.0.1"
rcon_port = 25575
rcon_password = "DpSEqo1u5CfQmiY"

pal_rcon = PalRcon(rcon_addr, rcon_port, rcon_password)
flag, message = pal_rcon.send_command("showplayers")
print(flag, message)
flag, message = pal_rcon.send_command("info")
print(flag, message)
