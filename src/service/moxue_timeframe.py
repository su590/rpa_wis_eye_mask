import datetime
import logging

from src.service import _DslpAccount, get_dslp_account, get_jlyq_account, _JlyqAccount
from src.spider.dslp.dslp_session import DslpSessionByDd
from src.spider.jlyq.jlyq_session import JlyqSession
from src.spider.jlyq.moxue.live_room_scenery import get_live_room_scenery
from src.spider.dslp.mmoxue.deal_refund import get_deal, get_refund
from src.spider.jlyq.moxue.live_universal import get_live_universal, get_constitution_live
from src.spider.jlyq.moxue.strand_commodity_all import xiao_dian, hot, total
from src.spider.jlyq.moxue.universal_commodity import chun_yong, fen_fa, ran_fa, universal, paid_influencer
from src.sql.moxue_timeframe import MoxueTimeframe
from src.utils.feishutools import get_time_period_per_30min, insert_spread_all, send_message_by_robot
from src.utils.trycatchtools import catch_errors

SPREAD_TOKEN = "S5mFsivyKhcx5ktD5Z8cDFd5nLb" # 表格token
CURRENT_SHEET_ID = "JoC53A" # 当前时段子表id
HISTORY_SHEET_ID = "yCZOQi" # 历史时段子表id
ROBOT = "https://open.feishu.cn/open-apis/bot/v2/hook/95c69911-abf5-4fce-ac89-55edd62818fd" # 机器人链接


@catch_errors("获取抖店成交退款失败")
def _dslp_data(dslp_account: _DslpAccount, moxue_timeframe: MoxueTimeframe):
    """
    收集电商罗盘当中的数据
    Args:
        dslp_account:
        moxue_timeframe:

    Returns:

    """
    with DslpSessionByDd(dslp_account.port, dslp_account.username, dslp_account.shop) as session:
        moxue_timeframe.doudian_deal = get_deal(session)
        moxue_timeframe.luopan_refund = get_refund(session)

@catch_errors("巨量引擎数据获取失败")
def _jlyq_data(jlyq_account: _JlyqAccount, moxue_timeframe: MoxueTimeframe):
    """
    收集巨量引擎当中的信息
    Args:
        jlyq_account:
        moxue_timeframe:

    Returns:

    """
    with JlyqSession(jlyq_account.port, jlyq_account.username, jlyq_account.password) as session:
        get_live_universal(session, moxue_timeframe)
        xiao_dian(session, moxue_timeframe)
        paid_influencer(session, moxue_timeframe)
        get_live_room_scenery(session, moxue_timeframe)
        total(session, moxue_timeframe)
        chun_yong(session, moxue_timeframe)
        fen_fa(session, moxue_timeframe)
        ran_fa(session, moxue_timeframe)
        universal(session, moxue_timeframe)
        get_constitution_live(session, moxue_timeframe)

def _assemble_feishu_message(moxue_timeframe: MoxueTimeframe) -> str:
    """
    组装飞书机器人发送的消息
    Args:
        moxue_timeframe:

    Returns:

    """
    text = f"消息推送展示项目：墨雪实时营销数据通知\n" \
           f"获取数据来源：墨雪官方旗舰店\n" \
           f">> 时段：{get_time_period_per_30min()}" \
           f">> 获取时间：{datetime.datetime.now().strftime('%H:%M:%S')};\n" \
           "【抖店数据】\n" \
           f">> 抖店成交：{moxue_timeframe.doudian_deal};\n" \
           f">> 罗盘退款：{moxue_timeframe.luopan_refund};\n" \
           "【直播间-全域】\n" \
           f">> 智能优惠劵：{moxue_timeframe.smart_coupon};\n" \
           f">> 直播间时段消耗(全域)：{moxue_timeframe.live_room_timeframe_consumption};\n" \
           f">> 直播间时段付费ROI：{moxue_timeframe.live_room_timeframe_cost_roi};\n" \
           "【直播间画面】\n" \
           f">> 直播间画面总消耗：{moxue_timeframe.live_scenery_consumption};\n" \
           f">> 直播间画面ROI：{moxue_timeframe.live_scenery_roi};\n" \
           "【小店】\n" \
           f">> 小店消耗：{moxue_timeframe.xiao_dian_cost};\n" \
           f">> 随心推ROI：{moxue_timeframe.xiao_dian_roi}; \n" \
           "【付费达人】\n" \
           f">> 付费达人消耗：{moxue_timeframe.paid_influencer_cost};\n" \
           f">> 付费达人ROI：{moxue_timeframe.paid_influencer_roi}; \n" \
           "【千川短视频】\n" \
           f">> 标准短视频总消耗：{moxue_timeframe.short_video_consumption}; \n" \
           f">> 短视频ROI：{moxue_timeframe.short_video_roi};\n" \
           "【全域】\n" \
           f">> 全域消耗：{moxue_timeframe.short_video_university_consumption}; \n" \
           f">> 全域ROI：{moxue_timeframe.short_video_university_roi};\n" \
           "【纯佣】\n" \
           f">> 消耗：{moxue_timeframe.chunyong_consumption}; \n" \
           f">> ROI：{moxue_timeframe.chunyong_roi};\n" \
           "【分发】\n" \
           f">> 消耗：{moxue_timeframe.fenfa_consumption}; \n" \
           f">> ROI：{moxue_timeframe.fenfa_roi};\n" \
           "【染发】\n" \
           f">> 消耗：{moxue_timeframe.ranfa_consumption}; \n" \
           f">> ROI：{moxue_timeframe.ranfa_roi};\n"\
           "【机构直播间】\n" \
           f">> 消耗：{moxue_timeframe.constitution_consumption}; \n" \
           f">> ROI：{moxue_timeframe.constitution_roi};\n"
    return text

def _assemble_sheet_list(moxue_timeframe: MoxueTimeframe) -> list:
    """
    组装表格当中的信息
    Args:
        moxue_timeframe:

    Returns:

    """
    assemble_list = []
    assemble_list.append(datetime.date.today().strftime('%Y-%m-%d'))
    assemble_list.append(get_time_period_per_30min())
    assemble_list.append(datetime.datetime.now().strftime('%H:%M:%S'))
    assemble_list.extend([moxue_timeframe.doudian_deal, moxue_timeframe.luopan_refund,
                          moxue_timeframe.smart_coupon, moxue_timeframe.live_room_timeframe_consumption, moxue_timeframe.live_room_timeframe_cost_roi])
    assemble_list.append("")
    assemble_list.extend([moxue_timeframe.live_scenery_consumption, moxue_timeframe.live_scenery_roi])
    assemble_list.append("")
    assemble_list.extend([moxue_timeframe.xiao_dian_cost, moxue_timeframe.xiao_dian_roi])
    assemble_list.append("")
    assemble_list.extend([moxue_timeframe.paid_influencer_cost, moxue_timeframe.paid_influencer_roi])
    assemble_list.extend([""] * 4)
    assemble_list.extend([moxue_timeframe.short_video_consumption, moxue_timeframe.short_video_roi,
                          moxue_timeframe.short_video_university_consumption, moxue_timeframe.short_video_university_roi,
                          moxue_timeframe.chunyong_consumption, moxue_timeframe.chunyong_roi,
                          moxue_timeframe.fenfa_consumption, moxue_timeframe.fenfa_roi,
                          moxue_timeframe.ranfa_consumption, moxue_timeframe.ranfa_roi,
                          moxue_timeframe.constitution_consumption, moxue_timeframe.constitution_roi])
    return assemble_list

def moxue_timeframe():
    """
    获取墨雪时段信息
    Returns:

    """
    brand = "墨雪"

    _dslp_account = get_dslp_account(brand)
    _jlyq_account = get_jlyq_account(brand, True)

    res: MoxueTimeframe = MoxueTimeframe()
    _dslp_data(_dslp_account, res)
    _jlyq_data(_jlyq_account, res)
    logging.info(res)

    insert_list = _assemble_sheet_list(res)

    insert_spread_all(SPREAD_TOKEN, CURRENT_SHEET_ID, insert_list, "")
    insert_spread_all(SPREAD_TOKEN, HISTORY_SHEET_ID, insert_list)

    message = _assemble_feishu_message(res)
    send_message_by_robot(message, ROBOT)


if __name__ == '__main__':
    moxue_timeframe()