#!/usr/bin/env python3

import os
import re
import json
import logging
import requests
from termcolor import colored

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s — %(name)s — %(levelname)s — %(funcName)s:%(lineno)d — %(message)s"
)

LOGGER = logging.getLogger('CONSOLE')
LOGGER.info(colored('Moby mover starting up...', 'green'))

TVDB_API_KEY = "5e8485a16ce4ba020c142fa930adc285"
API_PARAM = f"?api_key={TVDB_API_KEY}"
TVDB_BASE_URL = "https://api.themoviedb.org/3"
OAK_TVID = "60603"
EP_FILTERS = ['curse', 'oak', 'island']

def parse_response(res):
    raw = res.text
    return json.loads(raw)

def get_tv_ep(id, season, ep):
    url = f"{TVDB_BASE_URL}/tv/{id}/season/{str(season)}/episode/{str(ep)}{API_PARAM}"
    LOGGER.info(colored(f"making request for: {url}", 'yellow'))
    return parse_response(requests.get(url))

def get_tv_ep_name(id, season, ep):
    return get_tv_ep(id, season, ep)['name']

def get_episodes_in_dir(filters):
    contents = os.listdir()
    eps = []
    for c in contents:
        lower_c = c.lower()
        if any(n in lower_c for n in filters):
            eps.append(lower_c)
    return eps

def split_season_ep_ids(ep):
    match = re.findall(r"(?:s|season)(\d{2})(?:e|x|episode|\n)(\d{2})", ep, re.I)
    return match[0]

eps = get_episodes_in_dir(EP_FILTERS)

for ep in eps:
    split = split_season_ep_ids(ep)
    ep_name = get_tv_ep_name(OAK_TVID, split[0], split[1])
    LOGGER.info(colored(f"looked up: {ep_name}", 'yellow'))
    ep_string = f"{ep_name} - S{split[0]}E{split[1]}.mkv"
    LOGGER.info(colored(f"moving episode: {ep_string}", 'yellow'))
