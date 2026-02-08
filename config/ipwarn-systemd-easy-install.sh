#!/usr/bin/env bash

set -e
set -u

if [[ $EUID > 0 ]]
  then echo "Please run as root"
  exit
fi


# Install Python and pip if not present
echo "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "Python3 is not installed. Installing..."
    apt-get update
    apt-get install -y python3 python3-pip python3-venv
else
    echo "Python3 found: $(python3 --version)"
fi

if ! command -v pip3 &> /dev/null; then
    echo "pip3 is not installed. Installing..."
    apt-get update
    apt-get install -y python3-pip
fi

# Download files (config and service)
echo "Downloading files..."
mkdir -p /tmp/ipwarn-install
pushd /tmp/ipwarn-install
curl -O https://raw.githubusercontent.com/caldito/ipwarn/master/config/ipwarn.conf.example
curl -O https://raw.githubusercontent.com/caldito/ipwarn/master/config/ipwarn.service
echo "Files downloaded successfully..."

# Create user
echo "Creating user..."
useradd --system ipwarn || true
echo "User created successfully"

# Install ipwarn
echo "Installing ipwarn..."
pip3 install ipwarn || (
    echo "ipwarn not available on PyPI yet, installing from source..."
    apt-get install -y git
    cd /tmp
    git clone https://github.com/caldito/ipwarn.git
    cd ipwarn
    pip3 install -e .
)

# Copy config and set permissions
echo "Copying files and setting permissions..."
mkdir -p /etc/ipwarn
chown ipwarn:ipwarn /etc/ipwarn
chmod 755 /etc/ipwarn

if [ ! -f /etc/ipwarn/ipwarn.conf ]; then
    cp ./ipwarn.conf.example /etc/ipwarn/ipwarn.conf
else
    echo "Config file already exists, skipping..."
fi

chown ipwarn:ipwarn /etc/ipwarn/ipwarn.conf
chmod 600 /etc/ipwarn/ipwarn.conf

cp ./ipwarn.service /etc/systemd/system/ipwarn.service
chown root /etc/systemd/system/ipwarn.service
chmod 644 /etc/systemd/system/ipwarn.service
popd
echo "Files copied and permissions set successfully"

# Prepare systemd service
echo "Preparing systemd service..."
systemctl daemon-reload
systemctl enable ipwarn.service
systemctl start ipwarn.service
printf "Systemd service prepared successfully\n\n"

# Finish
printf "ipwarn installation completed successfully!\n\n"

echo "The program is now running with default config. You can edit config in \"/etc/ipwarn/ipwarn.conf\" and then restart ipwarn service running \"systemctl restart ipwarn\""
echo "View logs with: journalctl -u ipwarn -f"
