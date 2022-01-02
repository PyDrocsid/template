from pathlib import Path

import uvicorn

from PyDrocsid.config import Config, load_config_file, load_version
from PyDrocsid.environment import SENTRY_DSN, ENABLE_API, HOST, PORT
from PyDrocsid.logger import setup_sentry, get_logger

logger = get_logger(__name__)

logger.debug("loading config")
load_config_file(Path("config.yml"))

logger.debug("loading version")
load_version()

print(
    "\033[1m\033[36m"
    r"""

        ____        ____                       _     __   ____        __
       / __ \__  __/ __ \_________  __________(_)___/ /  / __ )____  / /_
      / /_/ / / / / / / / ___/ __ \/ ___/ ___/ / __  /  / __  / __ \/ __/
     / ____/ /_/ / /_/ / /  / /_/ / /__(__  ) / /_/ /  / /_/ / /_/ / /_
    /_/    \__, /_____/_/   \____/\___/____/_/\__,_/  /_____/\____/\__/
          /____/

    """
    "\033[0m",
)

logger.info(f"Starting {Config.NAME} v{Config.VERSION} ({Config.REPO_LINK})\n")

if SENTRY_DSN:
    logger.debug("initializing sentry")
    setup_sentry(SENTRY_DSN, Config.NAME, Config.VERSION)

if ENABLE_API:
    uvicorn.run("bot:fastapi", host=HOST, port=PORT)
else:
    from bot import run  # noqa: E402

    run()
