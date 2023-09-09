import schedule
import time
from typing import Callable
from currency_fetcher.log_factory import logger


class Scheduler:

    def __init__(self, task: Callable):
        self.task = task

    def create_daily_schedule(self, sched_time: str, args: str = None):
        logger.info(f"scheduling daily job [{self.task}] with sched time [{sched_time}]")
        schedule.every().day.at(sched_time).do(self.task, args)

    def create_seconds_schedule(self, sched_time: int, args: str = None):
        logger.info(f"scheduling secondly job [{self.task}] with sched time [{sched_time}]")
        schedule.every(sched_time).seconds.do(self.task, args)

    def start_schedule(self):
        while True:
            schedule.run_pending()
            time.sleep(1)
