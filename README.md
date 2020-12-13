# Flow.Plugin.Currency

Currency conversion for the [Flow launcher](https://github.com/Flow-Launcher/Flow.Launcher)

### About

Uses the [Eurpoean Central Bank](https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/index.en.html) daily rates to get and convert currency exchange rates.

Currency code that can be used are:

'AUD' , 'BGN' , 'BRL' , 'CAD' , 'CHF' , 'CNY' , 'CZK' , 'DKK' , 'GBP', 'HKD' , 'HRK' , 'HUF' , 'IDR' , 'ILS' , 'INR' , 'ISK' , 'JPY' , 'KRW', 'MXN','MYR' , 'NOK' , 'NZD' , 'PHP' , 'PLN' , 'RON' , 'RUB' , 'SEK', 'SGD' , 'THB' , 'TRY' , 'USD' , 'ZAR' , 'EUR'

### Requirements

Python 3.5 or later installed on your system, with python.exe in your PATH variable (this is a general requirement to use Python plugins with Flow).
See requirements.txt for package dependencies.

You must be online when you run the plugin to download the XML or you will get a connection error. If the local XML file is 2 hours or less old (that is, you've run the plugin before in the previous two hours), it will just use the local file.

### Installing

Add the Flow.Plugin.Currency directory to %APPDATA%\FlowLauncher\Plugins\ and restart Flow.

### Usage

| Keyword                                                          | Description    |
| ---------------------------------------------------------------- | -------------- |
| `cc {amount} {source currency code} {destination currency code}` | Convert amount |
