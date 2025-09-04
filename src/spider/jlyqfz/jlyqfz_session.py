import time

import requests

from src.spider.jlyqfz.jlyqfz_login import JlyqfzLogin
from src.spider.jlyqfz.wis_eye_mask.feel_free_to_push_live import check_session
from src.utils.logintools import Session
from src.utils.tabtools import EasyTab


class JlyqfzSession(Session):
    def __init__(self, port: int, username: str, password: str, account: str):
        super().__init__(port, username)
        self._password = password
        self._account = account

    def _check(self, session: requests.Session):
        check_session(session)


    def _session(self) -> requests.Session:
        with JlyqfzLogin(self._port, self._username, self._password) as tab:
            time.sleep(3)
            tab.get('https://agent.oceanengine.com/admin/optimizeModule/dataSummary/bidding/bidding-adv')
            tab.wait.doc_loaded()
            et = EasyTab(tab.ele(f"x://div[@role='button' and text()='{self._account}']").click.for_new_tab())
            time.sleep(3)
            return et.session()
