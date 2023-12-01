import subprocess

import device


# 执行云端
def execute_scrcpy(serial):
    try:
        command = ['scrcpy', '-s', serial]
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        if process.returncode == 0:
            print("scrcpy command executed successfully.")
        else:
            print(f"scrcpy command failed with error: {stderr.decode('utf-8')}")

    except Exception as e:
        print(f"Error executing scrcpy command: {e}")


class Cloud:

    def run_scrcpy(self):
        if isinstance(self, list):
            for item in self:
                execute_scrcpy(item)
        else:
            print("no list")


if __name__ == '__main__':
    # 调用函数获取设备列表
    devices_list = device.get_adb_devices()
    Cloud.run_scrcpy(devices_list)

