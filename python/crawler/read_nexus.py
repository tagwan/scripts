# -*- coding: utf-8 -*-

import os
import re
import json
import sys
import shutil

try:
    import requests
except ImportError:
    print("ERROR: not install package: \"requests\"")

"""
获取协议包最大版本+1，并自动写入到build.gradle.kts中，可拷贝至客户端协议文件夹
"""

CONST_URL = "http://192.168.189.16:16000/service/extdirect"

header = {
    'User-Agent': 'Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'Content-Type': 'application/json',
    'cookie': '__author__:jdg'
}

postData = {
    'action': "coreui_Browse",
    'method': "read",
    'data': [{"repositoryName": "topg-releases", "node": "com/point18/conquer/base-protocol"}],
    'type': "rpc",
    'tid': 10
}


class ReadNexus(object):
    def __init__(self):
        self.url = CONST_URL
        self.heard = header
        self.postData = postData

    def checkVersionIsTrue(self, version) -> bool:
        """
        版本号格式是否正确
        :param version:
        :return:
        """
        check = re.match("\d+(\.\d+){0,2}", version)
        if check is None or check.group() != version:
            return False
        return True

    def checkIsMoreThan(self, v1="1.0.1", v2="1.2") -> bool:
        """
        格式化的字符串比较大小
        :param v1:
        :param v2:
        :return:
        """
        v1_list = v1.split(".")
        v2_list = v2.split(".")
        v1_len = len(v1_list)
        v2_len = len(v2_list)
        if v1_len > v2_len:
            for i in range(v1_len - v2_len):
                v2_list.append("0")
        elif v2_len > v1_len:
            for i in range(v2_len - v1_len):
                v1_list.append("0")
        else:
            pass
        for i in range(len(v1_list)):
            if int(v1_list[i]) > int(v2_list[i]):
                return True
            if int(v1_list[i]) < int(v2_list[i]):
                return False
        return False

    def quickSort(self, arr):
        """
        快排
        :param arr:
        :return:
        """
        if len(arr) < 2:
            return arr
        mid = arr[len(arr) // 2]
        left, right = [], []
        arr.remove(mid)
        for item in arr:
            if self.checkIsMoreThan(v1=item, v2=mid):
                right.append(item)
            else:
                left.append(item)
        return self.quickSort(left) + [mid] + self.quickSort(right)

    def getNowVersion(self) -> int:
        response = requests.post(self.url, json=self.postData).text
        fileMap = json.loads(response)
        dataList = fileMap["result"]["data"]
        versionList = list()

        for v in dataList:
            version = v['text']
            if self.checkVersionIsTrue(version):
                versionList.append(version)

        versionSortList = self.quickSort(versionList)
        maxVersion = versionSortList[-1]
        return maxVersion

    def getMaxVersion(self, nowVersion) -> str:
        """
        最大版本号
        :param nowVersion:
        :return:
        """
        versionList = nowVersion.split('.', 2)
        versionList[-1] = str(int(versionList[-1]) + 1)
        return ".".join(versionList)

    def run(self) -> None:
        """
        run
        :return:
        """
        nowVersion = self.getNowVersion()
        version = self.getMaxVersion(nowVersion)
        pattern = '^[ ]*version.*?"$'
        fileName = "build.gradle.kts"

        readFile = open(fileName, "r", encoding="utf8")
        allLines = readFile.readlines()
        readFile.close()

        with open(fileName, "w+", encoding="utf8") as file:
            for eachLine in allLines:
                writeLine = eachLine
                if (re.match(pattern, eachLine)):
                    versionList = eachLine.split("\"")
                    versionList[1] = "\"{}\"".format(version)
                    writeLine = "".join(versionList)

                file.writelines(writeLine)


class MoveFile:
    def __init__(self, targetPath):
        self.source = r".\protocol\src\main\proto\client2server.proto"
        self.targetPath = targetPath

    def run(self):
        if not os.path.isdir(self.targetPath):
            print("ERROR:客户端协议地址没找到{path}".format(path=self.targetPath))
            exit(1)
        try:
            shutil.copy(self.source, self.targetPath)
        except IOError as e:
            print("ERROR:Unable to copy file. %s" % e)
        except:
            print("Unexpected ERROR:", sys.exc_info())


if __name__ == '__main__':
    targetPath = r"D:\workspace\client\Proto"

    cmdList = sys.argv

    if len(cmdList) <= 1:
        ReadNexus().run()
    else:
        cmd = sys.argv[1]
        MoveFile(targetPath).run()
