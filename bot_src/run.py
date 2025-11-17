import asyncio
import signal
import sys

from utils.configs.path import PathConfig
from utils.log import print_log
from utils.database import init_db
from bot_src.main import run_bot


loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

run_filename = PathConfig.DISCORD_RUN_FILE



def handle_exit(sig, frame):
    print_log("info", run_filename, f"Bot stopping by signal {sig}")
    loop.stop()
    sys.exit(0)


signal.signal(signal.SIGINT, handle_exit)
signal.signal(signal.SIGTERM, handle_exit)

init_db()

if __name__ == "__main__":
    try:
        loop.run_until_complete(run_bot())
    except KeyboardInterrupt:
        print_log("info", run_filename, "Bot stopped by KeyboardInterrupt")
    except Exception as e:
        print_log("error", run_filename, f"Unexpected error: {e}")
    finally:
        loop.close()
        print_log("info", run_filename, "Event loop closed. Goodbye!")
