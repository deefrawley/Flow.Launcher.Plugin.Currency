# Currency Converter (Flow.Launcher.Plugin.Currency)

Currency conversion for the [Flow Launcher](https://github.com/Flow-Launcher/Flow.Launcher)

![screenshot](assets/cc_screenshot.png)

### About

Uses the [European Central Bank](https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/index.en.html) daily rates to get and convert currency exchange rates.

Currency code that can be used are:

'AUD' , 'BGN' , 'BRL' , 'CAD' , 'CHF' , 'CNY' , 'CZK' , 'DKK' , 'GBP', 'HKD' , 'HRK' , 'HUF' , 'IDR' , 'ILS' , 'INR' , 'ISK' , 'JPY' , 'KRW', 'MXN','MYR' , 'NOK' , 'NZD' , 'PHP' , 'PLN' , 'RON' , 'RUB' , 'SEK', 'SGD' , 'THB' , 'TRY' , 'USD' , 'ZAR' , 'EUR'

### Requirements

Python 3.5 or later installed on your system, with python.exe in your PATH variable and this path updated in the Flow Launcher settings (this is a general requirement to use Python plugins with Flow).
See requirements.txt for package dependencies. Install these with

`pip install -r requirements.txt`

You must be online when you run the plugin in Flow to download the currency XML file, or you will get a connection error. If the local XML file is 2 hours or less old (that is, you've run the plugin before in the previous two hours), it will just use the local file.

### Installing

#### Package Manager

Use the `pm install` command from within Flow itself

#### Manual

Add the Flow.Launcher.Plugin.Currency directory to %APPDATA%\Roaming\FlowLauncher\Plugins\ and restart Flow.

### Localisation

Currently English and Chinese language supported. Edit the .env file to change the language.

### Usage

| Keyword                                                          | Description                                 |
| ---------------------------------------------------------------- | ------------------------------------------- |
| `cc {amount} {source currency code} {destination currency code}` | Convert amount from source to dest currency |

### Problems, errors and feature requests

Open an issue in this repo.
