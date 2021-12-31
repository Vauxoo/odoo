#!/usr/bin/env bash
set -o errexit
set -o nounset
set -o pipefail
# set -o xtrace

if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root" 
   exit 1
fi

file_exists() {
    [[ -f $1 ]];
}

require_command () {
    type "$1" &> /dev/null || { echo "Command $1 is missing. Install it e.g. with 'apt-get install $1'. Aborting." >&2; exit 1; }
}

require_command kpartx
require_command qemu-arm-static
require_command zerofree

__dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
__file="${__dir}/$(basename "${BASH_SOURCE[0]}")"
__base="$(basename ${__file} .sh)"

MOUNT_POINT="${__dir}/root_mount"
OVERWRITE_FILES_BEFORE_INIT_DIR="${__dir}/overwrite_before_init"
OVERWRITE_FILES_AFTER_INIT_DIR="${__dir}/overwrite_after_init"
VERSION=15.0
VERSION_IOTBOX=21.10
REPO=https://github.com/odoo/odoo.git

# if ! file_exists *raspios*.img ; then
#    wget 'https://downloads.raspberrypi.org/raspios_lite_armhf/images/raspios_lite_armhf-2021-05-28/2021-05-07-raspios-buster-armhf-lite.zip' -O raspios.img.zip
#    unzip raspios.img.zip
# fi

RASPIOS=$(echo PIPIformateado.img)
rsync -avh --progress "${RASPIOS}" iotbox.img

CLONE_DIR="${OVERWRITE_FILES_BEFORE_INIT_DIR}/home/pi/odoo"

rm -rfv "${CLONE_DIR}"

if [ ! -d $CLONE_DIR ]; then
    echo "Clone Github repo"
    mkdir -pv "${CLONE_DIR}"
    git clone -b ${VERSION} --no-local --no-checkout --depth 1 ${REPO} "${CLONE_DIR}"
    cd "${CLONE_DIR}"
    git config core.sparsecheckout true
    echo "addons/web
addons/hw_*
addons/point_of_sale/tools/posbox/configuration
odoo/
odoo-bin" | tee --append .git/info/sparse-checkout > /dev/null
    git read-tree -mu HEAD
fi

cd "${__dir}"
USR_BIN="${OVERWRITE_FILES_BEFORE_INIT_DIR}/usr/bin/"
mkdir -pv "${USR_BIN}"
cd "/tmp"
curl 'https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-arm.zip' > ngrok.zip
unzip ngrok.zip
rm -v ngrok.zip
cd "${__dir}"
mv -v /tmp/ngrok "${USR_BIN}"



# Instatiate partitions to be overwritten


SECTORS_BOOT_START=$(sudo fdisk -l iotbox.img | tail -n 2 | awk 'NR==1 {print $2}')
SECTORS_BOOT_END=$((SECTORS_BOOT_START + 1048576)) # sectors to have a partition of ~512Mo
SECTORS_ROOT_START=$((SECTORS_BOOT_END + 1))

START_OF_ROOT_PARTITION=$(fdisk -l iotbox.img | tail -n 1 | awk '{print $2}')

LOOP_RASPIOS=$(kpartx -avs "${RASPIOS}")
LOOP_RASPIOS_ROOT=$(echo "${LOOP_RASPIOS}" | tail -n 1 | awk '{print $3}')
LOOP_RASPIOS_PATH="/dev/${LOOP_RASPIOS_ROOT::-2}"
LOOP_RASPIOS_ROOT="/dev/mapper/${LOOP_RASPIOS_ROOT}"

LOOP_IOT=$(kpartx -avs iotbox.img)
LOOP_IOT_ROOT=$(echo "${LOOP_IOT}" | tail -n 1 | awk '{print $3}')
LOOP_IOT_PATH="/dev/${LOOP_IOT_ROOT::-2}"
LOOP_IOT_ROOT="/dev/mapper/${LOOP_IOT_ROOT}"
LOOP_IOT_BOOT=$(echo "${LOOP_IOT}" | tail -n 2 | awk 'NR==1 {print $3}')
LOOP_IOT_BOOT="/dev/mapper/${LOOP_IOT_BOOT}"


mkdir -pv "${MOUNT_POINT}" #-p: no error if existing
mount -v "${LOOP_IOT_ROOT}" "${MOUNT_POINT}"
mount -v "${LOOP_IOT_BOOT}" "${MOUNT_POINT}/boot/"

QEMU_ARM_STATIC="/usr/bin/qemu-arm-static"
cp -v "${QEMU_ARM_STATIC}" "${MOUNT_POINT}/usr/bin/"

# 'overlay' the overwrite directory onto the mounted image filesystem
cp -av "${OVERWRITE_FILES_BEFORE_INIT_DIR}"/* "${MOUNT_POINT}"
chroot "${MOUNT_POINT}" /bin/bash -c "sudo /etc/init_posbox_image.sh"

# copy iotbox version
mkdir -pv "${MOUNT_POINT}"/var/odoo
echo "${VERSION_IOTBOX}" | tee "${MOUNT_POINT}"/var/odoo/iotbox_version "${MOUNT_POINT}"/home/pi/iotbox_version

# get rid of the git clone
rm -rfv "${CLONE_DIR}"
# and the ngrok usr/bin
rm -rfv "${OVERWRITE_FILES_BEFORE_INIT_DIR}/usr"
cp -av "${OVERWRITE_FILES_AFTER_INIT_DIR}"/* "${MOUNT_POINT}"

find "${MOUNT_POINT}"/ -type f -name "*.iotpatch"|while read iotpatch; do
    DIR=$(dirname "${iotpatch}")
    BASE=$(basename "${iotpatch%.iotpatch}")
    find "${DIR}" -type f -name "${BASE}" ! -name "*.iotpatch"|while read file; do
        patch -f --verbose "${file}" < "${iotpatch}"
    done
done

# cleanup
umount -fv "${MOUNT_POINT}"/boot/
umount -fv "${MOUNT_POINT}"/
rm -rfv "${MOUNT_POINT}"

echo "Running zerofree..."
zerofree -v "${LOOP_IOT_ROOT}" || true

sleep 10

kpartx -dv "${LOOP_IOT_PATH}"
kpartx -dv "${LOOP_RASPIOS_PATH}"
