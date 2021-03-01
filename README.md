# Currency Converter (Flow.Launcher.Plugin.Currency)

Currency conversion for the [Flow Launcher](https://github.com/Flow-Launcher/Flow.Launcher)

![screenshot](assets/cc_screenshot.png)

### About

Uses the [European Central Bank](https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/index.en.html) daily rates to get and convert currency exchange rates.

Currency code that can be used are:

'AUD' , 'BGN' , 'BRL' , 'CAD' , 'CHF' , 'CNY' , 'CZK' , 'DKK' , 'GBP', 'HKD' , 'HRK' , 'HUF' , 'IDR' , 'ILS' , 'INR' , 'ISK' , 'JPY' , 'KRW', 'MXN','MYR' , 'NOK' , 'NZD' , 'PHP' , 'PLN' , 'RON' , 'RUB' , 'SEK', 'SGD' , 'THB' , 'TRY' , 'USD' , 'ZAR' , 'EUR'

### Requirements

Python 3.5 or later installed on your system, with python.exe in your PATH variable and this path updated in the Flow Launcher settings (this is a general requirement to use Python plugins with Flow). As of v1.7, Flow Launcher should take care of the installation of Python for you if it is not on your system.

You must be online when you run the plugin in Flow to download the currency XML file, or you will get a connection error. If the local XML file is 2 hours or less old (that is, you've run the plugin before in the previous two hours), it will just use the local file.

### Installing

#### Package Manager

Use the `pm install` command from within Flow itself.

#### Manual

Add the Flow.Launcher.Plugin.Currency directory to %APPDATA%\Roaming\FlowLauncher\Plugins\ and restart Flow.

#### Python Package Requirements

Regardless of the method used to install, the user must currently manually ensure that the correct Python packages are installed within the same Python environment used by Flow. The `requirements.txt` file in this repo outlines which packages are needed. This can be found online here on Github, as well as in the local plugin directory once installed (%APPDATA%\Roaming\FlowLauncher\Plugins\Currency Converter-X.X.X\ where X.X.X is the currently installed version)

The easiest way to install these packages is to use the following command in a Windows Command Prompt or Powershell Prompt

`pip install -r requirements.txt`

Remember you need to be in the local directory containing the requirements text file.

### Localisation

Currently English and Chinese language supported. Edit the .env file to change the language.

### Usage

| Keyword                                                          | Description                                 |
| ---------------------------------------------------------------- | ------------------------------------------- |
| `cc {amount} {source currency code} {destination currency code}` | Convert amount from source to dest currency |

### Problems, errors and feature requests

Open an issue in this repo.
