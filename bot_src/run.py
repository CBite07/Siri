# load asyncio module
import asyncio
import signal
import sys

# load main, util modules
from bot_src.main import run_bot
from utils.configs.path import PathConfig
from utils.log import logger
from utils.database import Base, engine

# make a new event loop
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

# get entry point path/filename
run_filename = PathConfig.DISCORD_RUN_FILE


# define exit handler
def handle_exit(sig, frame):
    logger.info(f"Received exit signal {sig}. Shutting down bot...")
    loop.stop()
    sys.exit(0)


# register signal handlers
signal.signal(signal.SIGINT, handle_exit)
signal.signal(signal.SIGTERM, handle_exit)

# create database tables
Base.metadata.create_all(bind=engine)

# run the bot
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
