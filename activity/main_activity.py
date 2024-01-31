import os
import sys
import subprocess
import shutil
import time
from datetime import datetime, timedelta

from PyQt5.uic import loadUi
from PyQt5.QtGui import QIcon, QTextCharFormat, QColor, QTextCursor
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QFileDialog, QTableWidgetItem, QMenu, QAction, QInputDialog, QStatusBar
import psutil
import pyperclip

from activity import world_settings_activity
from utils import json_operation, random_password, settings_file_operation
from utils.PalRcon.module import PalRcon
import setting


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.module_path = os.path.split(sys.modules[__name__].__file__)[0]
        self.config_path = os.path.join(sys.argv[0], r"../config.json")
        self.config = json_operation.load_json(self.config_path)
        self.rcon_connect_flag = False
        self.pal_rcon = None
        self.server_run_flag = False
        self.server_run_time = datetime.now()
        self.last_auto_backup_time = datetime.now()
        self.player_list = []
        self.palserver_settings_path = None
        self.option_settings_dict = {}
        self.initUi()

    def initUi(self):
        loadUi(os.path.join(self.module_path, r"../ui/main.ui"), self)
        if setting.publicity_ad:
            self.setWindowTitle("幻兽帕鲁开服助手 - PalServer Helper " + setting.version + " - " + setting.publicity_ad)
        else:
            self.setWindowTitle("幻兽帕鲁开服助手 - PalServer Helper " + setting.version)
        self.setFixedSize(1450, 730)
        self.setWindowIcon(QIcon(os.path.join(self.module_path, r"../resource/favicon.ico")))
        self.table_widget_player_list.setColumnWidth(0, 80)
        self.table_widget_player_list.setColumnWidth(1, 100)
        self.table_widget_player_list.setColumnWidth(2, 130)

        if setting.status_bar_show_flag:
            status_bar = QStatusBar()
            self.setStatusBar(status_bar)
            status_bar.showMessage(setting.status_bar_message)

        self.check_palserver_path()

        if "game_port" in self.config:
            self.line_edit_game_port.setText(str(self.config["game_port"]))
        if "game_publicport" in self.config:
            self.line_edit_game_publicport.setText(str(self.config["game_publicport"]))
        if "game_player_limit" in self.config:
            self.line_edit_game_player_limit.setText(str(self.config["game_player_limit"]))

        if "rcon_addr" in self.config:
            self.line_edit_rcon_addr.setText(self.config["rcon_addr"])
        if "rcon_port" in self.config:
            self.line_edit_rcon_port.setText(str(self.config["rcon_port"]))
        if "rcon_password" in self.config:
            self.line_edit_rcon_password.setText(self.config["rcon_password"])

        if "crash_detection_flag" in self.config:
            self.check_box_crash_detection.setChecked(self.config["crash_detection_flag"])
            if self.config["crash_detection_flag"]:
                self.check_box_crash_detection_click(True)
        if "auto_restart_time_limit" in self.config:
            self.line_edit_auto_restart_time_limit.setText(str(self.config["auto_restart_time_limit"]))
        if "auto_restart_flag" in self.config:
            self.check_box_auto_restart.setChecked(self.config["auto_restart_flag"])
            if self.config["auto_restart_flag"]:
                self.check_box_auto_restart_click(True)
        if "auto_restart_player_limit" in self.config:
            self.line_edit_auto_restart_player_limit.setText(str(self.config["auto_restart_player_limit"]))
        if "auto_restart_player_flag" in self.config:
            self.check_box_auto_restart_player.setChecked(self.config["auto_restart_player_flag"])
            if self.config["auto_restart_player_flag"]:
                self.check_box_auto_restart_player_click(True)

        if "auto_backup_time_limit" in self.config:
            self.line_edit_auto_backup_time_limit.setText(str(self.config["auto_backup_time_limit"]))
        if "backup_dir_path" in self.config:
            if os.path.isdir(self.config["backup_dir_path"]):
                self.line_edit_backup_path.setText(self.config["backup_dir_path"])
                self.check_box_auto_backup.setEnabled(True)
                self.line_edit_auto_backup_time_limit.setEnabled(True)
                if "auto_backup_flag" in self.config:
                    self.check_box_auto_backup.setChecked(self.config["auto_backup_flag"])
                    if self.config["auto_backup_flag"]:
                        self.check_box_auto_backup_click(True)
            else:
                self.config.pop("backup_dir_path")
                self.save_config_json()

        if "launch_options_info" in self.config:
            self.line_edit_launch_options.setText(self.config["launch_options_info"])
        if "launch_options_flag" in self.config:
            self.check_box_launch_options.setChecked(self.config["launch_options_flag"])
            self.line_edit_launch_options.setEnabled(not self.config["launch_options_flag"])

        self.timed_detection_timer_1000 = QTimer(self)
        self.timed_detection_timer_1000.timeout.connect(self.timed_detection_1000)
        self.timed_detection_timer_1000.start(1000)
        self.timed_detection_timer_5000 = QTimer(self)
        self.timed_detection_timer_5000.timeout.connect(self.timed_detection_5000)
        self.timed_detection_timer_5000.start(5000)
        self.timed_detection_timer_60000 = QTimer(self)
        self.timed_detection_timer_60000.timeout.connect(self.timed_detection_5000)
        self.timed_detection_timer_60000.start(60000)

    def timed_detection_1000(self):
        if self.server_run_flag:
            if "palserver_pid" in self.config:
                if psutil.pid_exists(self.config["palserver_pid"]) is False:
                    self.server_run_flag = False
                    if self.config["crash_detection_flag"]:
                        self.text_browser_rcon_server_notice("client_error", "检测到服务端崩溃，开始重启 ！")
                        self.button_game_start_click()
        else:
            if "palserver_pid" in self.config:
                if psutil.pid_exists(self.config["palserver_pid"]):
                    self.server_run_flag = True

        if self.server_run_flag:
            self.label_server_status.setText("正在运行")
            self.label_server_status.setStyleSheet("color:green")
        else:
            self.label_server_status.setText("已停止")
            self.label_server_status.setStyleSheet("color:red")
        self.button_game_start.setEnabled(not self.server_run_flag)
        self.button_game_stop.setEnabled(self.server_run_flag)
        self.button_game_restart.setEnabled(self.server_run_flag)
        self.button_game_kill.setEnabled(self.server_run_flag)
        self.text_edit_server_name.setEnabled(not self.server_run_flag)
        self.text_edit_server_description.setEnabled(not self.server_run_flag)
        self.text_edit_server_description.setEnabled(not self.server_run_flag)
        self.button_edit_server_name.setEnabled(not self.server_run_flag)

        self.line_edit_command.setEnabled(self.rcon_connect_flag)
        self.button_send_command.setEnabled(self.rcon_connect_flag)
        self.button_countdown_stop.setEnabled(self.rcon_connect_flag)
        self.button_broadcast.setEnabled(self.rcon_connect_flag)

        if self.config["auto_restart_flag"] and self.server_run_flag:
            if self.server_run_time + timedelta(seconds=self.config["auto_restart_time_limit"]) < datetime.now():
                if self.config["auto_restart_player_flag"]:
                    if len(self.player_list) <= self.config["auto_restart_player_limit"]:
                        self.text_browser_rcon_server_notice("client_message", "检测到符合服务器自动重启条件，开始重启！")
                        self.button_game_restart_click()
                else:
                    self.text_browser_rcon_server_notice("client_message", "检测到符合服务器自动重启条件，开始重启！")
                    self.button_game_restart_click()

        if self.config["auto_backup_flag"]:
            if self.last_auto_backup_time + timedelta(seconds=self.config["auto_backup_time_limit"]) < datetime.now():
                self.text_browser_rcon_server_notice("client_message", "检测到符合服务器自动备份标准，开始备份！")
                old_dir_path = os.path.join(self.config["palserver_path"], r"../Pal/Saved/")
                new_dir_path = os.path.join(self.config["backup_dir_path"], datetime.now().strftime("%Y%m%d %H-%M-%S"))
                shutil.copytree(old_dir_path, new_dir_path)
                self.text_browser_rcon_server_notice("client_success", "存档自动备份完成！备份路径：" + str(os.path.abspath(new_dir_path)))
                self.last_auto_backup_time = datetime.now()

    def timed_detection_5000(self):
        try:
            self.label_cpu_info.setText(str(psutil.cpu_percent(interval=0)) + " %")
            self.label_mem_info.setText(str(round(psutil.virtual_memory().used / (1024 * 1024), 2)) + " MB / " + str(round(psutil.virtual_memory().total / (1024 * 1024), 2)) + " MB")
            if self.server_run_flag:
                mem_info = 0
                psu_proc = psutil.Process(self.config["palserver_pid"])
                pcs = psu_proc.children(recursive=True)
                for proc in pcs:
                    mem_info += proc.memory_full_info().rss
                self.label_mem_info_2.setText(str(round(mem_info / (1024 * 1024), 2)) + " MB")
            else:
                self.label_mem_info_2.setText("0 MB")
        except:
            return

        if "palserver_path" in self.config:
            total, used, free = shutil.disk_usage(self.config["palserver_path"])
            self.label_disk_info.setText(str(round(used / (1024 * 1024 * 1024), 2)) + " GB / " + str(round(total / (1024 * 1024 * 1024), 2)) + " GB")
        else:
            self.label_disk_info.setText("未设置")

        if "backup_dir_path" in self.config:
            total, used, free = shutil.disk_usage(self.config["backup_dir_path"])
            self.label_disk_info_2.setText(str(round(used / (1024 * 1024 * 1024), 2)) + " GB / " + str(round(total / (1024 * 1024 * 1024), 2)) + " GB")
        else:
            self.label_disk_info_2.setText("未设置")

    def timed_detection_timer_60000(self):
        if self.rcon_connect_flag is False:
            self.label_online_player.setText("未连接 RCON")
            return

        self.table_widget_player_list.clearContents()
        self.table_widget_player_list.setRowCount(0)

        self.player_list_menu = QMenu(self)
        kick_action = QAction('踢出该玩家', self)
        kick_action.triggered.connect(self.kick_player)
        ban_action = QAction('封禁该玩家', self)
        ban_action.triggered.connect(self.ban_player)
        copy_uid_action = QAction('复制玩家UID', self)
        copy_uid_action.triggered.connect(self.copy_uid)
        copy_steamid_action = QAction('复制玩家StramID', self)
        copy_steamid_action.triggered.connect(self.copy_steamid)
        self.player_list_menu.addAction(kick_action)
        self.player_list_menu.addAction(ban_action)
        self.player_list_menu.addAction(copy_uid_action)
        self.player_list_menu.addAction(copy_steamid_action)
        self.table_widget_player_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table_widget_player_list.customContextMenuRequested.connect(self.show_player_list_menu)

        flag, rcon_result = self.pal_rcon.send_command("showplayers")
        if flag is False:
            self.rcon_connect_flag = False
            self.text_browser_rcon_server_notice("client_error", rcon_result.replace("\n", ""))
            return
        player_list = rcon_result.split("\n")[1:]
        player_id = 0
        self.player_list = []
        for player in player_list:
            if player == "":
                continue
            player_info = player.split(",")
            if len(player_info) < 3:
                continue
            self.player_list.append(player_info)
            self.table_widget_player_list.insertRow(player_id)
            item = QTableWidgetItem(player_info[0])
            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.table_widget_player_list.setItem(player_id, 0, item)
            item = QTableWidgetItem(player_info[-2])
            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.table_widget_player_list.setItem(player_id, 1, item)
            item = QTableWidgetItem(player_info[-1])
            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.table_widget_player_list.setItem(player_id, 2, item)
            player_id += 1

        self.label_online_player.setText(str(player_id) + "/" + str(self.config["game_player_limit"]))

    def kick_player(self):
        selected_items = self.table_widget_player_list.selectedItems()
        if selected_items:
            selected_row = selected_items[0].row()
            player_uid = self.player_list[selected_row][1]
            command = "KickPlayer " + player_uid
            self.text_browser_rcon_server_notice("client_command", command)
            rcon_result = self.pal_rcon.send_command(command)
            self.text_browser_rcon_server_notice("server_success", rcon_result.replace("\n", ""))
        self.get_server_info()

    def ban_player(self):
        selected_items = self.table_widget_player_list.selectedItems()
        if selected_items:
            selected_row = selected_items[0].row()
            player_uid = self.player_list[selected_row][1]
            command = "BanPlayer " + player_uid
            self.text_browser_rcon_server_notice("client_command", command)
            rcon_result = self.pal_rcon.send_command(command)
            self.text_browser_rcon_server_notice("server_success", rcon_result.replace("\n", ""))
        self.get_server_info()

    def copy_uid(self):
        selected_items = self.table_widget_player_list.selectedItems()
        if selected_items:
            selected_row = selected_items[0].row()
            player_uid = self.player_list[selected_row][1]
            pyperclip.copy(player_uid)

    def copy_steamid(self):
        selected_items = self.table_widget_player_list.selectedItems()
        if selected_items:
            selected_row = selected_items[0].row()
            player_steamid = self.player_list[selected_row][2]
            pyperclip.copy(player_steamid)

    def text_browser_rcon_server_notice(self, message_type, message):
        cursor = self.text_browser_rcon_server.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.text_browser_rcon_server.setTextCursor(cursor)
        black_format = QTextCharFormat()
        black_format.setForeground(QColor("black"))
        red_format = QTextCharFormat()
        red_format.setForeground(QColor("red"))
        green_format = QTextCharFormat()
        green_format.setForeground(QColor("green"))
        blue_format = QTextCharFormat()
        blue_format.setForeground(QColor("blue"))
        grey_format = QTextCharFormat()
        grey_format.setForeground(QColor(190, 190, 190))
        sky_blue_format = QTextCharFormat()
        sky_blue_format.setForeground(QColor(135, 206, 235))
        dark_violet_format = QTextCharFormat()
        dark_violet_format.setForeground(QColor(148, 0, 211))
        olive_drab_format = QTextCharFormat()
        olive_drab_format.setForeground(QColor(105, 139, 34))
        self.text_browser_rcon_server.setCurrentCharFormat(dark_violet_format)
        self.text_browser_rcon_server.append(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        if message_type == "client_success":
            self.text_browser_rcon_server.setCurrentCharFormat(sky_blue_format)
            self.text_browser_rcon_server.insertPlainText("  CLIENT: ")
            self.text_browser_rcon_server.setCurrentCharFormat(green_format)
            self.text_browser_rcon_server.insertPlainText("[SUCCESS] ")
        if message_type == "client_message":
            self.text_browser_rcon_server.setCurrentCharFormat(sky_blue_format)
            self.text_browser_rcon_server.insertPlainText("  CLIENT: ")
            self.text_browser_rcon_server.setCurrentCharFormat(olive_drab_format)
            self.text_browser_rcon_server.insertPlainText("[MESSAGE] ")
        if message_type == "client_error":
            self.text_browser_rcon_server.setCurrentCharFormat(sky_blue_format)
            self.text_browser_rcon_server.insertPlainText("  CLIENT: ")
            self.text_browser_rcon_server.setCurrentCharFormat(red_format)
            self.text_browser_rcon_server.insertPlainText("  [ERROR] ")
        if message_type == "client_command":
            self.text_browser_rcon_server.setCurrentCharFormat(sky_blue_format)
            self.text_browser_rcon_server.insertPlainText("  CLIENT: ")
            self.text_browser_rcon_server.setCurrentCharFormat(blue_format)
            self.text_browser_rcon_server.insertPlainText("[COMMAND] ")
        if message_type == "server_success":
            self.text_browser_rcon_server.setCurrentCharFormat(grey_format)
            self.text_browser_rcon_server.insertPlainText("  SERVER: ")
            self.text_browser_rcon_server.setCurrentCharFormat(green_format)
            self.text_browser_rcon_server.insertPlainText("[SUCCESS] ")
        self.text_browser_rcon_server.setCurrentCharFormat(black_format)
        self.text_browser_rcon_server.insertPlainText(message)
        self.text_browser_rcon_server.ensureCursorVisible()

    def save_config_json(self):
        json_operation.save_json(self.config_path, self.config)

    def check_palserver_path(self):
        if "palserver_path" not in self.config:
            return False

        if os.path.isfile(self.config["palserver_path"]) is False:
            self.line_edit_palserver_path.setText("")
            self.config.pop("palserver_path")
            self.save_config_json()
            self.text_browser_rcon_server_notice("client_error", "检测到 PalServer.exe 文件不存在，请重新选择！")
            return False

        self.palserver_settings_path = os.path.abspath(os.path.join(self.config["palserver_path"], r"../Pal/Saved/Config/WindowsServer/PalWorldSettings.ini"))
        if os.path.isfile(self.palserver_settings_path) is False:
            self.line_edit_palserver_path.setText("")
            self.config.pop("palserver_path")
            self.save_config_json()
            self.text_browser_rcon_server_notice("client_error", "服务端路径下的 /Pal/Saved/Config/WindowsServer/PalWorldSettings.ini 配置文件不存在，请启动一次PalServer.exe，或检查服务端完整性！")
            return False

        self.line_edit_palserver_path.setText(self.config["palserver_path"])
        if os.stat(self.palserver_settings_path).st_size < 10:
            self.text_browser_rcon_server_notice("client_success", "检测到 服务端路径下的 /Pal/Saved/Config/WindowsServer/PalWorldSettings.ini 配置文件大小不正确，正在重新初始化。")
            settings_file_operation.default_setting(self.palserver_settings_path)

        self.save_config_json()
        self.button_open_settings_dir.setEnabled(True)
        self.button_open_rcon_settings_file.setEnabled(True)
        self.button_get_rcon_config.setEnabled(True)
        self.button_automatic_rcon.setEnabled(True)
        try:
            self.option_settings_dict = settings_file_operation.load_setting(self.palserver_settings_path)
        except:
            settings_file_operation.default_setting(self.palserver_settings_path)
            settings_file_operation.load_setting(self.palserver_settings_path)
            shutil.copy(self.palserver_settings_path, os.path.join(sys.argv[0], "../PalWorldSettings.ini"))
            self.text_browser_rcon_server_notice("client_success", "检测到 服务端路径下的 /Pal/Saved/Config/WindowsServer/PalWorldSettings.ini 配置文件读取出错，已自动重置配置文件，旧文件已备份到软件根目录。")
            QMessageBox.critical(self, "错误", "检测到 服务端路径下的 /Pal/Saved/Config/WindowsServer/PalWorldSettings.ini 配置文件读取出错，已自动重置配置文件，旧文件已备份到软件根目录。")
        self.text_edit_server_name.setText(self.option_settings_dict["ServerName"].replace("\"", ""))
        self.text_edit_server_description.setText(self.option_settings_dict["ServerDescription"].replace("\"", ""))

    def button_select_file_click(self):
        qfile_dialog = QFileDialog.getOpenFileName(self, "选择文件", "/", "PalServer (PalServer.exe)")
        self.config["palserver_path"] = qfile_dialog[0]
        self.save_config_json()
        self.text_browser_rcon_server_notice("client_success", "已获取PalServer.exe路径：" + qfile_dialog[0])
        self.check_palserver_path()

    def button_open_settings_dir_click(self):
        os.system("explorer /select,\"" + str(os.path.abspath(self.palserver_settings_path)) + "\"")
        self.text_browser_rcon_server_notice("client_success", "已打开 配置文件夹 目录，请修改RCON相关字段")

    def button_open_rcon_settings_file_click(self):
        try:
            subprocess.run(["notepad.exe", self.palserver_settings_path], check=True)
            self.text_browser_rcon_server_notice("client_success", "已通过记事本打开 配置文件，请修改RCON相关字段")
        except subprocess.CalledProcessError as e:
            self.text_browser_rcon_server_notice("client_error", "无法打开 RCON 配置文件！")
            return
        except:
            self.text_browser_rcon_server_notice("client_error", "发生未知错误！")
            QMessageBox.critical(self, "错误", "发生未知错误！请联系开发人员！")
            return

    def button_get_rcon_config_click(self):
        if self.option_settings_dict['RCONEnabled'] == "False":
            self.text_browser_rcon_server_notice("client_error", "配置文件中 RCONEnabled 未启用，请修改为 True 或使用自动配置！")
            QMessageBox.critical(self, "错误", "配置文件中 RCONEnabled 未启用，请修改为 True 或使用自动配置！")
            return
        self.config["rcon_addr"] = "127.0.0.1"
        self.config["rcon_port"] = int(self.option_settings_dict["RCONPort"])
        self.config["rcon_password"] = self.option_settings_dict["AdminPassword"].replace("\"", "")
        self.save_config_json()
        self.line_edit_rcon_addr.setText("127.0.0.1")
        self.line_edit_rcon_port.setText(str(self.option_settings_dict["RCONPort"]))
        self.line_edit_rcon_password.setText(self.option_settings_dict["AdminPassword"].replace("\"", ""))
        self.text_browser_rcon_server_notice("client_success", "已获取配置文件中的 RCON 连接信息")

    def button_automatic_rcon_click(self):
        self.option_settings_dict['RCONEnabled'] = True
        self.option_settings_dict['RCONPort'] = 25575
        admin_password = random_password.random_string()
        self.option_settings_dict['AdminPassword'] = "\"" + admin_password + "\""
        new_option_settings = ','.join(f"{key}={value}" for key, value in self.option_settings_dict.items())
        settings_file_operation.save_setting(self.palserver_settings_path, new_option_settings)
        self.config["rcon_addr"] = "127.0.0.1"
        self.config["rcon_port"] = 25575
        self.config["rcon_password"] = admin_password
        self.save_config_json()
        self.line_edit_rcon_addr.setText(self.config["rcon_addr"])
        self.line_edit_rcon_port.setText(str(self.config["rcon_port"]))
        self.line_edit_rcon_password.setText(self.config["rcon_password"])
        self.text_browser_rcon_server_notice("client_success", "已自动配置 RCON 连接信息，已生成随机密码：" + admin_password)

    def line_edit_rcon_textchange(self):
        rcon_addr = self.line_edit_rcon_addr.text()
        rcon_port = self.line_edit_rcon_port.text()
        rcon_password = self.line_edit_rcon_password.text()
        self.button_test_connect.setEnabled(rcon_addr != "" and rcon_port != "" and rcon_password != "")

    def button_test_connect_click(self):
        rcon_addr = self.line_edit_rcon_addr.text()
        rcon_port = self.line_edit_rcon_port.text()
        rcon_password = self.line_edit_rcon_password.text()
        if rcon_port.isdigit() is False:
            self.text_browser_rcon_server_notice("client_error", "RCON 端口只能为数字，请重新输入！")
            return
        if int(rcon_port) < 1000 or int(rcon_port) > 65534:
            self.text_browser_rcon_server_notice("client_error", "RCON 端口需在1000~65534范围，请重新输入！")
            return

        self.pal_rcon = PalRcon(rcon_addr, int(rcon_port), rcon_password)
        flag, rcon_result = self.pal_rcon.send_command("info")
        if flag is False:
            self.rcon_connect_flag = False
            self.text_browser_rcon_server_notice("client_error", rcon_result.replace("\n", ""))
            return
        server_version = rcon_result[rcon_result.index("[") + 1:rcon_result.index("]")]
        self.label_server_version.setText(server_version)
        self.config["rcon_addr"] = rcon_addr
        self.config["rcon_port"] = int(rcon_port)
        self.config["rcon_password"] = rcon_password
        self.save_config_json()
        self.rcon_connect_flag = True
        self.text_browser_rcon_server_notice("client_success", "RCON 服务器连接成功")

    def check_box_launch_options_click(self, flag):
        self.line_edit_launch_options.setEnabled(not flag)

    def button_game_start_click(self):
        if "palserver_path" not in self.config:
            self.text_browser_rcon_server_notice("client_error", "请先选择PalServer.exe服务端文件！")
            return

        game_port = self.line_edit_game_port.text()
        game_publicport = self.line_edit_game_publicport.text()
        game_player_limit = self.line_edit_game_player_limit.text()
        if game_port.isdigit() is False:
            self.text_browser_rcon_server_notice("client_error", "游戏 连接端口只能为数字，请重新输入！")
            return
        if int(game_port) < 1000 or int(game_port) > 65534:
            self.text_browser_rcon_server_notice("client_error", "游戏 连接端口需在1000~65534范围，请重新输入！")
            return
        if game_publicport.isdigit() is False:
            self.text_browser_rcon_server_notice("client_error", "游戏 查询端口只能为数字，请重新输入！")
            return
        if int(game_publicport) < 1000 or int(game_publicport) > 65534:
            self.text_browser_rcon_server_notice("client_error", "游戏 查询端口需在1000~65534范围，请重新输入！")
            return
        if game_player_limit.isdigit() is False:
            self.text_browser_rcon_server_notice("client_error", "游戏 人数上限只能为数字，请重新输入！")
            return
        if int(game_player_limit) < 2 or int(game_player_limit) > 128:
            self.text_browser_rcon_server_notice("client_error", "游戏 人数上限需在2~128范围，请重新输入！")
            return

        self.config["launch_options_flag"] = self.check_box_launch_options.isChecked()
        self.config["launch_options_info"] = self.line_edit_launch_options.text()
        command = self.config["palserver_path"] + " -port=" + game_port + " -players=" + game_player_limit + " -publicip 0.0.0.0 -publicport " + game_publicport
        if self.config["launch_options_flag"]:
            command += " " + self.config["launch_options_info"]
        process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
        self.config["game_port"] = int(game_port)
        self.config["game_publicport"] = int(game_publicport)
        self.config["game_player_limit"] = int(game_player_limit)
        self.config["palserver_pid"] = process.pid
        self.save_config_json()
        self.text_browser_rcon_server_notice("client_success", "PalServer 服务器已启动，获取到进程PID：" + str(process.pid))
        self.server_run_flag = True
        self.server_run_time = datetime.now()

    def button_game_stop_click(self):
        if self.rcon_connect_flag is False:
            self.text_browser_rcon_server_notice("client_error", "请先连接 RCON ！")
            return
        command = "Shutdown 1 The_server_will_stop_in_1_seconds!!!"
        self.text_browser_rcon_server_notice("client_command", command)
        flag, rcon_result = self.pal_rcon.send_command(command)
        self.rcon_connect_flag = flag
        if flag is False:
            self.rcon_connect_flag = False
            self.text_browser_rcon_server_notice("client_error", rcon_result.replace("\n", ""))
            return
        self.text_browser_rcon_server_notice("server_success", rcon_result.replace("\n", ""))
        self.server_run_flag = False

    def button_game_restart_click(self):
        if self.rcon_connect_flag is False:
            self.text_browser_rcon_server_notice("client_error", "请先连接 RCON ！")
            return
        self.server_run_flag = False
        self.stop_countdown = 11
        self.stop_timer = QTimer(self)
        self.stop_timer.timeout.connect(self.broadcast_restart)
        self.stop_timer.start(1000)

    def broadcast_restart(self):
        self.stop_countdown -= 1
        if self.stop_countdown > 0:
            command = "Broadcast The_server_will_restart_in_" + str(int(self.stop_countdown)) + "_seconds!!!"
            self.text_browser_rcon_server_notice("client_command", command)
            flag, rcon_result = self.pal_rcon.send_command(command)
            if flag is False:
                self.rcon_connect_flag = False
                self.text_browser_rcon_server_notice("client_error", rcon_result.replace("\n", ""))
                return
            self.text_browser_rcon_server_notice("server_success", rcon_result.replace("\n", ""))
        elif self.stop_countdown == 0:
            command = "Shutdown 1 The_server_will_restart_in_0_seconds!!!"
            self.text_browser_rcon_server_notice("client_command", command)
            flag, rcon_result = self.pal_rcon.send_command(command)
            if flag is False:
                self.rcon_connect_flag = False
                self.text_browser_rcon_server_notice("client_error", rcon_result.replace("\n", ""))
                return
            self.server_run_flag = False
            self.text_browser_rcon_server_notice("server_success", rcon_result.replace("\n", ""))
        elif self.stop_countdown == -10:
            self.button_game_start_click()
        elif self.stop_countdown == -20:
            self.stop_timer.stop()
            self.button_test_connect_click()

    def button_game_kill_click(self):
        self.server_run_flag = False
        psu_proc = psutil.Process(self.config["palserver_pid"])
        pcs = psu_proc.children(recursive=True)
        for proc in pcs:
            os.kill(proc.pid, 9)
        self.text_browser_rcon_server_notice("client_success", "已强制停止服务端")

    def button_send_command_click(self):
        command = self.line_edit_command.text()
        if command == "":
            return
        self.text_browser_rcon_server_notice("client_command", command.replace("\n", ""))
        flag, rcon_result = self.pal_rcon.send_command(command)
        if flag is False:
            self.rcon_connect_flag = False
            self.text_browser_rcon_server_notice("client_error", rcon_result.replace("\n", ""))
            return
        self.text_browser_rcon_server_notice("server_success", rcon_result.replace("\n", ""))
        self.line_edit_command.setText("")

    def show_player_list_menu(self, position):
        self.player_list_menu.exec_(self.table_widget_player_list.mapToGlobal(position))

    def button_countdown_stop_click(self):
        if self.rcon_connect_flag is False:
            self.text_browser_rcon_server_notice("client_error", "请先连接 RCON ！")
            return
        value, flag = QInputDialog.getInt(self, "倒计时关服并广播", "设置多少时间后关服(秒)：", 60, 10, 999, 2)
        if flag:
            self.stop_countdown = value + 1
            self.stop_timer = QTimer(self)
            self.stop_timer.timeout.connect(self.broadcast_stop)
            self.stop_timer.start(1000)

    def broadcast_stop(self):
        self.stop_countdown -= 1
        if self.stop_countdown > 0:
            command = "Broadcast The_server_will_stop_in_" + str(int(self.stop_countdown)) + "_seconds!!!"
            self.text_browser_rcon_server_notice("client_command", command)
            flag, rcon_result = self.pal_rcon.send_command(command)
            if flag is False:
                self.rcon_connect_flag = False
                self.text_browser_rcon_server_notice("client_error", rcon_result.replace("\n", ""))
                return
            self.text_browser_rcon_server_notice("server_success", rcon_result.replace("\n", ""))
        elif self.stop_countdown == 0:
            self.button_game_stop_click()
            self.stop_timer.stop()

    def button_broadcast_click(self):
        value, flag = QInputDialog.getText(self, "广播", "请输入需要全服广播的内容：")
        if flag:
            command = "Broadcast " + value
            self.text_browser_rcon_server_notice("client_command", command)
            flag, rcon_result = self.pal_rcon.send_command(command)
            if flag is False:
                self.rcon_connect_flag = False
                self.text_browser_rcon_server_notice("client_error", rcon_result.replace("\n", ""))
                return
            self.text_browser_rcon_server_notice("server_success", rcon_result.replace("\n", ""))

    def check_box_crash_detection_click(self, flag):
        self.config["crash_detection_flag"] = flag
        self.save_config_json()

    def check_box_auto_restart_click(self, flag):
        self.config["auto_restart_flag"] = flag
        self.line_edit_auto_restart_time_limit.setEnabled(not flag)
        if flag:
            self.config["auto_restart_time_limit"] = int(self.line_edit_auto_restart_time_limit.text())
        self.save_config_json()

    def line_edit_auto_restart_time_limit_textchange(self):
        auto_restart_time_limit = self.line_edit_auto_restart_time_limit.text()
        if auto_restart_time_limit.isdigit() is False:
            self.text_browser_rcon_server_notice("client_error", "重启时间 只能为数字，请重新输入！")
            return
        if int(auto_restart_time_limit) < 600 or int(auto_restart_time_limit) > 86400:
            self.text_browser_rcon_server_notice("client_error", "重启时间 需在600~86400范围，请重新输入！")
            return

    def check_box_auto_restart_player_click(self, flag):
        self.config["auto_restart_player_flag"] = flag
        self.line_edit_auto_restart_player_limit.setEnabled(not flag)
        if flag:
            self.config["auto_restart_player_limit"] = int(self.line_edit_auto_restart_player_limit.text())
        self.save_config_json()

    def line_edit_auto_restart_player_limit_textchange(self):
        auto_restart_player_limit = self.line_edit_auto_restart_player_limit.text()
        if auto_restart_player_limit.isdigit() is False:
            self.text_browser_rcon_server_notice("client_error", "重启人数限制 只能为数字，请重新输入！")
            return
        if int(auto_restart_player_limit) < 0 or int(auto_restart_player_limit) > 128:
            self.text_browser_rcon_server_notice("client_error", "重启人数限制 需在0~128范围，请重新输入！")
            return

    def check_box_auto_backup_click(self, flag):
        self.config["auto_backup_flag"] = flag
        self.line_edit_auto_backup_time_limit.setEnabled(not flag)
        if flag:
            self.config["auto_backup_time_limit"] = int(self.line_edit_auto_backup_time_limit.text())
        self.save_config_json()

    def line_edit_auto_backup_time_limit_textchange(self):
        auto_backup_time_limit = self.line_edit_auto_backup_time_limit.text()
        if auto_backup_time_limit.isdigit() is False:
            self.text_browser_rcon_server_notice("client_error", "备份时间间隔 只能为数字，请重新输入！")
            return
        if int(auto_backup_time_limit) < 600 or int(auto_backup_time_limit) > 86400:
            self.text_browser_rcon_server_notice("client_error", "备份时间间隔 需在600~86400范围，请重新输入！")
            return

    def button_select_backup_dir_click(self):
        qfile_dialog = QFileDialog.getExistingDirectory(self, "选择文件夹", None)
        if os.path.isdir(qfile_dialog):
            self.line_edit_backup_path.setText(qfile_dialog)
            self.config["backup_dir_path"] = qfile_dialog
            self.save_config_json()
            self.check_box_auto_backup.setEnabled(True)
            self.line_edit_auto_backup_time_limit.setEnabled(True)

    def button_edit_settings_click(self):
        if "palserver_path" in self.config is False:
            QMessageBox.critical(self, "错误", "请先配置 PalServer.exe 路径，再修改配置文件！")
            return
        if self.palserver_settings_path is None:
            QMessageBox.critical(self, "错误", "请先配置 PalServer.exe 路径，再修改配置文件！")
            return
        if os.path.isfile(self.palserver_settings_path) is False:
            QMessageBox.critical(self, "错误", "服务端路径下的 /Pal/Saved/Config/WindowsServer/PalWorldSettings.ini 配置文件不存在，请启动一次PalServer.exe，或检查服务端完整性！")
            return

        self.world_settings_window = world_settings_activity.Window()
        self.world_settings_window.show()

    def button_edit_server_name_click(self):
        self.option_settings_dict["ServerName"] = "\"" + self.text_edit_server_name.toPlainText().replace("\n", "") + "\""
        self.option_settings_dict["ServerDescription"] = "\"" + self.text_edit_server_description.toPlainText().replace("\n", "") + "\""
        new_option_settings = ','.join(f"{key}={value}" for key, value in self.option_settings_dict.items())
        settings_file_operation.save_setting(self.palserver_settings_path, new_option_settings)
        self.text_browser_rcon_server_notice("client_success", "服务器名称或服务器描述已修改成功，现可启动服务器查看。")
