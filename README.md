<h1 align="center">
  <a href="https://github.com/hualuoo/palworld_helper" alt="logo" ><img src="https://raw.githubusercontent.com/hualuoo/palworld_helper/main/resource/favicon.ico" width="60"/></a>
  <br>
  PalWorld Helper
  <br>
</h1>
<h3 align="center">幻兽帕鲁开服助手</h3>
<p align="center">
  <a href="https://www.python.org/">
    <img src="https://img.shields.io/badge/Language-Python-blue?style=flat-square"/>
  </a>
  <a href="https://github.com/hualuoo/palworld-helper/releases">
    <img src="https://img.shields.io/badge/Release-V1.0.8-blue?style=flat-square"/>
  </a>
</p>
<h4 align="center">4小时用PyQt搓出来的小工具，交流Q群：209726238</h4>

![image](https://raw.githubusercontent.com/hualuoo/palworld_helper/main/images/img1.png)

## :sparkles: 特性
* :rocket: 极低占用，在EPYC 7T83双核VPS上CPU占用0.1%左右，内存20MB左右
* :cloud: 支持崩溃检测，服务端因内存溢出导致崩溃后将会自动重启服务端
* 💻 支持自动配置RCON，更加便携简单
* 💾 支持自动备份存档，防止因BUG或服务端崩溃导致存档损坏
* 📚 支持自动重启，预防长期未重启的服务端内存占用过大导致崩溃
* :family_woman_girl_boy: 自动重启支持人数检测，可避免玩家高峰期自动重启
* :link: 提供常见快捷指令，例如自动倒计时关服广播、踢出玩家等
* :eye_speech_bubble: (等待更新)存档修复
* :zap: 倍率等配置文件可视化修改
* :outbox_tray: (等待更新) 背包编辑
* :art: (后续计划) 迁移至flutter使界面更加美观
* 🌈 ... ...

## :hammer_and_wrench: BUG问题相关
由于该工具为边打CS边搓出来的小工具，为方便自身开服使用，仅花了5小时不到，未考虑优化等因素，如遇BUG，欢迎提交issues并注明出现错误的情景方便复现。
#### 报错查看建议使用如下源码执行的方式：
```shell
# 下载Python并安装：https://www.python.org/
# Git Clone或下载代码文件，以下以C:\Users\Administrator\Desktop\palworld-helper为例
# 打开cmd，cd进入代码路径
cd C:\Users\Administrator\Desktop\palworld-helper
# 安装PIP库依赖
pip install -r "C:\Users\Administrator\Desktop\palworld-helper\requirements.txt"
# 以源码方式运行
python "C:\Users\Administrator\Desktop\palworld-helper\main.py"
```
