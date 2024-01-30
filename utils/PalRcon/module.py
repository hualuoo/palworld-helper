import rcon
from rcon.source.proto import Packet
from rcon.source import Client


class PalClient(Client):
    def run(self, command: str, *args: str, encoding: str = "utf-8") -> str:
        """Run a command."""
        request = Packet.make_command(command, *args, encoding=encoding)
        response = self.communicate(request)
        return response.payload.decode(encoding)


class PalRcon:
    def __init__(self, rcon_addr, rcon_port, rcon_password):
        self.rcon_addr = rcon_addr
        self.rcon_port = rcon_port
        self.rcon_password = rcon_password

    def send_command(self, command):
        try:
            with PalClient(host=self.rcon_addr,
                           port=self.rcon_port,
                           passwd=self.rcon_password,
                           timeout=1) as pal_client:
                response = pal_client.run(command)
            return True, response
        except rcon.exceptions.WrongPassword:
            return False, "RCON 密码错误，请检查密码是否正确"
        except rcon.exceptions.SessionTimeout:
            return False, "会话超时，请检查服务端是否正常开启"
        except rcon.exceptions.EmptyResponse:
            return False, "回复为空"
        except rcon.exceptions.UserAbort:
            return False, "用户中断"
        except TimeoutError:
            return False, "连接超时，请检查服务端是否正常开启"
        except ConnectionResetError:
            return False, "远程主机强迫关闭了一个现有的连接，请重连RCON"
        except:
            return False, "未知错误，请联系开发人员"

