import datetime
import logging

import requests
import json

from src.sql.moxue_timeframe import MoxueTimeframe
from src.utils.trycatchtools import catch_errors


def _get_live_room_scenery(session: requests.Session, avvid: str) -> tuple[float, float]:
    """
    在全域推广-推直播间当中选择一个账号进入，选择其中的一个直播间，拿到直播间画面当中的整体消耗、整体支付roi
    Args:
        session:
        avvid: 账号唯一标识

    Returns:

    """
    start_time = datetime.datetime.combine(datetime.date.today(), datetime.time().min).strftime('%Y-%m-%d %H:%M:%S')
    end_time = datetime.datetime.combine(datetime.date.today(), datetime.time().max).strftime('%Y-%m-%d %H:%M:%S')

    url = f"https://qianchuan.jinritemai.com/ad/api/pmc/v1/uni-promotion/material/list-required?aavid={avvid}&gfversion=1.0.0.1441"

    payload = json.dumps({
        "Metrics": [
            "stat_cost_for_roi2_fork",
            "total_prepay_and_pay_order_roi2_fork",
            "total_pay_order_gmv_for_roi2_fork",
            "live_cvr_rate_exclude_video_for_roi2",
            "live_convert_rate_exclude_video_for_roi2",
            "live_show_count_exclude_video_for_roi2",
            "total_pay_order_gmv_rate_for_roi2_fork",
            "total_unfinished_estimate_order_gmv_for_roi2_fork",
            "total_pay_order_coupon_amount_for_roi2_fork",
            "live_follow_count_for_roi2",
            "live_comment_count_for_roi2",
            "live_like_count_for_roi2",
            "basic_stat_cost_for_roi2_v2_fork",
            "live_watch_count_exclude_video_for_roi2"
        ],
        "Filters": {
            "ConditionRelationshipType": 1,
            "Conditions": [
                {
                    "Field": "query_type",
                    "Operator": 7,
                    "Values": [
                        "all"
                    ]
                },
                {
                    "Field": "roi2_material_type_v3",
                    "Operator": 7,
                    "Values": [
                        "4"
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
                    "Field": "aggregate_smart_bid_type",
                    "Operator": 7,
                    "Values": [
                        "0"
                    ]
                },
                {
                    "Field": "anchor_id",
                    "Operator": 7,
                    "Values": [
                        "103916849759"
                    ]
                }
            ]
        },
        "StartTime": start_time,
        "EndTime": end_time,
        "PageParams": {
            "Limit": 10,
            "Offset": 0
        },
        "DataSetKey": "site_promotion_post_data_live",
        "Dimensions": [
            "anchor_id",
            "roi2_304_cid",
            "roi2_material_anchor_name",
            "roi2_material_anchor_show_id",
            "roi2_material_anchor_icon"
        ],
        "aavid": avvid
    })
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'content-type': 'application/json',
        'origin': 'https://qianchuan.jinritemai.com',
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
    cost = response_json["data"]["statsData"]["rows"][0]["metrics"]["statCostForRoi2Fork"]["value"]
    roi = response_json["data"]["statsData"]["rows"][0]["metrics"]["totalPrepayAndPayOrderRoi2Fork"]["value"]
    logging.info(f"墨雪在全域-直播间-直播间画面当中得到的消耗、roi为：{cost}、{roi}")
    return cost, roi

@catch_errors("在全域-直播间-直播间画面当中得到的消耗、roi失败")
def get_live_room_scenery(session: requests.Session, moxue_timeframe: MoxueTimeframe):
    """
    获取 品创部-墨雪-上海九和
    Args:
        moxue_timeframe:
        session:

    Returns:

    """
    avvid = "1728784932773000"
    moxue_timeframe.live_scenery_consumption, moxue_timeframe.live_scenery_roi =  _get_live_room_scenery(session, avvid)


