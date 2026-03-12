from scheduler import scheduler

def schedule_post(bot, channel, message, date):

    scheduler.add_job(
        bot.send_message,
        "date",
        run_date=date,
        args=[channel, message]
    )
