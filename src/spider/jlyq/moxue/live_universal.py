import datetime
import json
import logging

import requests

from src.sql.moxue_timeframe import MoxueTimeframe
from src.utils.trycatchtools import catch_errors


def _get_live_universal(session: requests.Session, avvid: str):
    """
    获取直播全域下面的三个数据：直播间累计消耗、直播间ROI、直播全域智能优惠券
    Args:
        session:
        avvid: 直接点击对应的账户再url当中拿到

    Returns:

    """
    begin_str = datetime.datetime.combine(datetime.date.today(), datetime.time.min).strftime("%Y-%m-%d %H:%M:%S")
    end_str = datetime.datetime.combine(datetime.date.today(), datetime.time.max).strftime("%Y-%m-%d %H:%M:%S")


    url = ("https://qianchuan.jinritemai.com/ad/api/data/v1/common/statQuery?"
           f"aavid={avvid}")

    payload = json.dumps({
        "Dimensions": [
            "marketing_goal"
        ],
        "StartTime": f"{begin_str}",
        "EndTime": f"{end_str}",
        "DataSetKey": "site_promotion_post_overview",
        "Metrics": [
            "stat_cost",
            "total_prepay_and_pay_order_roi2",
            "total_pay_order_coupon_amount_for_roi2",
            "total_pay_order_gmv_for_roi2",
            "total_pay_order_count_for_roi2"
        ],
        "Filters": {
            "ConditionRelationshipType": 1,
            "Conditions": [
                {
                    "Field": "advertiser_id",
                    "Operator": 7,
                    "Values": [
                        f"{avvid}"
                    ]
                },
                {
                    "Field": "pricing_category",
                    "Operator": 7,
                    "Values": [
                        "2"
                    ]
                },
                {
                    "Field": "marketing_goal",
                    "Operator": 7,
                    "Values": [
                        "2"
                    ]
                },
                {
                    "Field": "ecp_app_id",
                    "Operator": 7,
                    "Values": [
                        "1"
                    ]
                },
                {
                    "Field": "campaign_type",
                    "Operator": 7,
                    "Values": [
                        "1"
                    ]
                },
                {
                    "Field": "adlab_mode",
                    "Operator": 7,
                    "Values": [
                        "1"
                    ]
                }
            ]
        },
        "FilterParams": {
            "promotion_overview": [
                "1"
            ]
        },
        "aavid": f"{avvid}"
    })
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'content-type': 'application/json',
        'priority': 'u=1, i',
        'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
    }

    response = session.request("POST", url, headers=headers, data=payload).json()
    totals = response['data']['StatsData']['Totals']
    coupon = totals['total_pay_order_coupon_amount_for_roi2']['Value']
    roi = totals['total_prepay_and_pay_order_roi2']['Value']
    cost = totals['stat_cost']['Value']
    logging.info(f"墨雪直播全域消耗、roi、优惠劵：{cost}、{roi}、{coupon}")
    return cost, roi, coupon

@catch_errors("获取直播间全域数据失败")
def get_live_universal(session: requests.Session, moxue_timeframe: MoxueTimeframe):
    avvid = "1728784932773000"
    moxue_timeframe.live_room_timeframe_consumption, moxue_timeframe.live_room_timeframe_cost_roi, moxue_timeframe.smart_coupon = _get_live_universal(session, avvid)

def get_constitution_live(session: requests.Session, moxue_timeframe: MoxueTimeframe):
    avvid = '1834617161038346'
    moxue_timeframe.constitution_consumption, moxue_timeframe.constitution_roi, _ = _get_live_universal(session, avvid)

