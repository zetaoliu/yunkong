import threading
import device
import douyin
import toutiao
import time


def thread_function(item):
    toutiaoOp = toutiao.Toutiao(item)
    toutiaoOp.startApp()
    toutiaoOp.startRun()
    time.sleep(60)
    douyinOp = douyin.Douyin(item)
    douyinOp.startApp()
    douyinOp.startRun()
    time.sleep(60)


def runApp():
    devices_list = device.get_adb_devices()
    threads = []
    if isinstance(devices_list, list):
        for item in devices_list:
            # 创建线程对象
            threadOp = threading.Thread(target=thread_function, args=(item,))
            threads.append(threadOp)
            threadOp.start()
    else:
        print("no list")

    # 等待所有线程结束
    for thread in threads:
        thread.join()

    print("All threads have finished.")


runApp()
