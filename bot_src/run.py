import asyncio
import signal
import sys

from bot_src.main import run_bot
from utils.configs.path import PathConfig
from utils.log import logger
from utils.database import Base, engine, DBUtils


loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

run_filename = PathConfig.DISCORD_RUN_FILE


def handle_exit(sig, frame):
    logger.info(f"Received exit signal {sig}. Shutting down bot...")
    loop.stop()
    sys.exit(0)


signal.signal(signal.SIGINT, handle_exit)
signal.signal(signal.SIGTERM, handle_exit)

Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    try:
        loop.run_until_complete(run_bot())
    except KeyboardInterrupt:
        logger.info("Bot stopped by KeyboardInterrupt")
    except Exception as e:
        logger.error(f"Bot stopped by Exception: {e}")
    finally:
        logger.info("Bot event loop closing")
        loop.close()
