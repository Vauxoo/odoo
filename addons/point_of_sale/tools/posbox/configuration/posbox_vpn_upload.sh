#!/usr/bin/env bash

function upload () {
    CONFIGURATION_FILE="${1}"
    OPENVPN_DIR="/home/pi/.openvpn"
    sleep 3

    # make network choice persistent
    if [ -f "${CONFIGURATION_FILE}" ] ; then
        sudo mount -o remount,rw /
        if [ ! -d "${OPENVPN_DIR}" ]; then
            logger -t posbox_vpn_upload "Creating openvpn directory.."
            sudo mkdir "${OPENVPN_DIR}"
        fi
        logger -t posbox_vpn_upload "Copying new configuration file..."
        sudo mv "${CONFIGURATION_FILE}" "${OPENVPN_DIR}/pos.conf"
        sudo mount -o remount,ro /
        sleep 5
        logger -t posbox_upload_vpn_config "Restarting openvpn..."
        sudo service openvpn restart
    fi
}

upload "${1}" &
