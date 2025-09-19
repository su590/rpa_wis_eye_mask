# -*- coding: utf-8 -*-  
"""
@Date     : 2025-03-20
@Author   : xwq
@Desc     : <None>

"""
from apscheduler.schedulers.blocking import BlockingScheduler

from src.schedule.disk_schedule import clear_files
from src.service.wis_eye_mask import wis_eye_mask_timeframe


def _wis_eye_mask():
    """
    整点5分跑这个 wis 眼膜时段数据
    :return:
    """
    wis_eye_mask_timeframe()

def create_scheduler() -> BlockingScheduler:
    scheduler = BlockingScheduler()
    scheduler.add_job(_wis_eye_mask, "cron", hour="1-23", minute=5, second=0, misfire_grace_time=100)
    scheduler.add_job(_wis_eye_mask, "cron", hour=23, minute=55, second=0, misfire_grace_time=100)
    # scheduler.add_job(clear_files, 'cron', hour=7, minute=30, second=0, misfire_grace_time=100)
    return scheduler


def create_scheduler_and_start():
    create_scheduler().start()

if __name__ == '__main__':
    create_scheduler_and_start()
