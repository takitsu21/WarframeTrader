[![ko-fi](https://www.ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/U7U1RSV5)

[![PyPI pyversions](https://img.shields.io/badge/python-3.8-blue)](https://www.python.org/)  ![AppVeyor](https://img.shields.io/appveyor/ci/takitsu21/WarframeTrader) [![Codacy Badge](https://api.codacy.com/project/badge/Grade/1f714471f70140e3a551936af53e9ea9)](https://app.codacy.com/app/takitsu21/WarframeTrader?utm_source=github.com&utm_medium=referral&utm_content=takitsu21/WarframeTrader&utm_campaign=Badge_Grade_Dashboard) [![Discord](https://img.shields.io/discord/556268083681951759?color=blue&label=discord)](http://discord.gg/wTxbQYb) ![GitHub pull requests](https://img.shields.io/github/issues-pr/takitsu21/WarframeTrader) ![GitHub issues](https://img.shields.io/github/issues/takitsu21/WarframeTrader) [![GitHub](https://img.shields.io/github/license/takitsu21/WarframeTrader)](LICENCE)

# WarframeTrader

This bot has many features for warframe, he provide Worldstate data and use warframe.market API to trade using discord.
More features are coming.

## Commands

Prefix : **`* or custom or @mention`**

| Command | Description |
| ------- | ----------- |
| **`<*wtb / *b> <pc / xbox / ps4 / swi> [ITEM_NAME]`** | Views 7 sellers sort by prices and status (Online in game) |
| **`<*wts / *s> <pc / xbox / ps4 / swi> [ITEM_NAME]`** | Views 7 buyers sort by prices and status (Online in game) |
| **`<*riven / *r> <pc / xbox / ps4 / swi> [ITEM_NAME]`** | Viewss 6 riven mod sorted by ascending prices and status (Online in game) |
| **`<*ducats / *d>`** | Views 18 worth it items to sell in ducats |
| **`<*fissures / *f> <pc / ps4 / xb1 / swi> <FILTER>`** | Views current fissures available, you can add filter, for exemple **`*f pc requiem axi survival`** the filter arguments will show only requiem, axi and survival missions (infinite filter accepted separated with space) |
| **`*sortie`** | Views current sortie |
| **`*baro`** | Views baro ki'teer inventory and dates |
| **`*news <pc / ps4 / xb1 / swi>`** | Views news about Warframe |
| **`*earth`** | Views earth cycle |
| **`*wiki [QUERY]`** | Views wiki url according to the query |
| **`*event`** | Views current running events |
| **`*acolytes <pc / xbox / ps4 / swi>`** | Views current acolytes available |
| **`*bug [MESSAGE]`** | Send me a bug report, this will helps to improve the bot |
| **`*suggestion [MESSAGE]`** | Suggestion to add for the bot, all suggestions are good don't hesitate |
| **`*language [COUNTRY_CODE]`** | Languages supported for now (**fr**, **en**). Languages not supported but you can contribute (de, es, it, ja, ko, pl, pt, ru, tc, tr, zh) [Here](https://github.com/takitsu21/WarframeTrader/tree/master/locales) by doing pull requests. |
| **`*ping`** | Views bot latency |
| **`*about`** | Bot info |
| **`*donate`** | Link to support me |
| **`*vote`** | An other way to support me |
| **`*support`** | Discord support if you need help or want to discuss with me |
| **`*invite`** | Views bot link invite |
| **`*set_prefix [PREFIX]`** | Set new prefix (Only admins) |
| **`*get_prefix`** | Views actual guild prefix |
| **`*settings [--delete] [n / no]`** | Change message settings (Only admin) |
| **`*settings [--delay] [TIME_IN_SECOND]`** | Change message delay setting (Only admin) |
| **`<*help / *h>`** | Views bot commands |

## Few examples

![Example WTB ](https://i.imgur.com/iwMiNwA.png)

![Graph stats](https://i.imgur.com/MsoIiRW.png)

![Riven list](https://i.imgur.com/rLhuSxk.png)

![Sortie](https://i.imgur.com/v7qQ4S7.png)

![Arbitration](https://i.imgur.com/iPIyV1N.png)

## Built With

* [discord.py](https://discordpy.readthedocs.io/en/latest/)

## Author

* [**takitsu21**](https://github.com/takitsu21/)

### License

This project is licensed under the GNU General Public License v3.0 License - see the [LICENSE.md](LICENSE) file for details.

### Deployment

* AWS Amazon
