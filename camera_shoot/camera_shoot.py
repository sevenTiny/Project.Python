import os
import time

if __name__ == '__main__':
    path = '/mnt/sda1'
    # path = 'E:\code\Project.Python\CameraShoot'
    folder = f'{path}/{time.strftime("%Y%m%d")}'

    if not os.path.exists(folder):
        os.mkdir(folder)

    # 拍照
    os.system(
        f'fswebcam --no-banner -r 1920*1080 --delay 3 --skip 10 {folder}/{time.strftime("%Y%m%d%H%M%S")}.jpg'
    )
