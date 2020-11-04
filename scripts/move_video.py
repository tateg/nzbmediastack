#!/usr/bin/env python3

import os
import re
import shutil
import json
import logging
import requests
from termcolor import colored

logging.basicConfig(
    level=logging.DEBUG,
    format=(
        "%(asctime)s — "
        "%(name)s — "
        "%(levelname)s — "
        "%(funcName)s:%(lineno)d — "
        "%(message)s"
    )
)

LOGGER = logging.getLogger('CONSOLE')
TVDB_API_KEY = ""
API_PARAM = f"?api_key={TVDB_API_KEY}"
TVDB_BASE_URL = "https://api.themoviedb.org/3"
OAK_TVID = "60603"
EP_FILTERS = ['curse', 'oak', 'island']
VALID_EXTENSIONS = ['mkv','avi','mpg','mp4']
DEST_DIR = 'test_dir/The Curse Of Oak Island'

def parse_response(res):
    raw = res.text
    return json.loads(raw)

def get_tv_ep(id, season, episode):
    szn = str(season)
    epz = str(episode)
    url_base = f"{TVDB_BASE_URL}/tv/{id}"
    url_season_w_ep = f"{url_base}/season/{szn}/episode/{epz}"
    full_url = url_season_w_ep + API_PARAM
    LOGGER.debug(colored(f"making request for: {full_url}", 'yellow'))
    res = parse_response(requests.get(full_url))
    LOGGER.debug(colored(res, 'yellow'))
    return res

def get_tv_ep_name(id, season, episode):
    return get_tv_ep(id, season, episode)['name']

def get_episodes_in_dir(filters):
    contents = os.listdir()
    eps = []
    for c in contents:
        lower_c = c.lower()
        if any(n in lower_c for n in filters):
            ep_files = os.listdir(c)
            eps.append({
                'original_dirname': c,
                'lower_dirname': lower_c,
                'contents': ep_files
            })
    return eps

def split_season_ep_ids(ep):
    match = re.findall(
        r"(?:s|season)(\d{2})(?:e|x|episode|\n)(\d{2})", ep, re.I
    )
    return match[0]

def get_vidfile(contents):
    for item in contents:
        extension = item.split('.')[1].lower()
        if extension in VALID_EXTENSIONS:
            return [item, extension]

def move_vidfile(original, new, directory):
    full_path = directory + new
    LOGGER.info(colored(f"moving: {original} -> {full_path}", 'yellow'))
    if not os.path.exists(directory):
        os.makedirs(directory)
    shutil.move(original, full_path)

def cleanup_leftover_dir(dir):
    LOGGER.info(colored(f"removing directory: {dir}", 'yellow'))
    os.rmdir(dir)

LOGGER.info(colored('--- moby mover starting up ---', 'green'))

LOGGER.info(colored(f"getting episodes with filter: {EP_FILTERS}", 'green'))
eps = get_episodes_in_dir(EP_FILTERS)

LOGGER.info(colored('filtering episodes and preparing move', 'green'))
for ep in eps:
    LOGGER.debug(colored(f"splitting: {ep.get('lower_dirname')}"))
    split = split_season_ep_ids(ep.get('lower_dirname'))
    s_num = split[0]
    e_num = split[1]
    ep_name = get_tv_ep_name(OAK_TVID, s_num, e_num)
    LOGGER.info(colored(f"looked up: {ep_name} - S{s_num}E{e_num}", 'yellow'))
    vidfile = get_vidfile(ep.get('contents'))
    if vidfile is not None:
        ep_string = f"{ep_name} - S{s_num}E{e_num}.{vidfile[1]}"
        move_path = DEST_DIR + '/Season '+ s_num.lstrip('0') + '/'
        file_to_move = ep.get('original_dirname') + '/' + vidfile[0]
        move_vidfile(file_to_move, ep_string, move_path)
    cleanup_leftover_dir(ep.get('original_dirname'))
