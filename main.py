import asyncio

from loguru import logger

from helper import bot, dp


async def on_startup():
    logger.warning('Бот онлайн')
    await print_info()


def include_user_routers(dp):
    from core.handlers.user import (
        menu,
        promocodes,
        send_report,
        translations
    )
    dp.include_routers(
        menu.r,
        promocodes.r,
        send_report.r,
        translations.r
    )


def include_admin_routers(dp):
    from core.handlers.admin import (
        add_promo,
        add_translation,
        delete_promo,
        delete_translation,
        menu,
        send_mail,
        grand_admin_commands
    )
    dp.include_routers(
        add_promo.r,
        add_translation.r,
        delete_promo.r,
        delete_translation.r,
        menu.r,
        send_mail.r,
        grand_admin_commands.r
    )


def set_loggers():
    logger.add(
        'logs/{time}.log',
        level='INFO',
        backtrace=True,
        diagnose=True,
        rotation='00:00',
        retention='1 week',
        catch=True
    )
    logger.add(
        'errors/{time}.log',
        level='ERROR',
        backtrace=True,
        diagnose=True,
        rotation='00:00',
        retention='1 week',
        catch=True
    )


async def print_info():
    info = await bot.get_webhook_info()
    logger.info(info)
    info = await bot.get_me()
    logger.info(info)


if __name__ == "__main__":

    set_loggers()
    include_admin_routers(dp)
    include_user_routers(dp)
    dp.startup.register(on_startup)
    asyncio.run(dp.start_polling(bot))
