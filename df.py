from contextlib import suppress

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils.exceptions import MessageToDeleteNotFound, MessageCantBeDeleted

import logging
import asyncio
import tracemalloc



tracemalloc.start()

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s')
logging.debug('A DEBUG Message')
logging.info('An INFO')
logging.warning('A WARNING')
logging.error('An ERROR')
logging.critical('A message of CRITICAL severity')

from auxiliary_files.config import token_API



storage = MemoryStorage()
bot = Bot(token_API)
loop = asyncio.get_event_loop()
dp = Dispatcher(bot,
                storage=storage,
                loop=loop)



async def delete_message(message: types.Message, sleep_time: int = 0):
    await asyncio.sleep(sleep_time)
    with suppress(MessageCantBeDeleted, MessageToDeleteNotFound):
        await message.delete()

    msg = await message.reply('Я удалюсь через 30 секунд')
    asyncio.create_task(delete_message(msg, 30))



if __name__ == '__main__':
    executor.start_polling(dispatcher=dp)
