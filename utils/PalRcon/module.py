import utils.PalRcon.rcon
from utils.PalRcon.rcon.source import Client


class PalRcon:
    def __init__(self, rcon_addr, rcon_port, rcon_password):
        self.rcon_addr = rcon_addr
        self.rcon_port = rcon_port
        self.rcon_password = rcon_password

    def send_command(self, command):

            with Client(host=self.rcon_addr,
                        port=self.rcon_port,
                        passwd=self.rcon_password,
                        timeout=1) as pal_client:
                response = pal_client.run(command)
            return True, response


