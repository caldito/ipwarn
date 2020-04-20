# ipwarn

A simple Dynamic DNS Update Client written in Shell for Unix and Unix-like operating systems. The purpose of this project is to be able to update DNS records of the main hosting providers directly and also provide other functionalities like notifiying through Telegram.

For now it is able to update Godaddy's DNS records and notify using Telegram Bots.

## Prerequisites :clipboard:

In order to work ipwarn needs
* `curl`
* `sed`

All of these can be easily installed (if are not already by default) in all Unix and Unix-like operating systems.

## Installing :wrench:

First, clone the repository from GitHub

```bash
git clone https://github.com/pablogcaldito/ipwarn.git
```
After that, change to the repositorie's directory

```bash
cd ipwarn
```
Finally, use run the setup as administrator with bash as superuser

```bash
sudo bash setup.sh
```
Now, ipwarn is installed at `/usr/local/bin/ipwarn` and can be executed from terminal just typing `ipwarn`
## Configuration :gear:
This software is intended to use the APIs of different services. That is why you have to store the tokens of the services you want to use in the configuration file `/etc/ipwarn.conf` 

---
So, for instance, if you want ipwarn to be able to update GoDaddy DNS records and send you a message via Telegram when the IP changes you should make these changes in the configuration file:

`TEL_API_TOKEN=""` --> `TEL_API_TOKEN="your-telegram-bot-api-token"`

`TEL_API_ID=""` --> `TEL_API_ID="your-telegram-api-id"`

`GD_DOMAIN=""` --> `GD_DOMAIN="your-domain-name"`

`GD_API_KEY=""` --> `GD_API_KEY="your-godaddy-api-key"`

`GD_API_SECRET=""` --> `GD_API_SECRET="your-godaddy-api-key"`

The fileds that are already filled in the cofiguration file can be left by default.

## Deployment :package:

The flags you pass to the program are important because they determine the service(s) it will use. If you don't put any flag the ipwarn will only print the change of IP.

---
For example, if you want that send you a telegram message when it happens you will have use the telegram flag:

`ipwarn -t` or `ipwarn --telegram`

For GoDaddy 

`ipwarn -g` or `ipwarn --godaddy`

Of course, you can use multiple flags. For checking all the options available use

`ipwarn -h` or `ipwarn --help`

## Built With :hammer_and_wrench:	

* [Telegram Bot API](https://core.telegram.org/bots/apis) - Used to notify when IP changes
* [GoDaddy API](https://developer.godaddy.com/) - Used to update DNS records in GoDaddy

## Contributing :handshake:

Please read [CONTRIBUTING.md](https://github.com/pablogcaldito/ipwarn/blob/master/CONTRIBUTING.md) for details on the process for submitting pull requests to us.

Also read [CODE_OF_CONDUCT.md](https://github.com/pablogcaldito/ipwarn/blob/master/CODE_OF_CONDUCT.md) for details on our code of conduct.

## Authors :black_nib:

* **Pablo Gómez-Caldito Gómez** - *Initial work* - [pablogcaldito](https://github.com/pablogcaldito)


## License :balance_scale:
This project is licensed under the MIT License - see the [LICENSE](https://github.com/pablogcaldito/ipwarn/blob/master/LICENSE) file for details

