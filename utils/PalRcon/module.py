import socket
import struct
import re


class PalRcon:
    def __init__(self, host, port, password):
        self.host = host
        self.port = port
        self.password = password
        self.socket = None

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def connect(self):
        """
        Establishes a TCP connection to the RCON server.
        """
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(5)  # Set timeout to 5 seconds
        try:
            self.socket.connect((self.host, self.port))
            return True, "RCON服务器连接连接成功。"
        except ConnectionRefusedError:
            return False, "无法访问服务器，连接被拒绝。"

    def login(self):
        """
        Performs login/authentication with the RCON server using the provided password.
        """
        if self.socket:
            try:
                packet = struct.pack('<3i', 10 + len(self.password), 0, 3) + self.password.encode('utf-8') + b'\x00\x00'
                self.socket.send(packet)
                response = self.socket.recv(4096)
                self.handle_response(response)
                return True, "RCON服务器登录成功"
            except (socket.timeout, ConnectionAbortedError) as e:
                return False, "RCON服务器登录失败：" + str(e) + "。"

    def check_connect(self):
        """
        Checks the connection status and reconnects if necessary.
        """
        if not self.socket or self.socket.fileno() == -1:
            return False, "连接未建立或已关闭。"
        try:
            # 尝试向服务器发送一个空的请求来检测连接状态
            self.socket.send(b'\x00\x00\x00\x00')
            return True, "连接正常"
        except (socket.error, socket.timeout, ConnectionAbortedError):
            return False, "无法与服务器通信，服务器可能已关闭"

    def command(self, cmd):
        """
        Sends a command to the RCON server and processes the response.
        """
        try:
            packet = struct.pack('<3i', 10 + len(cmd), 0, 2) + cmd.encode('utf-8') + b'\x00\x00'
            self.socket.send(packet)
            response = self.socket.recv(4096)
            return self.handle_response_with_log(response)
        except (socket.timeout, ConnectionAbortedError) as e:
            print(f"Error during command execution: {e}")

    def handle_response(self, response):
        """
        Handles the response received from the RCON server.
        """
        if response:
            try:
                decoded_response = response.decode('utf-8')
                cleaned_text = re.sub(r'[^\x20-\x7E\u4E00-\u9FA5\n]', '', decoded_response)
                return cleaned_text
            except UnicodeDecodeError:
                print("Unable to decode response as UTF-8, printing hexadecimal representation:")
                print(response.hex())

    def handle_response_with_log(self, response):
        """
        Handles the response from the server and logs it with timestamp and command information.
        """
        if response:
            try:
                decoded_response = response.decode('utf-8').strip()
                cleaned_text = re.sub(r'[^\x20-\x7E\u4E00-\u9FA5\n]', '', decoded_response)
                print(cleaned_text)
                return cleaned_text
            except UnicodeDecodeError:
                hex_response = response.hex()
                print(f"Unable to decode response as UTF-8, printing hexadecimal representation:\n{hex_response}")

    def close(self):
        """
        Closes the socket connection to the RCON server.
        """
        if self.socket:
            self.socket.close()
