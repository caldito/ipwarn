# ipwarn

A simple Dynamic DNS Update Client written in Bash.

The purpose of this project is to be able to update DNS records of the main hosting providers directly and also provide other functionalities like notifiying through Telegram.

For now it is able to update Godaddy's DNS records and notify using Telegram Bots.

## Prerequisites :clipboard:

In order to work ipwarn needs `curl`.

## Configuration :gear:
This software needs to use the APIs of different services. Due to this in the config file `/etc/ipwarn/ipwarn.conf` you can choose the services to enable and store the tokens for those. The configs inside this file are quite self descriptive, so I won't go into details here.

With the flag `-c` or `--config` you can override the default location of this file.

## Running :running:

### Docker
```
docker run --mount type=bind,source=your-custom-ipwarn.conf,target=/etc/ipwarn/ipwarn.conf pablogcaldito/ipwarn:v1.0.1
```
### Systemd install
Run the install script
```
curl -O https://raw.githubusercontent.com/caldito/ipwarn/master/config/ipwarn-systemd-easy-install.sh && sudo bash ./ipwarn-systemd-easy-install.sh
```
Override the config found in `/etc/ipwarn/ipwarn.conf`

Restart the service
```
sudo systemd restart ipwarn.service
```

### Standalone run

After clonning the repo go into its directory and run:
./ipwarn --config your-config-file


## Built with :hammer_and_wrench:

* [Telegram Bot API](https://core.telegram.org/bots/apis) - Used to notify when IP changes
* [GoDaddy API](https://developer.godaddy.com/) - Used to update DNS records in GoDaddy

## Contributing :handshake:

Please read [CONTRIBUTING.md](https://github.com/caldito/ipwarn/blob/master/CONTRIBUTING.md) for details on the process for submitting pull requests to the project.

Also read [CODE_OF_CONDUCT.md](https://github.com/caldito/ipwarn/blob/master/CODE_OF_CONDUCT.md) for details on the code of conduct.

## Authors :black_nib:

See the [contributors](https://github.com/caldito/ipwarn/graphs/contributors) page.

## License :balance_scale:
This project is licensed under the MIT License - see the [LICENSE](https://github.com/caldito/ipwarn/blob/master/LICENSE) file for details
