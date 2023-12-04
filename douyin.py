import uiautomator2 as u2
import time
import random
import redistool


# 描述
# 看视频最多900
# 逛街赚钱10分钟一次，可以领三次
# 一个小时就够了差不多
# 3000就可以关app

class Douyin:

    def __init__(self, item, shopTime=10 * 60):
        self.phoneKey = item
        self.d = u2.connect_usb(item)
        self.redis = redistool.RedisTool()
        # 购物时间
        self.redis.set(f'{item}dd', 0)
        # 检查宝箱时间
        self.redis.set(f'{item}ss', 0)

        self.redis.set(f'{item}isHomePage', 1)  # 是否是金币页面[因为是金币页面是webview]

        self.redis.set(f'{item}isShopping', 0)  # 逛街可以领三次

        # 逛街间隔时间是600
        self.t = shopTime

    # 关闭app
    def closeApp(self):
        self.d.app_stop('com.ss.android.ugc.aweme.lite')
        self.cleanCache()

    def cleanCache(self):
        self.redis.delKey(self.phoneKey)

    # 启动头条app
    def startApp(self):
        self.d.app_start('com.ss.android.ugc.aweme.lite')
        time.sleep(5)

    # 是否在首页
    def isHomePage(self):
        if int(self.redis.get(f'{self.phoneKey}isHomePage')) == 0:
            return False
            # 判断是否存在首页标志元素
        if self.d(text="首页").exists and self.d(text="朋友").exists and self.d(text="消息").exists and self.d(
                text="我").exists:
            return True
        else:
            return False

    # 判断金币收益是否大于3000
    def isSuccess(self):
        if int(self.redis.get(f'{self.phoneKey}isHomePage')) == 1:
            self.d.click(0.196, 0.155)
            if self.checkMoney():
                time.sleep(3)
                self.d.swipe_ext("right", 1)
                return True
        return False

    # 查看金额是否大于3000
    def checkMoney(self):
        time.sleep(5)
        # 9500就可以下一个app
        element = self.d.xpath('//*[contains(@text, "金币收益")]')
        money = element.get_text()
        number = money.replace('金币收益', '')
        if int(number) > 3000:
            return True
        else:
            return False

    # 侧滑返回到首页
    def sideSlip(self):
        time.sleep(3)
        self.d.swipe_ext("right", 1)
        self.redis.set(f'{self.phoneKey}isHomePage', 0)

    # 查看视频
    # 因为看这个视频是有钱的可以多看点
    def readVideo(self):
        time.sleep(1)
        rand = [1, 2, 3, 4, 5]
        count = random.choice(rand)
        for item in range(count):
            timeSleep = [1 * 15, 1.5 * 15, 2 * 15]
            a = random.choice(timeSleep)
            time.sleep(a)
            self.d.swipe_ext("up", 1)

        # 是否有开宝箱

    def checkBox(self):
        jj = int(time.time())
        if int(jj - int(self.redis.get(f'{self.phoneKey}ss'))) > 20 * 60:
            self.redis.set(f'{self.phoneKey}ss', jj)
            return True
        if self.d(text="开宝箱").exists:
            self.redis.set(f'{self.phoneKey}ss', jj)
            return True

        return False

        # 跳转到宝箱页面

    def clickBoxPage(self):
        time.sleep(3)
        self.d.click(0.504, 0.959)
        self.redis.set(f'{self.phoneKey}isHomePage', 1)

    # 点击宝箱
    def clickBox(self):
        time.sleep(5)
        self.d.click(0.838, 0.942)

    # 关闭宝箱
    def closeBox(self):
        time.sleep(3)
        self.d.click(0.504, 0.746)

    # 查找逛街赚钱
    def searchShopping(self):
        time.sleep(3)
        self.d.swipe_ext("up", 0.2)
        time.sleep(3)
        self.d.click(0.442, 0.826)
        self.redis.decr(f'{self.phoneKey}isShopping')

    # 逛街
    # 60-70
    def readShopping(self):
        rand = [60, 65, 70]
        count = random.choice(rand)
        i = 0
        for item in range(100):
            if self.isSuccessReadFinish():
                self.closeSuccessWindow()
                return
            timeSleep = [1, 2, 3]
            a = random.choice(timeSleep)
            time.sleep(a)
            self.d.swipe_ext("up", 0.3)
            i = i + a
            if i >= count:
                return

    def isSuccessReadFinish(self):
        time.sleep(1)
        element = self.d.xpath('//*[contains(@text, "已获得")]')
        if element.exists:
            return True
        return False

    def closeSuccessWindow(self):
        time.sleep(3)
        self.d.click(0.804, 0.36)

        # 关闭逛街

    def closeShopping(self):
        time.sleep(3)
        self.d.swipe_ext("right", 1)
        time.sleep(1)
        element = self.d.xpath('//*[contains(@text, "坚持退出")]')
        if element.exists:
            self.d(text='坚持退出').click()
        time.sleep(3)
        self.d.swipe_ext("down", 1)
        self.redis.set(f'{self.phoneKey}dd', int(time.time()))

    # 第一次进来还是要判断一下是否金额已经超过3000
    def checkFirstMoneyIn(self):
        self.clickBoxPage()
        time.sleep(3)
        self.d.click(0.196, 0.155)
        if self.isSuccess():
            self.sideSlip()
            return True
        return False

    # 开始执行
    def startRun(self):
        if not self.isHomePage():
            self.sideSlip()

        if self.checkFirstMoneyIn():
            self.closeApp()
            return
        else:
            self.sideSlip()
            self.sideSlip()
        self.readVideo()
        if self.checkBox():
            self.clickBoxPage()
            self.clickBox()
            self.closeBox()
            tt = int(time.time())
            if int(self.redis.get(f'{self.phoneKey}isShopping')) > 0 and (
                    tt - int(self.redis.get(f'{self.phoneKey}dd')) > self.t):
                self.searchShopping()
                self.readShopping()
                self.closeShopping()
                self.sideSlip()  # 回到首页
            # 判断是否超过了金币收益
            if int(self.redis.get(f'{self.phoneKey}isShopping')) == 0:
                if self.isSuccess():
                    self.sideSlip()
                    return

        self.startRun()


if __name__ == '__main__':
    douyin = Douyin("AKGR9K2914901715")
    douyin.startApp()
    print(douyin.startRun())
