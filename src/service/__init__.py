import dataclasses
import json
import os

@dataclasses.dataclass
class _Account:
    username: str
    port: int
    brand: str

    def show(self) -> dict:
        dct = self.__dict__.copy()
        if dct.get("password") is not None:
            dct["password"] = "*" * len(dct["password"] or 1)
        return dct

@dataclasses.dataclass
class _DslpAccount(_Account):
    shop: str

def get_dslp_account(brand: str) -> _DslpAccount | None:
    path = os.path.join(os.path.dirname(__file__).split('src')[0], 'src', 'config/dslp_account.json')
    with open(path, 'r', encoding='utf-8') as f:
        acc_lst: list[dict] = json.load(f)
        for x in acc_lst:
            if x['brand'] == brand:
                return _DslpAccount(**x)
    return None

@dataclasses.dataclass
class _JlyqAccount(_Account):
    password: str

def get_jlyq_account(brand: str, is_normal: bool = True) -> _JlyqAccount | None:
    """

    Args:
        brand:
        is_normal: True为获取常规的巨量引擎，False为获取巨量引擎方舟

    Returns:

    """
    plat = "jlyq_account" if is_normal else "jlyqfz_account"
    path = os.path.join(os.path.dirname(__file__).split('src')[0], 'src', f'config/{plat}.json')
    with open(path, 'r', encoding='utf-8') as f:
        acc_lst: list[dict] = json.load(f)
        for x in acc_lst:
            if x['brand'] == brand:
                return _JlyqAccount(**x)
    return None

@dataclasses.dataclass
class _JlyqfzAccount(_Account):
    password: str
    account: str
def get_jlyqfz_account(brand: str) -> _JlyqfzAccount | None:
    """
    获取巨量引擎方舟的登录信息
    在登录进入巨量引擎方舟之后 进入如下url：
    'https://agent.oceanengine.com/admin/optimizeModule/dataSummary/bidding/bidding-adv'
    然后在此选择账户获取各个账户之下不同的session
    :param brand:  品牌
    :return: 
    """
    path = os.path.join(os.path.dirname(__file__).split('src')[0], 'src', 'config/jlyqfz_account.json')
    with open(path, 'r', encoding='utf-8') as f:
        acc_list: list[dict] = json.load(f)
        for x in acc_list:
            if x['brand'] == brand:
                return _JlyqfzAccount(**x)
    return None
