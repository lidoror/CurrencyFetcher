from currency_fetcher.log_factory import logger
from currency_fetcher.task_schedule import scheduler
from currency_fetcher.bot import bot
import os
import threading


def main():
    token = os.environ.get('BOT_TOKEN')
    my_bot = bot.Bot(token)
    job_scheduler = scheduler.Scheduler(my_bot.send_message_to_users)
    job_scheduler.create_daily_schedule(sched_time="09:30", args=my_bot.get_exchange_rate())
    threading.Thread(target=job_scheduler.start_schedule()).start()

    my_bot.start_bot()


if __name__ == '__main__':
    logger.info('_____application_starting_____')
    main()
