import datetime
import json
import logging

import requests

from src.sql.wis_eye_mask_model import JxFeelFreeToPush, JxNewNine
from src.utils.logintools import Session
from src.utils.trycatchtools import catch_errors


def _get_universal_commodity_by_account(session: requests.session, avvid: str) -> tuple:
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
    smart_coupon = response_json["data"]["totalMetrics"]["metrics"]["totalPayOrderCouponAmountForRoi2Primary"]["value"]
    user_pay_deal = response_json["data"]["totalMetrics"]["metrics"]["totalPayOrderGmvForRoi2Primary"]["value"]
    logging.info("获取商品数据消耗、智能优惠劵、成交的数据为："
                 f"{consumption}、"
                 f"{smart_coupon}、"
                 f"{user_pay_deal}")
    return consumption, smart_coupon, user_pay_deal

@catch_errors("营销部-WIS-剧星-眼膜-随心推获取商品数据失败")
def get_feel_free_to_push_commodity(session: Session, jx_feel_free_to_push: JxFeelFreeToPush):
    consumption, smart_coupon, user_pay_deal = _get_universal_commodity_by_account(session, "1758788274050062")
    jx_feel_free_to_push.commodity_total_consumption = consumption
    jx_feel_free_to_push.commodity_total_deal_smart_coupon = smart_coupon
    jx_feel_free_to_push.commodity_user_pay_amount = user_pay_deal

#
# @catch_errors("营销部WIS-剧星-新9获取商品数据失败")
# def get_new_nine_commodity(session, jx_new_nine: JxNewNine):
#     consumption, smart_coupon, user_pay_deal = _get_universal_commodity_by_account(session, "1835249215783051")
#     jx_new_nine.commodity_total_consumption = consumption
#     jx_new_nine.commodity_total_deal_smart_coupon = smart_coupon
#     jx_new_nine.commodity_user_pay_amount = user_pay_deal