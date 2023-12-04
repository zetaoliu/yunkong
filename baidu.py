import uiautomator2 as u2
import time
import random



#
class Baidu:
    dd = 0
    ss = 0
    isFirstIn = True

    def __init__(self, item, isHomePage=False, isShopping=3, shopTime=10 * 60):
        self.d = u2.connect_usb(item)
        self.x = isHomePage  # 是否是金币页面[因为是金币页面是webview]
        self.s = isShopping
        self.t = shopTime

    # 关闭app
    def closeApp(self):
        self.d.app_stop('com.ss.android.ugc.aweme.lite')

    # 启动头条app
    def startApp(self):
        self.d.app_start('com.ss.android.ugc.aweme.lite')

    # 开始执行
    def startRun(self):
        self.startRun()


if __name__ == '__main__':
    douyin = Baidu("AKGR9K2914901715")
    douyin.startApp()
    print(douyin.startRun())
