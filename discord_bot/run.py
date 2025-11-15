import asyncio
import signal
import sys

from configs.path import PathConfig
from discord_bot.main import run_bot
from discord_bot.utils.log import print_formatted_log


loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

run_filename = PathConfig.DISCORD_RUN_FILE


def handle_exit(sig, frame):
    print_formatted_log("info", run_filename, f"Bot stopping by signal {sig}")
    loop.stop()
    sys.exit(0)


signal.signal(signal.SIGINT, handle_exit)
signal.signal(signal.SIGTERM, handle_exit)


if __name__ == "__main__":
    try:
        loop.run_until_complete(run_bot())
    except KeyboardInterrupt:
        print_formatted_log("info", run_filename, "Bot stopped by KeyboardInterrupt")
    except Exception as e:
        print_formatted_log("error", run_filename, f"Unexpected error: {e}")
    finally:
        loop.close()
        print_formatted_log("info", run_filename, "Event loop closed. Goodbye!")
