import datetime
import logging

import requests
import json

from src.sql.wis_eye_mask_model import JxNewNine
from src.utils.trycatchtools import catch_errors


def _get_new_nine_commodity(session: requests.Session, aavid: str, commodity_id: list, jx_new_nine: JxNewNine):

    url = ("https://qianchuan.jinritemai.com/ad/api/data/v1/common/statQuery?"
           f"aavid={aavid}")

    payload = json.dumps({
        "DataSetKey": "site_promotion_product_product",
        "Metrics": [
            "product_show_count_for_roi2",
            "product_click_count_for_roi2",
            "product_cvr_rate_for_roi2",
            "product_convert_rate_for_roi2",
            "stat_cost",
            "total_pay_order_gmv_include_coupon_for_roi2",
            "total_prepay_and_pay_order_roi2",
            "total_cost_per_pay_order_for_roi2",
            "total_pay_order_gmv_for_roi2",
            "total_pay_order_coupon_amount_for_roi2",
            "total_ecom_platform_subsidy_amount_for_roi2"
        ],
        "Dimensions": [
            "stat_time_day"
        ],
        "StartTime": datetime.datetime.combine(datetime.date.today(), datetime.time.min).strftime("%Y-%m-%d %H:%M:%S"),
        "EndTime": datetime.datetime.combine(datetime.date.today(), datetime.time.max).strftime("%Y-%m-%d %H:%M:%S"),
        "Filters": {
            "ConditionRelationshipType": 1,
            "Conditions": [
                {
                    "Field": "advertiser_id",
                    "Operator": 7,
                    "Values": [
                        f"{aavid}"
                    ]
                },
                {
                    "Field": "marketing_goal",
                    "Operator": 7,
                    "Values": [
                        "1"
                    ]
                },
                {
                    "Field": "adlab_mode_fork",
                    "Operator": 7,
                    "Values": [
                        "1"
                    ]
                },
                {
                    "Operator": 7,
                    "Field": "qianchuan_product_id",
                    "Values": commodity_id
                }
            ]
        },
        "refer": "ecp,7340216120470716425,7359133796433674250",
        "ComparisonParams": {
            "RatioStartTime": "2025-08-20 00:00:00",
            "RatioEndTime": "2025-08-26 23:59:59"
        },
        "aavid": f"{aavid}"
    })
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'content-type': 'application/json',
        'origin': 'https://qianchuan.jinritemai.com',
        'priority': 'u=1, i',
        'sec-ch-ua': '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
    }

    response = session.request("POST", url, headers=headers, data=payload)
    response_json = response.json()
    current_data = response_json['data']['StatsData']['Totals']
    jx_new_nine.commodity_total_consumption = current_data['stat_cost']['Value']
    jx_new_nine.commodity_user_pay_amount  = current_data['total_pay_order_gmv_for_roi2']['Value']
    jx_new_nine.commodity_total_deal_smart_coupon = current_data['total_pay_order_coupon_amount_for_roi2']['Value']

    logging.info("获取商品数据消耗、智能优惠劵、成交的数据为："
                 f"{jx_new_nine.commodity_total_consumption}、"
                 f"{jx_new_nine.commodity_total_deal_smart_coupon}、"
                 f"{jx_new_nine.commodity_user_pay_amount}")

@catch_errors("营销部WIS-剧星-新9获取商品数据失败")
def get_new_nine_commodity(session: requests.Session, jx_new_nine: JxNewNine):
    commodity_id = ["3658954147295807889", "3737635791363506266", "3509764557633625316", "3633378523286237027"]
    _get_new_nine_commodity(session, "1835249215783051", commodity_id, jx_new_nine)
