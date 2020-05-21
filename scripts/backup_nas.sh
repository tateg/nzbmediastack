#!/bin/bash

# rsync production nas to backup disk

SOURCE="/mnt/<source>"
DESTINATION="/mnt/<dest>"
EXCLUDE_PATTERN="<directories_to_exclude>"

rsync -avzP --delete --exclude="$EXCLUDE_PATTERN" $SOURCE $DESTINATION
