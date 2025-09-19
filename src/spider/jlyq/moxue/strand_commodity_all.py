import datetime
import json
import logging

import requests

from src.sql.moxue_timeframe import MoxueTimeframe
from src.utils.trycatchtools import catch_errors


def _search_in_strand_commodity_all_plain(session: requests.Session, x_csrftoken: str, search_word: str = "") -> tuple[float, float]:
    """
    在 标准-推商品-全部-计划  -> 筛选计划状态：全部（包含已删除）
    Args:
        session:
        x_csrftoken: 从cookie当中提取
        search_word: 进行筛选的关键字

    Returns: consumption，roi

    """
    url = "https://business.oceanengine.com/nbs/api/bm/promotion/ecp/get_ad_list"
    begin_date = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
    end_date = datetime.datetime.combine(datetime.date.today(), datetime.time.max)

    payload = json.dumps({
        "start_time": f"{int(begin_date.timestamp())}",
        "end_time": f"{int(end_date.timestamp()) + 1}",
        "cascade_metrics": [
            "ad_bid",
            "ad_budget"
        ],
        "fields": [
            "stat_cost",
            "all_order_pay_roi_7days",
            "show_cnt",
            "ctr",
            "prepay_and_pay_order_roi",
            "stat_pay_order_amount",
            "stat_indirect_order_pay_gmv_7days"
        ],
        "order_field": "create_time",
        "order_type": 1,
        "offset": 1,
        "limit": 10,
        "account_type": 80,
        "filter": {
            "advertiser": {},
            "group": {},
            "campaign": {
                "marketingGoal": [
                    1,
                    2
                ]
            },
            "ad": {
                "ecpAdStatus": [
                    30
                ]
            },
            "search": {
                "keyword": search_word,
                "searchType": 2,
                "queryType": "phrase"
            }
        }
    })
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'content-type': 'application/json',
        'origin': 'https://business.oceanengine.com',
        'priority': 'u=1, i',
        'sec-ch-ua': '"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
        'x-csrftoken': x_csrftoken
    }

    response = session.request("POST", url, headers=headers, data=payload)
    response_json = response.json()
    consumption = response_json["data"]["total_metrics"]["stat_cost"]
    roi = response_json["data"]["total_metrics"]["all_order_pay_roi_7days"]

    search_info = f"筛选{search_word}" if search_word else "不筛选"
    logging.info(
        f"墨雪在标准-商品-全部-计划当中{search_info}得到的消耗、roi：{consumption}、{roi}"
    )

    return consumption, roi

@catch_errors("在标准-商品-全部-计划中搜索小店获取消耗、roi失败")
def xiao_dian(session: requests.Session, moxue_timeframe: MoxueTimeframe):
    """
    搜索小店
    Args:
        moxue_timeframe:
        session:

    Returns:

    """
    x_csrftoken = session.cookies['csrftoken']
    search_word = "小店"
    moxue_timeframe.xiao_dian_cost, moxue_timeframe.xiao_dian_roi = _search_in_strand_commodity_all_plain(session, x_csrftoken, search_word)

@catch_errors("在标准-商品-全部-计划中搜索加热获取消耗、roi失败")
def hot(session: requests.Session, moxue_timeframe: MoxueTimeframe):
    """
    搜索加热
    Args:
        moxue_timeframe:
        session:

    Returns:

    """
    x_csrftoken = session.cookies['csrftoken']
    search_word = "加热"
    moxue_timeframe.jia_re_cost, moxue_timeframe.jia_re_roi = _search_in_strand_commodity_all_plain(session, x_csrftoken, search_word)

@catch_errors("在标准-商品-全部-计划中获取消耗、roi失败")
def total(session: requests.Session, moxue_timeframe: MoxueTimeframe):
    """
    拿到全部的
    Args:
        moxue_timeframe:
        session:

    Returns:

    """
    x_csrftoken = session.cookies['csrftoken']
    moxue_timeframe.short_video_consumption, moxue_timeframe.short_video_roi = _search_in_strand_commodity_all_plain(session, x_csrftoken)
