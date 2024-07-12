from typing import Final
import environ

env = environ.Env()
environ.Env.read_env()

TOKEN: Final = env("TOKEN")
BOT_USERNAME: Final = env("BOT_USERNAME")
