#!/bin/bash

# mount nfs share and insert into fstab

SERVER=127.0.0.1
MOUNT_SRC=""
MOUNT_DEST=""
FSTAB_ENTRY="${SERVER}:${MOUNT_SRC} ${MOUNT_DEST} nfs defaults    0 0"

echo "installing nfs-common..."
apt -y install nfs-common

mkdir -p ${MOUNT_DEST}

echo "mounting..."
mount ${SERVER}:${MOUNT_SRC} ${MOUNT_DEST}

if grep -Fxq "${FSTAB_ENTRY}" /etc/fstab; then
  echo "fstab entry already exists"
else
  echo "creating mount in fstab for persistent mount point"
  echo "${FSTAB_ENTRY}" >> /etc/fstab
fi

echo "done"
