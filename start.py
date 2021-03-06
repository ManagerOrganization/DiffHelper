# -*- coding:utf-8 -*-

import os
import platform
import sys
from distutils.version import StrictVersion

# 判断当前运行操作系统
if platform.system() != "Darwin":
    print("请在macOS操作系统运行该工具")
    os._exit(1)

parentPath = os.path.dirname(os.path.abspath(__file__))
if " " in parentPath:
    print(parentPath)
    print("工具所在的路径包含了空格,请移除路径中的空格后重试")
    os._exit(1)

# 需要安装的依赖以及对应的版本
kRequiredLib = {
    "biplist": "1.0.2",
    "filetype": "1.0.5",
    "lxml": "4.4.2",
    "nltk": "3.4.5",
    "ntplib": "0.3.3",
    "PyYAML": "5.1.2",
    "pyDes": "2.0.1",
    "pbxproj": "2.5.1",
    "Pillow": "6.1.0",
    "requests": "2.21.0",
}


# 获取当前系统版本
def curSystemVersion():
    output = os.popen("sw_vers | awk 'NR==2 {print $2}'")
    lines = output.readlines()
    output.close()
    line = "macOS: " + lines[0].strip()
    print(line)


# 判断当前运行python环境
def curPythonVersion():
    print("Python: %s" % (platform.python_version()))
    if platform.python_version() != "3.7.3":
        print("请确认在python3.7.3环境运行该工具")
        print("或者安装工具文件夹下的python3.7.3安装包(python-3.7.3-macosx10.9.pkg)")
        os._exit(1)


# pip3版本
def curPip():
    output = os.popen("pip3 -V")
    lines = output.readlines()
    output.close()
    if len(lines) == 0:
        print("检测到未安装pip3模块,现在开始安装......")
        os.system("sudo easy_install pip3")
    else:
        for line in lines:
            print(line.strip())


# 当前Xcode版本信息
def checkXcodeInstalled():
    output = os.popen("/usr/bin/xcodebuild -version")
    lines = output.readlines()
    output.close()
    if len(lines) == 0:
        print("请确认已经安装Xcode")
        os._exit(1)
    for line in lines:
        print(line.strip())


# 判断是否安装xcode-select
def checkXcodeSelect():
    output = os.popen("if xcode-select -p &>/dev/null; then echo 'installed'; else echo 'notInstall'; fi")
    content = output.readline()
    output.close()
    if content == "notInstall":
        print("当前未安装xcode-select,现在开始安装:")
        os.system("xcode-select --install")


# 获取当前pip3 list
def getPip3List():
    output = os.popen("pip3 list")
    lines = output.readlines()
    output.close()
    if len(lines) == 0:
        print("检测到未安装pip3模块,请重新运行当前脚本")
        print("或者安装工具文件夹下的python-3.7.3-macosx10.9.pkg后重试")
        os._exit(1)
    return lines


# 获取已经安装的依赖库
def getInstalledLib():
    lines = getPip3List()
    installedDict = {}
    for line in lines:
        line = line.strip()
        tmpList = line.split(" ")
        tmpList = [item for item in tmpList if len(item) > 0]
        if len(tmpList) == 2:
            lib = tmpList[0]
            version = tmpList[1]
            installedDict[lib] = version
    return installedDict


# 安装依赖库
def installLib(lib, requiredVersion):
    os.system("pip3 install %s==%s" % (lib, requiredVersion))


def operateEnvOK():
    installedDict = getInstalledLib()
    for lib in kRequiredLib:
        requiredVersion = kRequiredLib[lib]
        if lib in installedDict:
            curVersion = installedDict[lib]
            if StrictVersion(curVersion) < StrictVersion(requiredVersion):
                installLib(lib, requiredVersion)
        else:
            installLib(lib, requiredVersion)

    allInstalled = True
    installedDict = getInstalledLib()
    for lib in kRequiredLib:
        if lib not in installedDict:
            allInstalled = False
            break
    return allInstalled


def checkOperateEnv():
    print("*" * 32 + "开始检测运行环境" + "*" * 32)
    curSystemVersion()
    curPythonVersion()
    curPip()
    checkXcodeInstalled()
    checkXcodeSelect()
    time = 1
    print("Pip相关的警告可以忽略")
    while not operateEnvOK():
        if time == 1:
            print("首次运行将自动安装工具依赖")
        if time > 3:
            print("多次安装依赖库失败,请确认网络连接,重启终端重试")
            os._exit(1)
        else:
            print("\n运行环境不符合要求,正在安装依赖[%d]" % (time))
            operateEnvOK()
            time += 1
    print("*" * 32 + "运行环境符合要求" + "*" * 32)


checkOperateEnv()


toolPath = os.path.join(parentPath, "Tool")
sys.path.append(toolPath)

os.chdir(parentPath)

try:
    import JustDoIT
except Exception as exception:
    print("解决方案1:\n\t初次使用请重启终端再次运行")
    print("解决方案2:\n\t查看以下链接中常见错误3")
    print("\thttps://github.com/iOSCoderMaster/iOSCodeDifferHelper/wiki/%E5%B8%B8%E8%A7%81%E9%94%99%E8%AF%AF")
    print("解决方案3:\n\t输入python3,输入空格,将start.py文件拖到空格后面,输入回车")
    justDoITPath = os.path.join(toolPath, "JustDoIT.cpython-37m-darwin.so")
    if not os.path.exists(justDoITPath):
        print(justDoITPath)
        print("文件不存在")

if __name__ == "__main__":
    JustDoIT.justDoIT()
