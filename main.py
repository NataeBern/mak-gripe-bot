from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import logging

from auxiliary_files.config import token_API
from sql.sqlite import db_start



logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s')
logging.debug('A DEBUG Message')
logging.info('An INFO')
logging.warning('A WARNING')
logging.error('An ERROR')
logging.critical('A message of CRITICAL severity')

storage = MemoryStorage()
bot = Bot(token_API)
dp = Dispatcher(bot=bot,
                storage=storage)



async def on_startup(_):

    print('Бот был успешно запущен!')

    await db_start()

    from dialogue_admin.dialogue_admin import register_handlers_dialogue_admin
    from dialogue_admin.dialogue_admin_tires import register_handlers_dialogue_admin_tires
    from dialogue_admin.dialogue_admin_wheels import register_handlers_dialogue_admin_wheels
    from dialogue_others.dialogue_others_buy_product import register_handlers_dialogue_others_buy_pr
    from dialogue_others.dialogue_others_puck_up_product import register_handlers_dialogue_others_pick_up_pr
    from moderation.moderation import register_handlers_moderation

    register_handlers_dialogue_admin(dp=dp)
    register_handlers_dialogue_admin_tires(dp=dp)
    register_handlers_dialogue_admin_wheels(dp=dp)
    register_handlers_dialogue_others_buy_pr(dp=dp)
    register_handlers_dialogue_others_pick_up_pr(dp=dp)
    register_handlers_moderation(dp=dp)


if __name__ == '__main__':
    executor.start_polling(dispatcher=dp,
                           on_startup=on_startup,
                           skip_updates=False)
