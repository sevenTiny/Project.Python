from argparse import ArgumentError
from contextlib import closing
import os
import requests


class download_helper:
    def __init__(self):
        pass

    '''确保文件目录存在'''

    @staticmethod
    def _ensure_folder(file_full_name: str):
        if file_full_name is None:
            raise ArgumentError(file_full_name, "full name can not be none")

        folder = os.path.dirname(file_full_name)

        if not os.path.exists(folder):
            os.makedirs(folder)
            # print(f'{folder} created')

    @staticmethod
    def download(url, file_full_name):
        '''
            :param url: 下载url路径
            :return: 文件
            '''

        # 确保文件夹存在
        download_helper._ensure_folder(file_full_name)

        with closing(requests.get(url, stream=True)) as response:
            content_size = int(response.headers['content-length'])
            if (os.path.exists(file_full_name)
                    and os.path.getsize(file_full_name) == content_size):
                print(f'file [{file_full_name}] already exists')
            else:
                chunk_size = 1024
                progress = _ProgressBar(url,
                                        file_full_name,
                                        total=content_size,
                                        unit="KB",
                                        chunk_size=chunk_size,
                                        run_status="downloading...",
                                        fin_status="finished!")
                with open(file_full_name, "wb") as file:
                    for data in response.iter_content(chunk_size=chunk_size):
                        file.write(data)
                        progress.refresh(count=len(data))


'''
下载进度
'''


class _ProgressBar(object):
    def __init__(self,
                 url,
                 title,
                 count=0.0,
                 run_status=None,
                 fin_status=None,
                 total=100.0,
                 unit='',
                 sep='/',
                 chunk_size=1.0):
        super(_ProgressBar, self).__init__()
        self.info = "[%s] ==> [%s] %.2f %s %s %.2f %s %s"
        self.url = url
        self.title = title
        self.total = total
        self.count = count
        self.chunk_size = chunk_size
        self.status = run_status or ""
        self.fin_status = (fin_status or '').ljust(len(self.status))
        self.unit = unit
        self.seq = sep

    def __get_info(self):
        '''【名称】 进度 单位 分割线 总数 单位 状态'''
        return self.info % (self.url, self.title, self.count / self.chunk_size,
                            self.unit, self.seq, self.total / self.chunk_size,
                            self.unit, self.status)

    def refresh(self, count=1):
        self.count += count
        end_str = "\r"
        if self.count >= self.total:
            end_str = '\n'
            self.status = self.fin_status

        print(self.__get_info(), end=end_str)