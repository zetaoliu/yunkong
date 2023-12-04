import uiautomator2 as u2
import time
import random


# d = u2.connect()  # connect to device

class Toutiao:

    def __init__(self, item):
        self.d = u2.connect_usb(item)

    # 因为今日头条的是33000等于1块钱
    # 我们一天可以提现0.5
    # 所以大于9500就可以提现了【就可以关闭app】
    # 去开箱子的时候才可以检查
    # 视频返回的时候会重新刷新页面这个时候需要多下滑几下
    def isSuccess(self):
        # 9500就可以下一个app
        element = self.d.xpath('//*[contains(@text, "金币")]')
        money = element.get_text()
        number = money.replace('金币', '')
        if int(number) > 25000:
            return True
        else:
            return False

    # 关闭app
    def closeApp(self):
        self.d.app_stop('com.ss.android.article.lite')

    # 启动头条app
    def startApp(self):
        self.d.app_start('com.ss.android.article.lite')

    # 判断是否是主页
    def isHomePage(self):
        layer = self.d.dump_hierarchy()
        resourceId = 'android:id/tabs'
        # 判断是否存在首页标志元素
        if resourceId in layer and self.d(text="关注").exists and self.d(text="推荐").exists and self.d(
                text="热榜").exists and self.d(text="发现").exists and self.d(text="影视").exists:
            return True
        else:
            return False

    # 去首页
    def goHomePage(self):
        time.sleep(1)
        if self.d.xpath(
                '//*[@resource-id="android:id/tabs"]/android.widget.RelativeLayout[1]/android.widget.RelativeLayout['
                '1]/android.widget.FrameLayout[1]').exists:
            self.d.xpath(
                '//*[@resource-id="android:id/tabs"]/android.widget.RelativeLayout[1]/android.widget.RelativeLayout['
                '1]/android.widget.FrameLayout[1]').click()
        else:
          if self.d(description="返回").exists():
            self.d(description="返回").click()
            return
          if self.d(text="返回").exists():
            self.d(text="返回").click()
            return
        #   self.d.click(0.042, 0.059)
          self.d.click(0.056, 0.059)

    # 从内容页返回主页
    def backHome(self):
        time.sleep(3)
        if self.d(description="返回").exists():
            self.d(description="返回").click()
            return
        if self.d(text="残忍离开").exists():
            self.d(text="残忍离开").click()
            return
        self.d.click(0.056, 0.059)

    # 是否是内容页，还是直播页，还是啥页
    def isContentPage(self):
        time.sleep(5)
        # 小说
        if self.d(text="加入书架").exists:
            return 'book'

        # 搜索页
        if self.d(text="头条搜索精选").exists and self.d(text="大家都在搜").exists:
            return 'search'

        # 是否在内容页
        if self.d(description="返回").exists and self.d(description="听头条").exists and self.d(
                description="搜索").exists and self.d(description="更多操作").exists:
            return 'content'

        # 是否在视频页
        if self.d(description="返回").exists and self.d(description="音频").exists and self.d(
                description="更多操作").exists:
            return 'live'

        # 是否直播页
        if self.d(description="关闭").exists and self.d(text="更多直播").exists:
            return 'live'

        return 'none'

        # self.isContentPage()

    # 直播返回
    def liveBack(self):
        time.sleep(3)
        if self.d(description="返回").exists:
            self.d(description="返回").click()
            return
        if self.d(description="关闭").exists:
            self.d(description="关闭").click()
            time.sleep(5)
            if self.d(description="暂不使用").exists:
                self.d(description="暂不使用").click()
                return
        if self.d(text="暂不使用").exists:
            self.d(text="暂不使用").click()
            return
        if not self.isHomePage():
            time.sleep(3)
            self.liveBack()

    # 查询页面返回
    def searchBack(self):
        time.sleep(3)
        self.d(description="返回").click()
        time.sleep(3)
        if not self.isHomePage():
            self.searchBack()

    # 主页上下滑动
    def swapHomePage(self):
        time.sleep(2)
        rand = [0.3, 0.5, 0.6, 0.8]
        a = random.choice(rand)
        self.d.swipe_ext("up", a)

    # 随机点击内容
    def randClickContent(self):
        time.sleep(1)
        rand = [[0.42, 0.232], [0.392, 0.388], [0.396, 0.531], [0.388, 0.634],
                [0.39, 0.865]]
        a = random.choice(rand)
        self.d.click(a[0], a[1])

    # 内容阅读
    def contentRead(self):
        time.sleep(1)
        rand = [5, 8, 9, 10, 12, 9, 13, 15, 16, 17]
        count = random.choice(rand)
        for item in range(count):
            time.sleep(2)
            randNum = [0.1, 0.2, 0.3, 0.5, 0.6]
            a = random.choice(randNum)
            self.d.swipe_ext("up", a)

    # 滑动直播一个直播看1-2分钟
    def liveRead(self):
        time.sleep(1)
        rand = [1, 2]
        count = random.choice(rand)
        for item in range(count):
            timeSleep = [1 * 15, 1.5 * 15, 2 * 15]
            a = random.choice(timeSleep)
            time.sleep(a)
            self.d.swipe_ext("up", 1)

    # 是否有宝箱
    def isBox(self):
        time.sleep(1)
        layer = self.d.dump_hierarchy()
        resourceId = '开宝箱'
        # 判断是否存在首页标志元素
        if resourceId in layer:
            return True
        else:
            return False

    # 点击宝箱页面
    def clickBoxPage(self):
        time.sleep(1)
        self.d.click(0.426, 0.974)

    # 点击宝箱
    def clickBox(self):
        time.sleep(5)
        self.d(text="开宝箱得金币").click_exists()
        time.sleep(5)
        layer = self.d.dump_hierarchy()
        resourceId = '开心收下'
        # 判断是否存在首页标志元素
        if resourceId in layer:
            return
        else:
            self.clickBox()

    # 点击开心收下
    def clickDown(self):
        time.sleep(2)
        self.d.click(0.508, 0.6)
        # 这个有点久要延迟一个几秒
        time.sleep(3)
        layer = self.d.dump_hierarchy()
        resourceId = '开心收下'
        # 判断是否存在首页标志元素
        if resourceId in layer:
            self.clickDown()

    # 去阅读赚钱
    def goRead(self):
        time.sleep(5)
        if self.d(text="去阅读").exists():
            self.d(text="去阅读").click()
            return
        else:
            self.goHomePage()

    # 去视频赚钱
    def goVideo(self):
        time.sleep(5)
        self.d(text="视频赚钱").click_exists()

    # 去影视赚钱
    def goMovie(self):
        time.sleep(2)
        if self.d(text="看剧赚钱").exists():
            self.d(text="看剧赚钱").click()
        else:
            self.d.swipe_ext("up", 0.6)
            self.goMovie()

    # 点击影视观看
    def movDown(self):
        self.d.swipe_ext("down", 1)
        time.sleep(3)
        rand = [[0.236, 0.41], [0.748, 0.414], [0.208, 0.739], [0.734, 0.705]]
        a = random.choice(rand)
        self.d.click(a[0], a[1])

    # 5分钟关掉
    def movClose(self):
        time.sleep(5 * 60)
        self.backHome()

    # 返回推荐
    def backTuijian(self):
        self.d(text="推荐").click_exists()

    # 正常阅读
    def commonRead(self):
        self.swapHomePage()
        self.randClickContent()
        sw = self.isContentPage()
        if sw == 'search':
            self.searchBack()
        elif sw == 'book':
            self.backHome()
        elif sw == 'content':
            self.contentRead()
            self.backHome()
        elif sw == 'live':
            self.liveRead()
            self.liveBack()
        elif sw == 'none':
            self.backHome()

    # 影视操作
    def movOp(self):
        self.goMovie()
        self.movDown()
        self.movClose()
        self.backTuijian()

    # 开始执行
    def startRun(self):
        # self.startApp()
        homePage = self.isHomePage()
        if not homePage:
            self.goHomePage()

        box = self.isBox()

        if box:
            self.clickBoxPage()
            self.clickBox()
            self.clickDown()
            if self.isSuccess():
                self.closeApp()
                return
            # 1是阅读赚钱
            # 2是视频赚钱
            # 3是影视赚钱
            # 目前只有1可以赚钱
            rand = [1]

            a = random.choice(rand)

            if a == 1:
                self.goRead()
                self.commonRead()
            elif a == 2:
                self.goVideo()
                self.liveRead()
                self.liveBack()
            elif a == 3:
                self.movOp()
        else:
            self.commonRead()
        self.startRun()


if __name__ == '__main__':
    toutiao = Toutiao("AKGR9K2914901715")
    toutiao.startApp()
    print(toutiao.startRun())

