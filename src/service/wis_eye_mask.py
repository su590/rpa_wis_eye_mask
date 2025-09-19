from src.service import get_jlyqfz_account
from src.spider.jlyq.jlyq_session import JlyqSession
from src.spider.jlyqfz.wis_eye_mask.feel_free_to_push_commodity import get_feel_free_to_push_commodity
from src.spider.jlyqfz.wis_eye_mask.feel_free_to_push_live import get_feel_free_to_push_live
from src.spider.jlyqfz.wis_eye_mask.feel_free_to_push_material import get_feel_free_to_push_material
from src.spider.jlyqfz.wis_eye_mask.new_nine_commodity import get_new_nine_commodity
from src.sql.wis_eye_mask_model import JxFeelFreeToPush, JxNewNine, WisEyeMaskModel
from src.utils.feishutools import send_message_by_robot, get_time_period_per_hour, insert_spread_append

ROBOT = "https://open.feishu.cn/open-apis/bot/v2/hook/7c14546c-46d4-487b-98f4-0fce0924a36e" # 机器人链接
SPREAD_TOKEN = "R92WsH803hIu7ZtAQsOcOtkAnTd" # 表格token
CURRENT_SHEET_ID = "11d8d7" # 当前时段子表id

def _assemble_wis_eye_mask_message(wis_eye_mask_model: WisEyeMaskModel) -> str:
    """
    组装飞书机器人发送的 WIS 眼膜实时数据消息
    Args:
        wis_eye_mask_model: WisEyeMaskModel

    Returns:
        str
    """
    def fmt(value: float) -> str:
        return f"{value:.2f}"

    jx_fftp = wis_eye_mask_model.jx_feel_free_to_push
    jx_new9 = wis_eye_mask_model.jx_new_nine

    text = (
        "消息推送展示项目：WIS眼膜投放实时数据\n"
        f"日期：{datetime.date.today().strftime('%Y-%m-%d')}\n"
        f"获取时间：{datetime.datetime.now().strftime('%H:%M:%S')};\n"
        "【剧星随心推直播】\n"
        f">> 消耗：{fmt(jx_fftp.live_total_consumption)};\n"
        f">> 成交：{fmt(jx_fftp.live_total_deal)};\n"
        f">> 优惠券：{fmt(jx_fftp.live_total_deal_smart_coupon)};\n"
        "【剧星随心推直播间画面】\n"
        f">> 点击率：{fmt(jx_fftp.material_total_click_ratio)}%;\n"
        f">> 转化率：{fmt(jx_fftp.material_total_transfer_ratio)}%;\n"
        f">> 消耗：{fmt(jx_fftp.material_total_consumption)};\n"
        f">> 占比：{fmt(jx_fftp.material_total_consumption_ratio)}%;\n"
        f">> 成交：{fmt(jx_fftp.material_total_deal)};\n"
        f">> 成交金额占比：{fmt(jx_fftp.material_total_deal_ratio)}%;\n"
        "【剧星随心推直购】\n"
        f">> 消耗：{fmt(jx_fftp.commodity_total_consumption)};\n"
        f">> 支付：{fmt(jx_fftp.commodity_user_pay_amount)};\n"
        f">> 优惠券：{fmt(jx_fftp.commodity_total_deal_smart_coupon)};\n"
        "【剧星新9】\n"
        f">> 消耗：{fmt(jx_new9.commodity_total_consumption)};\n"
        f">> 支付：{fmt(jx_new9.commodity_user_pay_amount)};\n"
        f">> 优惠券：{fmt(jx_new9.commodity_total_deal_smart_coupon)};\n"
    )
    return text

import datetime
import dataclasses

def _assemble_sheet_list(wis_eye_mask_model: WisEyeMaskModel) -> list:
    """
    组装消息内容同步到飞书表格当中
    :param wis_eye_mask_model:
    :return:
    """
    assemble_list = [
        datetime.date.today().strftime('%Y-%m-%d'),
        get_time_period_per_hour(),
        datetime.datetime.now().strftime('%H:%M:%S')
    ]

    # 遍历 jx_feel_free_to_push
    for field in dataclasses.fields(wis_eye_mask_model.jx_feel_free_to_push):
        value = getattr(wis_eye_mask_model.jx_feel_free_to_push, field.name)
        if "ratio" in field.name:  # ratio 结尾的字段加 %
            assemble_list.append(f"{value}%")
        else:
            assemble_list.append(value)

    # 遍历 jx_new_nine
    for field in dataclasses.fields(wis_eye_mask_model.jx_new_nine):
        value = getattr(wis_eye_mask_model.jx_new_nine, field.name)
        if "ratio" in field.name:
            assemble_list.append(f"{value}%")
        else:
            assemble_list.append(value)

    return assemble_list


def wis_eye_mask_timeframe():
    jx_feel_free_to_push = JxFeelFreeToPush()
    jx_new_nine = JxNewNine()
    wis_eye_mask_model = WisEyeMaskModel()

    # pay attention 在这里原本是用巨量引擎方舟去登录的 后面改为用巨量引擎来登录了
    # 但是我在这里并没有改变相应的名称 注意一下就行 问题不大
    account = get_jlyqfz_account("WIS_EYE_MASK")

    with JlyqSession(account.port, account.username, account.password) as session:
        # 账户 营销部-WIS-剧星-眼膜-随心推
        get_feel_free_to_push_live(session, jx_feel_free_to_push)
        get_feel_free_to_push_material(session, jx_feel_free_to_push)
        get_feel_free_to_push_commodity(session, jx_feel_free_to_push)
        # 账户 营销部WIS-剧星-新9
        get_new_nine_commodity(session, jx_new_nine)

    wis_eye_mask_model.jx_feel_free_to_push = jx_feel_free_to_push
    wis_eye_mask_model.jx_new_nine = jx_new_nine
    send_message_by_robot(_assemble_wis_eye_mask_message(wis_eye_mask_model), ROBOT)
    insert_spread_append(SPREAD_TOKEN, CURRENT_SHEET_ID, _assemble_sheet_list(wis_eye_mask_model))

if __name__ == '__main__':
    wis_eye_mask_timeframe()