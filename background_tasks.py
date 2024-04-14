import asyncio
import logging

from aiogram import Bot
from aiogram.enums.parse_mode import ParseMode

from datetime import datetime, timedelta
from celery import Celery
from celery.schedules import crontab

from database.models.user import User
from database.connector import session

from configuration import BOT_TOKEN, ua_config

app = Celery('tasks', broker='redis://redis:6379')
logger = logging.getLogger(__name__)


async def async_accept_evacuation_request(volunteer_id, user_id):
    with session() as s:
        volunteer = s.query(User).filter(User.telegram_id == volunteer_id).first()
    if volunteer is None:
        return
    bot = Bot(BOT_TOKEN)
    await bot.send_message(
        chat_id=user_id,
        text=ua_config.get('evacuation_prompts', 'request_approved').format(
            first_name=volunteer.first_name,
            last_name=volunteer.last_name,
            phone_number=volunteer.phone_number
        ),
        parse_mode=ParseMode.HTML
    )


@app.task
def accept_evacuation_request(volunteer_id, user_id):
    coro = async_accept_evacuation_request(volunteer_id, user_id)
    asyncio.run(coro)

# Optional configuration, see the application user guide.
app.conf.update(
    result_expires=3600,
)

if __name__ == '__main__':
    app.start()
