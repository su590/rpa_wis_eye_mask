# -*- coding: utf-8 -*-  
"""
@Date     : 2025-02-20
@Author   : xwq
@Desc     : <None>

"""
import time

import requests

from src.spider.jlyq.jlyq_login import JlyqLogin
from src.spider.jlyqfz.wis_eye_mask.feel_free_to_push_live import check_session
from src.utils.logintools import Session
from src.utils.tabtools import EasyTab


class JlyqSession(Session):


    def __init__(self, port: int, username: str, password: str):
        super().__init__(port, username)
        self._password = password

    def _check(self, session: requests.Session):
        check_session(session)

    def _session(self) -> requests.Session:
        with JlyqLogin(self._port, self._username, self._password) as tab:
            time.sleep(1)
            return EasyTab(tab).session(
                'https://business.oceanengine.com/site/account-manage/ecp/bidding/standard/account'
            )
