# -*- coding: utf-8 -*-  
"""
@Date     : 2025-02-20
@Author   : xwq
@Desc     : <None>

"""
import json
import os.path
from typing import Callable

from DrissionPage import ChromiumPage, ChromiumOptions

from src.config import DSP_DOWNLOAD_PATH, DSP_USER_DATA_PATH
from src.utils.dsptools import dsptools


def _mkfolder(folder: str, subfolder: str) -> str:
    """
    获取子目录，无则新建
    :param folder: 父目录绝对地址
    :param subfolder: 子目录名，如 xxx 或 xxx/yyy
    :return:
    """
    dstfolder = os.path.join(folder, subfolder)
    if not os.path.exists(dstfolder):
        os.makedirs(dstfolder)
    return dstfolder


def _exoptions(port: int) -> Callable[[ChromiumOptions], ChromiumOptions]:
    def func(co: ChromiumOptions) -> ChromiumOptions:
        ip = '127.0.0.1'
        co.set_paths(address=f'{ip}:{port}')

        download_path: str = DSP_DOWNLOAD_PATH
        co.set_paths(download_path=_mkfolder(download_path, str(port)))

        user_data_path: str = DSP_USER_DATA_PATH
        co.set_paths(user_data_path=_mkfolder(user_data_path, str(port)))

        # co.headless()
        return co

    return func


def get_page(port: int = None) -> ChromiumPage:
    if (port is None) or (port == -1):
        return dsptools.page()
    else:
        return dsptools.page(_exoptions(port))


def _test():
    page = get_page(9520)
    page.ele('c:.auxo-select-selection-item').click()
    # tab = page.latest_tab
    # print(tab.url)
    # # tab.scroll.to_bottom()
    # tab.ele('c:[id="gar-sub-app-provider"]').get_screenshot('D:/test4.jpg', scroll_to_center=False)
    # # tab.ele('c:[class*=compare] .ecom-select-selection-item').click()
    pass


if __name__ == '__main__':
    _test()
    pass
