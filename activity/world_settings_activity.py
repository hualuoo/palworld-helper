import os
import shutil
import sys

from PyQt5.uic import loadUi
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QFileDialog, QTableWidgetItem, QMenu, QAction, QInputDialog

from utils import json_operation, settings_file_operation


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.module_path = os.path.split(sys.modules[__name__].__file__)[0]
        self.config_path = os.path.join(sys.argv[0], r"../config.json")
        self.config = json_operation.load_json(self.config_path)
        self.palserver_settings_path = None
        self.option_settings_dict = None
        self.initUi()

    def initUi(self):
        loadUi(os.path.join(self.module_path, r"../ui/world_settings.ui"), self)
        self.setWindowTitle("修改服务器配置文件")
        self.setFixedSize(880, 680)
        self.setWindowIcon(QIcon(os.path.join(self.module_path, r"../resource/favicon.ico")))
        self.palserver_settings_path = os.path.join(self.config["palserver_path"], r"../Pal/Saved/Config/WindowsServer/PalWorldSettings.ini")
        try:
            self.option_settings_dict = settings_file_operation.load_setting(self.palserver_settings_path)
        except:
            settings_file_operation.default_setting(self.palserver_settings_path)
            shutil.copy(self.palserver_settings_path, os.path.join(sys.argv[0], "PalWorldSettings.ini"))
            self.text_browser_rcon_server_notice("client_success", "检测到 服务端路径下的 /Pal/Saved/Config/WindowsServer/PalWorldSettings.ini 配置文件读取出错，已自动重置配置文件，旧文件已备份到软件根目录。")
            QMessageBox.critical(self, "错误", "检测到 服务端路径下的 /Pal/Saved/Config/WindowsServer/PalWorldSettings.ini 配置文件读取出错，已自动重置配置文件，旧文件已备份到软件根目录。")
        self.load_settings()

    def load_settings(self):
        # print(self.option_settings_dict)
        self.comboBox_Difficulty.setCurrentText(self.option_settings_dict["Difficulty"])
        self.doubleSpinBox_DayTimeSpeedRate.setValue(float(self.option_settings_dict["DayTimeSpeedRate"]))
        self.doubleSpinBox_NightTimeSpeedRate.setValue(float(self.option_settings_dict["NightTimeSpeedRate"]))
        self.doubleSpinBox_ExpRate.setValue(float(self.option_settings_dict["ExpRate"]))
        self.doubleSpinBox_PalCaptureRate.setValue(float(self.option_settings_dict["PalCaptureRate"]))
        self.doubleSpinBox_PalSpawnNumRate.setValue(float(self.option_settings_dict["PalSpawnNumRate"]))
        self.doubleSpinBox_PalDamageRateAttack.setValue(float(self.option_settings_dict["PalDamageRateAttack"]))
        self.doubleSpinBox_PalDamageRateDefense.setValue(float(self.option_settings_dict["PalDamageRateDefense"]))
        self.doubleSpinBox_PlayerDamageRateAttack.setValue(float(self.option_settings_dict["PlayerDamageRateAttack"]))
        self.doubleSpinBox_PlayerDamageRateDefense.setValue(float(self.option_settings_dict["PlayerDamageRateDefense"]))
        self.doubleSpinBox_PlayerStomachDecreaceRate.setValue(float(self.option_settings_dict["PlayerStomachDecreaceRate"]))
        self.doubleSpinBox_PlayerStaminaDecreaceRate.setValue(float(self.option_settings_dict["PlayerStaminaDecreaceRate"]))
        self.doubleSpinBox_PlayerAutoHPRegeneRate.setValue(float(self.option_settings_dict["PlayerAutoHPRegeneRate"]))
        self.doubleSpinBox_PlayerAutoHpRegeneRateInSleep.setValue(float(self.option_settings_dict["PlayerAutoHpRegeneRateInSleep"]))
        self.doubleSpinBox_PalStomachDecreaceRate.setValue(float(self.option_settings_dict["PalStomachDecreaceRate"]))
        self.doubleSpinBox_PalStaminaDecreaceRate.setValue(float(self.option_settings_dict["PalStaminaDecreaceRate"]))
        self.doubleSpinBox_PalAutoHPRegeneRate.setValue(float(self.option_settings_dict["PalAutoHPRegeneRate"]))
        self.doubleSpinBox_PalAutoHpRegeneRateInSleep.setValue(float(self.option_settings_dict["PalAutoHpRegeneRateInSleep"]))
        self.doubleSpinBox_BuildObjectDamageRate.setValue(float(self.option_settings_dict["BuildObjectDamageRate"]))
        self.doubleSpinBox_BuildObjectDeteriorationDamageRate.setValue(float(self.option_settings_dict["BuildObjectDeteriorationDamageRate"]))
        self.doubleSpinBox_CollectionDropRate.setValue(float(self.option_settings_dict["CollectionDropRate"]))
        self.doubleSpinBox_CollectionObjectHpRate.setValue(float(self.option_settings_dict["CollectionObjectHpRate"]))
        self.doubleSpinBox_CollectionObjectRespawnSpeedRate.setValue(float(self.option_settings_dict["CollectionObjectRespawnSpeedRate"]))
        self.doubleSpinBox_EnemyDropItemRate.setValue(float(self.option_settings_dict["EnemyDropItemRate"]))
        self.comboBox_DeathPenalty.setCurrentText(self.option_settings_dict["DeathPenalty"])
        self.checkBox_bEnablePlayerToPlayerDamage.setChecked(self.option_settings_dict["bEnablePlayerToPlayerDamage"] == "True")
        self.checkBox_bEnableFriendlyFire.setChecked(self.option_settings_dict["bEnableFriendlyFire"] == "True")
        self.checkBox_bEnableInvaderEnemy.setChecked(self.option_settings_dict["bEnableInvaderEnemy"] == "True")
        self.checkBox_bActiveUNKO.setChecked(self.option_settings_dict["bActiveUNKO"] == "True")
        self.checkBox_bEnableAimAssistPad.setChecked(self.option_settings_dict["bEnableAimAssistPad"] == "True")
        self.checkBox_bEnableAimAssistKeyboard.setChecked(self.option_settings_dict["bEnableAimAssistKeyboard"] == "True")
        self.doubleSpinBox_DropItemMaxNum.setValue(int(self.option_settings_dict["DropItemMaxNum"]))
        self.doubleSpinBox_DropItemMaxNum_UNKO.setValue(int(self.option_settings_dict["DropItemMaxNum_UNKO"]))
        self.doubleSpinBox_BaseCampMaxNum.setValue(int(self.option_settings_dict["BaseCampMaxNum"]))
        self.doubleSpinBox_BaseCampWorkerMaxNum.setValue(int(self.option_settings_dict["BaseCampWorkerMaxNum"]))
        self.doubleSpinBox_DropItemAliveMaxHours.setValue(float(self.option_settings_dict["DropItemAliveMaxHours"]))
        self.checkBox_bAutoResetGuildNoOnlinePlayers.setChecked(self.option_settings_dict["bAutoResetGuildNoOnlinePlayers"] == "True")
        self.doubleSpinBox_AutoResetGuildTimeNoOnlinePlayers.setValue(float(self.option_settings_dict["AutoResetGuildTimeNoOnlinePlayers"]))
        self.doubleSpinBox_GuildPlayerMaxNum.setValue(int(self.option_settings_dict["GuildPlayerMaxNum"]))
        self.doubleSpinBox_PalEggDefaultHatchingTime.setValue(float(self.option_settings_dict["PalEggDefaultHatchingTime"]))
        self.doubleSpinBox_WorkSpeedRate.setValue(float(self.option_settings_dict["WorkSpeedRate"]))
        self.checkBox_bIsMultiplay.setChecked(self.option_settings_dict["bIsMultiplay"] == "True")
        self.checkBox_bIsPvP.setChecked(self.option_settings_dict["bIsPvP"] == "True")
        self.checkBox_bCanPickupOtherGuildDeathPenaltyDrop.setChecked(self.option_settings_dict["bCanPickupOtherGuildDeathPenaltyDrop"] == "True")
        self.checkBox_bEnableNonLoginPenalty.setChecked(self.option_settings_dict["bEnableNonLoginPenalty"] == "True")
        self.checkBox_bEnableFastTravel.setChecked(self.option_settings_dict["bEnableFastTravel"] == "True")
        self.checkBox_bIsStartLocationSelectByMap.setChecked(self.option_settings_dict["bIsStartLocationSelectByMap"] == "True")
        self.checkBox_bExistPlayerAfterLogout.setChecked(self.option_settings_dict["bExistPlayerAfterLogout"] == "True")
        self.checkBox_bEnableDefenseOtherGuildPlayer.setChecked(self.option_settings_dict["bEnableDefenseOtherGuildPlayer"] == "True")
        self.doubleSpinBox_CoopPlayerMaxNum.setValue(int(self.option_settings_dict["CoopPlayerMaxNum"]))

    def button_write_click(self):
        self.option_settings_dict["Difficulty"] = self.comboBox_Difficulty.currentText()
        self.option_settings_dict["DayTimeSpeedRate"] = "{:.6f}".format(self.doubleSpinBox_DayTimeSpeedRate.value())
        self.option_settings_dict["NightTimeSpeedRate"] = "{:.6f}".format(self.doubleSpinBox_NightTimeSpeedRate.value())
        self.option_settings_dict["ExpRate"] = "{:.6f}".format(self.doubleSpinBox_ExpRate.value())
        self.option_settings_dict["PalCaptureRate"] = "{:.6f}".format(self.doubleSpinBox_PalCaptureRate.value())
        self.option_settings_dict["PalSpawnNumRate"] = "{:.6f}".format(self.doubleSpinBox_PalSpawnNumRate.value())
        self.option_settings_dict["PalDamageRateAttack"] = "{:.6f}".format(self.doubleSpinBox_PalDamageRateAttack.value())
        self.option_settings_dict["PalDamageRateDefense"] = "{:.6f}".format(self.doubleSpinBox_PalDamageRateDefense.value())
        self.option_settings_dict["PlayerDamageRateAttack"] = "{:.6f}".format(self.doubleSpinBox_PlayerDamageRateAttack.value())
        self.option_settings_dict["PlayerDamageRateDefense"] = "{:.6f}".format(self.doubleSpinBox_PlayerDamageRateDefense.value())
        self.option_settings_dict["PlayerStomachDecreaceRate"] = "{:.6f}".format(self.doubleSpinBox_PlayerStomachDecreaceRate.value())
        self.option_settings_dict["PlayerStaminaDecreaceRate"] = "{:.6f}".format(self.doubleSpinBox_PlayerStaminaDecreaceRate.value())
        self.option_settings_dict["PlayerAutoHPRegeneRate"] = "{:.6f}".format(self.doubleSpinBox_PlayerAutoHPRegeneRate.value())
        self.option_settings_dict["PlayerAutoHpRegeneRateInSleep"] = "{:.6f}".format(self.doubleSpinBox_PlayerAutoHpRegeneRateInSleep.value())
        self.option_settings_dict["PalStomachDecreaceRate"] = "{:.6f}".format(self.doubleSpinBox_PalStomachDecreaceRate.value())
        self.option_settings_dict["PalStaminaDecreaceRate"] = "{:.6f}".format(self.doubleSpinBox_PalStaminaDecreaceRate.value())
        self.option_settings_dict["PalAutoHPRegeneRate"] = "{:.6f}".format(self.doubleSpinBox_PalAutoHPRegeneRate.value())
        self.option_settings_dict["PalAutoHpRegeneRateInSleep"] = "{:.6f}".format(self.doubleSpinBox_PalAutoHpRegeneRateInSleep.value())
        self.option_settings_dict["BuildObjectDamageRate"] = "{:.6f}".format(self.doubleSpinBox_BuildObjectDamageRate.value())
        self.option_settings_dict["BuildObjectDeteriorationDamageRate"] = "{:.6f}".format(self.doubleSpinBox_BuildObjectDeteriorationDamageRate.value())
        self.option_settings_dict["CollectionDropRate"] = "{:.6f}".format(self.doubleSpinBox_CollectionDropRate.value())
        self.option_settings_dict["CollectionObjectHpRate"] = "{:.6f}".format(self.doubleSpinBox_CollectionObjectHpRate.value())
        self.option_settings_dict["CollectionObjectRespawnSpeedRate"] = "{:.6f}".format(self.doubleSpinBox_CollectionObjectRespawnSpeedRate.value())
        self.option_settings_dict["EnemyDropItemRate"] = "{:.6f}".format(self.doubleSpinBox_EnemyDropItemRate.value())
        self.option_settings_dict["DeathPenalty"] = self.comboBox_DeathPenalty.currentText()
        if self.checkBox_bEnablePlayerToPlayerDamage.isChecked():
            self.option_settings_dict["bEnablePlayerToPlayerDamage"] = "True"
        else:
            self.option_settings_dict["bEnablePlayerToPlayerDamage"] = "False"
        if self.checkBox_bEnableFriendlyFire.isChecked():
            self.option_settings_dict["bEnableFriendlyFire"] = "True"
        else:
            self.option_settings_dict["bEnableFriendlyFire"] = "False"
        if self.checkBox_bEnableInvaderEnemy.isChecked():
            self.option_settings_dict["bEnableInvaderEnemy"] = "True"
        else:
            self.option_settings_dict["bEnableInvaderEnemy"] = "False"
        if self.checkBox_bActiveUNKO.isChecked():
            self.option_settings_dict["bActiveUNKO"] = "True"
        else:
            self.option_settings_dict["bActiveUNKO"] = "False"
        if self.checkBox_bEnableAimAssistPad.isChecked():
            self.option_settings_dict["bEnableAimAssistPad"] = "True"
        else:
            self.option_settings_dict["bEnableAimAssistPad"] = "False"
        if self.checkBox_bEnableAimAssistKeyboard.isChecked():
            self.option_settings_dict["bEnableAimAssistKeyboard"] = "True"
        else:
            self.option_settings_dict["bEnableAimAssistKeyboard"] = "False"
        self.option_settings_dict["DropItemMaxNum"] = str(int(self.doubleSpinBox_DropItemMaxNum.value()))
        self.option_settings_dict["DropItemMaxNum_UNKO"] = str(int(self.doubleSpinBox_DropItemMaxNum_UNKO.value()))
        self.option_settings_dict["BaseCampMaxNum"] = str(int(self.doubleSpinBox_BaseCampMaxNum.value()))
        self.option_settings_dict["BaseCampWorkerMaxNum"] = str(int(self.doubleSpinBox_BaseCampWorkerMaxNum.value()))
        self.option_settings_dict["DropItemAliveMaxHours"] = "{:.6f}".format(self.doubleSpinBox_DropItemAliveMaxHours.value())
        if self.checkBox_bAutoResetGuildNoOnlinePlayers.isChecked():
            self.option_settings_dict["bAutoResetGuildNoOnlinePlayers"] = "True"
        else:
            self.option_settings_dict["bAutoResetGuildNoOnlinePlayers"] = "False"
        self.option_settings_dict["AutoResetGuildTimeNoOnlinePlayers"] = "{:.6f}".format(self.doubleSpinBox_AutoResetGuildTimeNoOnlinePlayers.value())
        self.option_settings_dict["GuildPlayerMaxNum"] = str(int(self.doubleSpinBox_GuildPlayerMaxNum.value()))
        self.option_settings_dict["PalEggDefaultHatchingTime"] = "{:.6f}".format(self.doubleSpinBox_PalEggDefaultHatchingTime.value())
        self.option_settings_dict["WorkSpeedRate"] = "{:.6f}".format(self.doubleSpinBox_WorkSpeedRate.value())
        if self.checkBox_bIsMultiplay.isChecked():
            self.option_settings_dict["bIsMultiplay"] = "True"
        else:
            self.option_settings_dict["bIsMultiplay"] = "False"
        if self.checkBox_bIsPvP.isChecked():
            self.option_settings_dict["bIsPvP"] = "True"
        else:
            self.option_settings_dict["bIsPvP"] = "False"
        if self.checkBox_bCanPickupOtherGuildDeathPenaltyDrop.isChecked():
            self.option_settings_dict["bCanPickupOtherGuildDeathPenaltyDrop"] = "True"
        else:
            self.option_settings_dict["bCanPickupOtherGuildDeathPenaltyDrop"] = "False"
        if self.checkBox_bEnableNonLoginPenalty.isChecked():
            self.option_settings_dict["bEnableNonLoginPenalty"] = "True"
        else:
            self.option_settings_dict["bEnableNonLoginPenalty"] = "False"
        if self.checkBox_bEnableFastTravel.isChecked():
            self.option_settings_dict["bEnableFastTravel"] = "True"
        else:
            self.option_settings_dict["bEnableFastTravel"] = "False"
        if self.checkBox_bIsStartLocationSelectByMap.isChecked():
            self.option_settings_dict["bIsStartLocationSelectByMap"] = "True"
        else:
            self.option_settings_dict["bIsStartLocationSelectByMap"] = "False"
        if self.checkBox_bExistPlayerAfterLogout.isChecked():
            self.option_settings_dict["bExistPlayerAfterLogout"] = "True"
        else:
            self.option_settings_dict["bExistPlayerAfterLogout"] = "False"
        if self.checkBox_bEnableDefenseOtherGuildPlayer.isChecked():
            self.option_settings_dict["bEnableDefenseOtherGuildPlayer"] = "True"
        else:
            self.option_settings_dict["bEnableDefenseOtherGuildPlayer"] = "False"
        self.option_settings_dict["CoopPlayerMaxNum"] = str(int(self.doubleSpinBox_CoopPlayerMaxNum.value()))

        new_option_settings = ','.join(f"{key}={value}" for key, value in self.option_settings_dict.items())
        settings_file_operation.save_setting(self.palserver_settings_path, new_option_settings)
        QMessageBox.information(self, "成功", "服务器配置文件已修改！")

    def button_default_click(self):
        settings_file_operation.default_setting(self.palserver_settings_path)
        self.option_settings_dict = settings_file_operation.load_setting(self.palserver_settings_path)
        self.load_settings()
        QMessageBox.information(self, "成功", "服务器配置文件已还原成默认值！")
