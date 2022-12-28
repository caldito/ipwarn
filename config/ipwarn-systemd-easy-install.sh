#!/usr/bin/env bash

set -e
set -u

if [[ $EUID > 0 ]]
  then echo "Please run as root"
  exit
fi


# Download files (program, config and service)
echo "Downloading files..."
mkdir -p /tmp/ipwarn-install
pushd /tmp/ipwarn-install
curl -O https://raw.githubusercontent.com/caldito/ipwarn/master/ipwarn
curl -O https://raw.githubusercontent.com/caldito/ipwarn/master/config/ipwarn.conf
curl -O https://raw.githubusercontent.com/caldito/ipwarn/master/config/ipwarn.service
echo "Files downloaded successfully..."

# Create user
echo "Creating user..."
useradd --system ipwarn || true
echo "User created successfully"

# Copy files and set permissions
echo "Copying files and setting permissions..."
cp ./ipwarn /usr/local/bin/ipwarn
chown ipwarn:ipwarn /usr/local/bin/ipwarn
chmod 755 /usr/local/bin/ipwarn

mkdir -p /etc/ipwarn
chown ipwarn:ipwarn /etc/ipwarn
chmod 755 /etc/ipwarn

cp ./ipwarn.conf /etc/ipwarn/ipwarn.conf
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
systemctl start ipwarn.service
printf "Systemd service prepared successfully\n\n"

# Finish
printf "ipwarn installation completed successfully!\n\n"

echo "The program is now running with the default config. You can edit the config in \"/etc/ipwarn/ipwarn.conf\" and then restart the ipwarn service runinng \"systemctl restart ipwarn\""
echo "If you wish the service to run on startup run: systemctl enable ipwarn.service"
