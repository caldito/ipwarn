#!/bin/bash

write_config(){
    echo 'IP=""' >> /etc/ipwarn.conf
    echo 'TEL_TOKEN=""' >> /etc/ipwarn.conf
    echo 'TEL_ID=""' >> /etc/ipwarn.conf
    echo 'GD_DOMAIN=""' >> /etc/ipwarn.conf
    echo 'GD_NAME="@"' >> /etc/ipwarn.conf
    echo 'GD_TYPE="A"' >> /etc/ipwarn.conf
    echo 'GD_KEY=""' >> /etc/ipwarn.conf
    echo 'GD_SECRET=""' >> /etc/ipwarn.conf
    echo "edit /etc/ipwarn.conf to configure warning channels"
}

main(){
    if [ "$(whoami)" != "root" ]; then
        echo "Setup should be executed as root. Exiting"
        exit 1
    fi
    #write_config
    #chmod 600 /etc/ipwarn.conf
    cp ${PWD}/ipwarn /usr/local/bin/ipwarn
    chmod 755 /usr/local/bin/ipwarn
}

main

