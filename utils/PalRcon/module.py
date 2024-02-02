import utils.PalRcon.rcon
from utils.PalRcon.rcon.source import Client


class PalRcon:
    def __init__(self, rcon_addr, rcon_port, rcon_password):
        self.rcon_addr = rcon_addr
        self.rcon_port = rcon_port
        self.rcon_password = rcon_password

    def send_command(self, command):
        try:
            with Client(host=self.rcon_addr,
                        port=self.rcon_port,
                        passwd=self.rcon_password,
                        timeout=1) as pal_client:
                response = pal_client.run(command)
            return True, response
        except utils.PalRcon.rcon.exceptions.WrongPassword:
            return False, "RCON 密码错误，请检查密码是否正确"
        except utils.PalRcon.rcon.exceptions.SessionTimeout:
            return False, "会话超时，请检查服务端是否正常开启"
        except utils.PalRcon.rcon.exceptions.EmptyResponse:
            return False, "回复为空"
        except utils.PalRcon.rcon.exceptions.UserAbort:
            return False, "用户中断"
        except TimeoutError:
            return False, "连接超时，请检查服务端是否正常开启"
        except ConnectionResetError:
            return False, "远程主机强迫关闭了一个现有的连接，请重连RCON"
        except:
            return False, "未知错误，请联系开发人员"
