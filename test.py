from rapid_api.request_to_api import request_to_api
from utils.data import get_data
from config_data import config
from loguru import logger
from loader import bot
from handlers.special_heandlers.finish_work import finish_work
import requests
import re
import json
import locale


locale.setlocale(locale.LC_ALL, "{config.LOCALE}.UTF-8")




