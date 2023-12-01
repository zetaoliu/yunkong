import subprocess


def get_adb_devices():
    try:
        # 执行 adb devices 命令
        result = subprocess.check_output(['adb', 'devices']).decode('utf-8')
        lines = result.strip().split('\n')

        # 解析设备列表
        devices = []
        for line in lines[1:]:
            parts = line.split('\t')
            if len(parts) == 2 and parts[1] == 'device':
                devices.append(parts[0])

        return devices

    except subprocess.CalledProcessError as e:
        print(f'Error executing adb command: {e}')
        return []


class Device:
    pass
