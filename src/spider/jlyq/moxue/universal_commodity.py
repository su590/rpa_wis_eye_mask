import datetime
import logging

import requests
import json

from src.sql.moxue_timeframe import MoxueTimeframe
from src.utils.trycatchtools import catch_errors


def _get_universal_commodity_by_account(session: requests.session, avvid: str) -> tuple[float, float]:
    """
    在全域商品当中进入某个账户，然后拿到账户当中的消耗、roi
    Args:
        session:
        avvid: 账户的唯一标识

    Returns:

    """
    start_time = datetime.datetime.combine(datetime.date.today(), datetime.time().min).strftime('%Y-%m-%d %H:%M:%S')
    end_time = datetime.datetime.combine(datetime.date.today(), datetime.time().max).strftime('%Y-%m-%d %H:%M:%S')

    url = f"https://qianchuan.jinritemai.com/ad/api/pmc/v1/standard/get_summary_info?aavid={avvid}&gfversion=1.0.0.1441"

    payload = json.dumps({
        "mar_goal": 1,
        "dataSetKey": "product_roi2_promotion",
        "page": 1,
        "page_size": 10,
        "order_by_type": 2,
        "order_by_field": "create_time",
        "start_time": start_time,
        "end_time": end_time,
        "smartBidType": 0,
        "ad_cost_status": -1,
        "ad_status_filter_type": 0,
        "metrics": "stat_cost_for_roi2,stat_cost_for_roi2_primary,total_prepay_and_pay_order_roi2,total_prepay_and_pay_order_roi2_primary,total_pay_order_count_for_roi2,total_pay_order_count_for_roi2_primary,total_pay_order_gmv_for_roi2,total_pay_order_gmv_for_roi2_primary,total_cost_per_pay_order_for_roi2,total_cost_per_pay_order_for_roi2_primary,total_pay_order_coupon_amount_for_roi2,total_pay_order_coupon_amount_for_roi2_primary",
        "adlab_mode": 1,
        "smart_bid_type": 0,
        "aavid": avvid
    })
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'content-type': 'application/json',
        'priority': 'u=1, i',
        'sec-ch-ua': '"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
    }

    response = session.request("POST", url, headers=headers, data=payload)
    response_json = response.json()
    consumption = response_json["data"]["totalMetrics"]["metrics"]["statCostForRoi2"]["value"]
    roi = response_json["data"]["totalMetrics"]["metrics"]["totalPrepayAndPayOrderRoi2"]["value"]
    logging.info(f"墨雪在全域-商品-账号：{avvid}下的消耗、roi:{consumption}、{roi}")
    return consumption, roi

@catch_errors("在全域-商品-账号下获取纯佣失败")
def chun_yong(session: requests.session, moxue_timeframe: MoxueTimeframe):
    """
    纯佣 上海九和06
    Args:
        moxue_timeframe:
        session:

    Returns:

    """
    avvid = "1765688797360135"
    moxue_timeframe.chunyong_consumption, moxue_timeframe.chunyong_roi = _get_universal_commodity_by_account(session, avvid)

@catch_errors("在全域-商品-账号下获取分发失败")
def fen_fa(session: requests.session, moxue_timeframe: MoxueTimeframe):
    """
    墨雪 - 博采 - 5
    Args:
        moxue_timeframe:
        session:

    Returns:

    """
    avvid = "1835884772677003"
    moxue_timeframe.fenfa_consumption, moxue_timeframe.fenfa_roi = _get_universal_commodity_by_account(session, avvid)

@catch_errors("在全域-商品-账号下获取染发失败")
def ran_fa(session: requests.session, moxue_timeframe: MoxueTimeframe):
    """
    染发 引力2
    Args:
        moxue_timeframe:
        session:

    Returns:

    """
    avvid = "1769657616904199"
    moxue_timeframe.ranfa_consumption, moxue_timeframe.ranfa_roi = _get_universal_commodity_by_account(session, avvid)

@catch_errors("在全域-商品-账号下获取全域消耗、roi失败")
def universal(session: requests.session, moxue_timeframe: MoxueTimeframe):
    """
    品创部墨雪-博彩-6
    Args:
        session:
        moxue_timeframe:

    Returns:

    """
    avvid = "1728785181002766"
    moxue_timeframe.short_video_university_consumption, moxue_timeframe.short_video_university_roi = _get_universal_commodity_by_account(session, avvid)

@catch_errors("获取付费达人数据失败")
def paid_influencer(session: requests.session, moxue_timeframe: MoxueTimeframe):
    """
    品创部墨雪-博采-3
    付费达人
    Args:
        session:
        moxue_timeframe:

    Returns:

    """
    avvid = "1835884649814410"
    moxue_timeframe.paid_influencer_cost, moxue_timeframe.paid_influencer_roi = _get_universal_commodity_by_account(session, avvid)

if __name__ == '__main__':
    pass