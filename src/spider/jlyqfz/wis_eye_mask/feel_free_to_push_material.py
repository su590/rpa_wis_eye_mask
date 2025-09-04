import datetime
import logging
import json

from requests import Session

from src.sql.wis_eye_mask_model import JxFeelFreeToPush
from src.utils.trycatchtools import catch_errors


def _get_material_data(session: Session, aavid: str, jx_feel_free_to_push: JxFeelFreeToPush):

    url = ("https://qianchuan.jinritemai.com/ad/api/pmc/v1/uni-promotion/material/list-required?"
           f"aavid={aavid}")

    payload = json.dumps({
        "Metrics": [
            "live_cvr_rate_exclude_video_for_roi2",
            "live_convert_rate_exclude_video_for_roi2",
            "stat_cost_for_roi2_fork",
            "cost_rate_for_roi2_fork",
            "total_pay_order_gmv_include_coupon_for_roi2_fork",
            "total_pay_order_gmv_rate_for_roi2_fork",
            "total_prepay_and_pay_order_roi2_fork",
            "live_show_count_exclude_video_for_roi2",
            "live_watch_count_exclude_video_for_roi2",
            "total_pay_order_count_for_roi2_fork",
            "basic_stat_cost_for_roi2_v2_fork",
            "total_cost_per_pay_order_for_roi2_fork",
            "total_pay_order_gmv_for_roi2_fork",
            "total_pay_order_coupon_amount_for_roi2_fork",
            "total_ecom_platform_subsidy_amount_for_roi2_fork",
            "total_prepay_order_count_for_roi2_fork",
            "total_prepay_order_gmv_for_roi2_fork",
            "total_unfinished_estimate_order_gmv_for_roi2_fork",
            "live_follow_count_for_roi2",
            "live_comment_count_for_roi2",
            "live_like_count_for_roi2",
            "additional_delivery_stat_cost_for_roi2_assist",
            "additional_delivery_total_pay_order_count_for_roi2_assist",
            "additional_delivery_total_pay_order_gmv_include_coupon_for_roi2_assist",
            "additional_delivery_total_prepay_and_pay_order_roi2_assist",
            "additional_delivery_total_pay_order_gmv_for_roi2_assist",
            "additional_delivery_total_pay_order_coupon_amount_for_roi2_assist",
            "additional_delivery_pay_convert_cost_for_roi2_assist_v2",
            "additional_delivery_pay_convert_cnt_for_roi2_assist_v2"
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
                        "3984227879106895"
                    ]
                }
            ]
        },
        "StartTime": datetime.datetime.combine(datetime.date.today(), datetime.time().min).strftime("%Y-%m-%d %H:%M:%S"),
        "EndTime": datetime.datetime.combine(datetime.date.today(), datetime.time().max).strftime("%Y-%m-%d %H:%M:%S"),
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
    current_data = response_json['data']['statsData']['totals']
    jx_feel_free_to_push.material_total_click_ratio = current_data['liveCvrRateExcludeVideoForRoi2']['value']
    jx_feel_free_to_push.material_total_transfer_ratio = current_data['liveConvertRateExcludeVideoForRoi2']['value']
    jx_feel_free_to_push.material_total_consumption = current_data['statCostForRoi2Fork']['value']
    jx_feel_free_to_push.material_total_consumption_ratio = current_data['costRateForRoi2Fork']['value']
    jx_feel_free_to_push.material_total_deal = current_data['totalPayOrderGmvIncludeCouponForRoi2Fork']['value']
    jx_feel_free_to_push.material_total_deal_ratio = current_data['totalPayOrderGmvRateForRoi2Fork']['value']
    logging.info("在营销部WIS-剧星-眼膜-随心推下获取素材数据点击率、转换率、消耗、消耗率、成交、成交率为："
                 f"{jx_feel_free_to_push.material_total_click_ratio}、"
                 f"{jx_feel_free_to_push.material_total_transfer_ratio}、"
                 f"{jx_feel_free_to_push.material_total_consumption}、"
                 f"{jx_feel_free_to_push.material_total_consumption_ratio}、"
                 f"{jx_feel_free_to_push.material_total_deal}、"
                 f"{jx_feel_free_to_push.material_total_deal_ratio}、")

@catch_errors("在营销部WIS-剧星-眼膜-随心推下获取素材数据失败")
def get_feel_free_to_push_material(session: Session, jx_feel_free_to_push: JxFeelFreeToPush):
    _get_material_data(session, '1758788274050062', jx_feel_free_to_push)
