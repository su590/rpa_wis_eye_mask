import time

from DrissionPage._pages.chromium_tab import ChromiumTab
from DrissionPage.errors import WaitTimeoutError

from src.utils.logintools import Login
from src.utils.tabtools import EasyTab


def _is_logined(tab: ChromiumTab) -> bool:
    tab.listen.start('https://agent.oceanengine.com/agent/user/profile-info/')
    tab.get('https://agent.oceanengine.com/admin/profile')
    try:
        dp = tab.listen.wait(timeout=10, raise_err=True)
    except WaitTimeoutError:
        return False
    return True

def _login(username: str, password: str, tab: ChromiumTab):
    et = EasyTab(tab)

    # 初始化
    et.get("https://agent.oceanengine.com/login")

    # 账密
    et.click('x://div[contains(@class, "switch-switch") and text()="邮箱登录"]')
    et.input('c:input[name="email"]', username)
    et.input('c:input[name="password"]', password)
    et.click('c:use[fill="#FFF"][fill-opacity=".01"]')
    # 确认
    et.click('c:button.account-center-action-button.active')
    time.sleep(3)


    
class JlyqfzLogin(Login):

    def __init__(self, port: int, username: str, password: str):
        super().__init__(port, username)
        self._password = password

    def _login(self, tab: ChromiumTab) -> None:
        if _is_logined(tab):
            time.sleep(.5)
            return
        _login(self._username, self._password, tab)
        time.sleep(.5)

if __name__ == '__main__':
    pass