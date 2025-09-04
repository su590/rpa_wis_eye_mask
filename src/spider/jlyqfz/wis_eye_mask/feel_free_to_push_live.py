import datetime
import json
import logging

from requests import Session

from src.sql.wis_eye_mask_model import JxFeelFreeToPush
from src.utils.trycatchtools import catch_errors


def _get_live_data(session: Session, avvid: str, jx_feel_free_to_push: JxFeelFreeToPush):
    """
    获取每个小时的直播间相关数据
    :param session: 
    :param avvid:
    :return: 
    """
    url = ("https://qianchuan.jinritemai.com/ad/api/data/v1/common/statQuery?"
           "reqFrom=compareTrend&"
           f"aavid={avvid}")

    payload = json.dumps({
        "Metrics": [
            "stat_cost",
            "total_prepay_and_pay_order_roi2",
            "total_pay_order_gmv_include_coupon_for_roi2",
            "total_pay_order_count_for_roi2",
            "total_cost_per_pay_order_for_roi2",
            "total_pay_order_gmv_for_roi2",
            "total_pay_order_coupon_amount_for_roi2",
            "total_ecom_platform_subsidy_amount_for_roi2",
            "total_prepay_order_count_for_roi2",
            "total_prepay_order_gmv_for_roi2",
            "total_unfinished_estimate_order_gmv_for_roi2",
            "total_prepay_and_pay_settle_roi2_7d",
            "total_order_settle_amount_for_roi2_7d",
            "total_order_settle_count_for_roi2_7d",
            "total_cost_per_pay_order_settle_for_roi2_7d",
            "total_order_settle_amount_rate_for_roi2_7d",
            "total_order_settle_count_rate_for_roi2_7d",
            "total_prepay_and_pay_settle_roi2_14d",
            "total_order_settle_amount_for_roi2_14d",
            "total_order_settle_count_for_roi2_14d",
            "total_cost_per_pay_order_settle_for_roi2_14d",
            "total_order_settle_amount_rate_for_roi2_14d",
            "total_order_settle_count_rate_for_roi2_14d",
            "total_prepay_and_pay_settle_roi2_30d",
            "total_order_settle_amount_rate_for_roi2_30d",
            "total_order_settle_count_rate_for_roi2_30d",
            "total_prepay_and_pay_settle_roi2_90d",
            "total_order_settle_amount_rate_for_roi2_90d",
            "total_order_settle_count_rate_for_roi2_90d"
        ],
        "refer": "ecp,7262942222943797285,7315033906162434099,site_promotion_ad_table_list",
        "DataSetKey": "site_promotion_ad_table_list",
        "OrderBy": [
            {
                "Type": 1,
                "Field": "stat_time_hour"
            }
        ],
        "Dimensions": [
            "ad_id",
            "stat_time_hour"
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
                    "Field": "ad_id",
                    "Operator": 7,
                    "Values": [
                        "1811885998727338"
                    ]
                }
            ]
        },
        "StartTime": datetime.datetime.combine(datetime.date.today(), datetime.time.min).strftime("%Y-%m-%d %H:%M:%S"),
        "EndTime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "aavid": f"{avvid}"
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
    current_data = response_json["data"]["StatsData"]["Rows"][-2]
    jx_feel_free_to_push.live_total_consumption = current_data["Metrics"]["stat_cost"]["Value"]
    jx_feel_free_to_push.live_total_deal = current_data["Metrics"]['total_pay_order_gmv_include_coupon_for_roi2']["Value"]
    jx_feel_free_to_push.live_total_deal_smart_coupon = current_data["Metrics"]["total_pay_order_coupon_amount_for_roi2"]["Value"]
    logging.info(f"在营销部WIS-剧星-眼膜-随心推下获取的直播消耗、成交、成交优惠劵的数据为："
                 f"{jx_feel_free_to_push.live_total_consumption}、"
                 f"{jx_feel_free_to_push.live_total_deal}、"
                 f"{jx_feel_free_to_push.live_total_deal_smart_coupon}")

@catch_errors("在营销部WIS-剧星-眼膜-随心推下获取直播数据失败")
def get_feel_free_to_push_live(session: Session, jx_feel_free_to_push: JxFeelFreeToPush):
    _get_live_data(session, "1758788274050062", jx_feel_free_to_push)

def check_session(session: Session):
    """
    改方法用来测试session正确性 如果抛出异常的话就重新拿session
    :param session:
    :return:
    """
    _get_live_data(session, "1758788274050062", JxFeelFreeToPush())
