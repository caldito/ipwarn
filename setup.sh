#!/usr/bin/env bash

check_dependencies(){
    missing=""
    command -v curl >/dev/null 2>&1 || missing="${missing} curl"
    command -v echo >/dev/null 2>&1 || missing="${missing} echo"
    command -v whoami >/dev/null 2>&1 || missing="${missing} whoami"
    command -v sed >/dev/null 2>&1 || missing="${missing} sed"
    [ -z "$missing" ] || { echo >&2 "Missing dependencies:${missing}. Exiting"; exit 1; }
}

write_config(){
    echo 'IP=""' >> /etc/ipwarn.conf
    echo >> /etc/ipwarn.conf
    echo '# The purpose of this file is to store the API keys and other information in order to be able to use the services you need.' >> /etc/ipwarn.conf
    echo '# Fill in the data of the services you are going to use.' >> /etc/ipwarn.conf
    echo '# Do not edit the IP variable.' >> /etc/ipwarn.conf
    echo >> /etc/ipwarn.conf
    echo '#---- Edit below this line ----#' >> /etc/ipwarn.conf
    echo >> /etc/ipwarn.conf
    echo '#Telegram configuration' >> /etc/ipwarn.conf
    echo 'TEL_API_TOKEN=""' >> /etc/ipwarn.conf
    echo 'TEL_API_ID=""' >> /etc/ipwarn.conf
    echo >> /etc/ipwarn.conf
    echo '#GoDaddy configuration' >> /etc/ipwarn.conf
    echo 'GD_DOMAIN=""' >> /etc/ipwarn.conf
    echo 'GD_RECORD_NAME="@" # Default value' >> /etc/ipwarn.conf
    echo 'GD_RECORD_TYPE="A" # Default value' >> /etc/ipwarn.conf
    echo 'GD_API_KEY=""' >> /etc/ipwarn.conf
    echo 'GD_API_SECRET=""' >> /etc/ipwarn.conf
    echo "Done. Edit /etc/ipwarn.conf to configure warning channels"
}

main(){
    if [ "$(whoami)" != "root" ]; then
        echo "Setup should be executed as root. Exiting"
        exit 1
    fi
    check_dependencies
    write_config
    chmod 600 /etc/ipwarn.conf
    cp ${PWD}/ipwarn /usr/local/bin/ipwarn
    chmod 755 /usr/local/bin/ipwarn
}

main

