import os
import stat
import time

from adb_shell.adb_device import AdbDeviceUsb
from adb_shell.auth.sign_pythonrsa import PythonRSASigner
from sty import fg

##################################################################################


class AdbUtil:
    def __init__(self):
        self._device = None
        self._path = "/storage/emulated/0"

    def _prepareAndroidKey(self):
        adbkey = "/Users/ting/.android/adbkey"
        with open(adbkey) as f:
            priv = f.read()

        with open(adbkey + ".pub") as f:
            pub = f.read()

        return PythonRSASigner(pub, priv)

    def connectDevice(self):
        if self._device is None:
            self._device = AdbDeviceUsb()
            self._device.connect(rsa_keys=[self._prepareAndroidKey()], auth_timeout_s=3)
            self.lsCmd()

    def closeDevice(self):
        if self._device:
            self._device.close()

    def lsCmd(self):
        response = self._device.shell("ls " + self._path)
        print(fg.li_cyan + "$ " + self._path + fg.rs + "\r\n")
        print(fg.blue + response + fg.rs)

    def lslaCmd(self):
        response = self._device.list(self._path)
        print(fg.li_cyan + "$ " + self._path + fg.rs)
        print(fg.blue)
        for l in response:
            print(
                "{:<8} {:<15} {:<30} {:<10}".format(
                    stat.filemode(l.mode),
                    l.size,
                    time.ctime(l.mtime),
                    l.filename.decode("utf-8"),
                )
            )
        print(fg.rs)

    def go(self, path: str):
        response = self._device.shell("cd " + self._path + "/" + path)
        if response is None or response == "":
            self._path = self._path + "/" + path
            self.lsCmd()
        else:
            print(fg.red + response + fg.rs)
            self.lsCmd()

    def back(self):
        ind = self._path.rindex("/")
        self._path = self._path[0:ind]
        self.lsCmd()

    def pullCmd(self, file):
        response = self._device.shell(
            "test -f " + self._path + "/" + file + " && echo OK"
        )
        if response is None or response == "":
            print(fg.red + "Get File Not Found" + fg.rs, response)
        else:
            response = self._device.pull(self._path + "/" + file, "./" + file)
            print(fg.green + "Done" + fg.rs)

    def pushCmd(self, file):
        if os.path.exists(file):
            filename = os.path.basename(file)
            response = self._device.push(file, self._path + "/" + filename)
            if response is not None and response != "":
                print(fg.red + "Up File Error" + fg.rs, response)
            else:
                print(fg.green + "Done" + fg.rs)
                self.lsCmd()
        else:
            print(fg.red + "Source File Not Found" + fg.rs)

    def delCmd(self, file):
        response = self._device.shell(
            "test -f " + self._path + "/" + file + " && echo OK"
        )
        if response is None or response == "":
            print(fg.red + "Delete File Not Found" + fg.rs, response)
        else:
            response = self._device.shell("rm " + self._path + "/" + file)
            print(fg.green + "Done" + fg.rs)
            self.lsCmd()


##################################################################################


def main():

    adbUtil = AdbUtil()

    while True:
        inval = input(fg(118) + "adb> " + fg.rs)
        cmds = inval.split(" ", 1)
        cmd = cmds[0]
        # print(fg.yellow + str(cmds) + fg.rs)
        if cmd == "\q":
            print(fg(207) + "Bye ~" + fg.rs)
            break
        elif cmd != "":
            if cmd == "\c":
                adbUtil.connectDevice()
            elif cmd == "\<":
                adbUtil.back()
            elif cmd == "\l":
                adbUtil.lsCmd()
            elif cmd == "\la":
                adbUtil.lslaCmd()
            else:
                if len(cmds) < 2:
                    print(fg.red + "Cmd missed param" + fg.rs)
                else:
                    if cmd == "\>":
                        adbUtil.go(cmds[1])
                    elif cmd == "\get":
                        adbUtil.pullCmd(cmds[1])
                    elif cmd == "\\up":
                        adbUtil.pushCmd(cmds[1])
                    elif cmd == "\del":
                        adbUtil.delCmd(cmds[1])


##################################################################################


if __name__ == "__main__":
    main()
