# -*- coding: utf-8 -*-
import textwrap

# import plugin.utils
import decimal
import locale
import requests
import decimal
import xml.etree.ElementTree as ET
import os
import datetime

from plugin.translation import _
from flox import Flox


class Currency(Flox):
    locale.setlocale(locale.LC_ALL, "")
    # TODO - save list to settings and update from each XML download and just use this list as a first time default
    CURRENCIES = [
        "AUD",
        "BGN",
        "BRL",
        "CAD",
        "CHF",
        "CNY",
        "CZK",
        "DKK",
        "GBP",
        "HKD",
        "HRK",
        "HUF",
        "IDR",
        "ILS",
        "INR",
        "ISK",
        "JPY",
        "KRW",
        "MXN",
        "MYR",
        "NOK",
        "NZD",
        "PHP",
        "PLN",
        "RON",
        "RUB",
        "SEK",
        "SGD",
        "THB",
        "TRY",
        "USD",
        "ZAR",
        "EUR",
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.max_age = self.settings.get("max_age")
        self.logger_level("info")

    def query(self, query):
        q = query.strip()
        args = q.split(" ")
        if len(args) == 3:
            # Check codes are three letters
            if len(args[1]) != 3 or len(args[2]) != 3:
                self.add_item(title=_("Please enter three character currency codes"))

            # Check first argument is valid currency code
            elif len(args[1]) == 3 and args[1].upper() not in self.CURRENCIES:
                self.add_item(title=_("Error - {} not a valid currency")).format(
                    args[1].upper()
                )
            # Check second argument is valid currency code
            elif len(args[2]) == 3 and args[2].upper() not in self.CURRENCIES:
                self.add_item(title=_("Error - {} not a valid currency")).format(
                    args[2].upper()
                )
            # Do the conversion
            else:
                # If source and dest currencies the same just return entered amount
                if args[1].upper() == args[2].upper():
                    self.add_item(
                        title="{} {} = {} {}".format(
                            args[0], args[1].upper(), args[0], args[2].upper()
                        )
                    )
                else:

                    # First strip any commas from the amount
                    args[0] = args[0].replace(",", "")
                    ratesxml_returncode = self.getrates_xml(self.max_age)
                    if ratesxml_returncode == 200:
                        ratedict = self.populate_rates("eurofxref-daily.xml")
                        conv = self.currconv(ratedict, args[1], args[2], args[0])
                        # decimal.getcontext().prec = conv[2]
                        self.add_item(
                            title=(
                                f"{locale.format_string('%.3f', float(args[0]), grouping=True)} {args[1].upper()} = "
                                f"{locale.format_string('%.3f', round(decimal.Decimal(conv[1]), conv[2]), grouping=True)} "
                                f"{args[2].upper()} "
                                f"(1 {args[1].upper()} = "
                                f"{round(decimal.Decimal(conv[1]) / decimal.Decimal(args[0]),conv[2],)} "
                                f"{args[2].upper()})"
                            ),
                            subtitle=f"Rates date : {conv[0]}",
                        )
                    else:
                        self.add_item(
                            title=_("Couldn't download the rates file"),
                            subtitle=_(
                                f"{ratesxml_returncode} - check log for more details"
                            ),
                        )

        # Always show the usage while there isn't a valid query
        else:
            self.add_item(
                title=_("<Amount> <Source currency code> <Destination currency code>"),
                subtitle=_(
                    "There will be a short delay if the currency rates file needs to be downloaded"
                ),
            )
            title = _("Available currencies:")
            subtitle = ", ".join(self.CURRENCIES)
            lines = textwrap.wrap(subtitle, 110)
            if len(lines) > 1:
                self.add_item(
                    title=(title),
                    subtitle=(lines[0]),
                )
                for line in range(1, len(lines)):
                    self.add_item(title="", subtitle=(lines[line]), icon="garbage")
            else:
                self.add_item(
                    (title),
                    (subtitle),
                )

    def populate_rates(self, xml):
        tree = ET.parse(xml)
        root = tree.getroot()
        rates = {}
        for root_Cube in root.findall(
            "{http://www.ecb.int/vocabulary/2002-08-01/eurofxref}Cube"
        ):
            for time_Cube in root_Cube.findall(
                "{http://www.ecb.int/vocabulary/2002-08-01/eurofxref}Cube"
            ):
                rates.update({"date": "{}".format(time_Cube.attrib["time"])})
                for currency_Cube in time_Cube.findall(
                    "{http://www.ecb.int/vocabulary/2002-08-01/eurofxref}Cube"
                ):
                    rates.update(
                        {
                            "{}".format(currency_Cube.attrib["currency"]): "{}".format(
                                currency_Cube.attrib["rate"]
                            )
                        }
                    )
        return rates

    def getrates_xml(self, max_age):

        xmlfile = "eurofxref-daily.xml"
        exists = os.path.isfile(xmlfile)
        getnewfile = True
        if exists:
            current = datetime.datetime.now()
            t = os.path.getmtime(xmlfile)
            file = datetime.datetime.fromtimestamp(t)
            if (current - file) > datetime.timedelta(hours=int(max_age)):
                getnewfile = True
            else:
                getnewfile = False
        if getnewfile:
            try:
                URL = "http://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml"
                r = requests.get(URL)
                with open(xmlfile, "wb") as file:
                    file.write(r.content)
                self.logger.info(f"Download rates file returned {r.status_code}")
                return r.status_code
            except requests.exceptions.HTTPError as e:
                self.logger.error(f"HTTP Error - {repr(e)}")
                return _("HTTP Error")
            except requests.exceptions.ConnectionError as e:
                self.logger.error(f"Connection Error - {repr(e)}")
                return _("Connection Error")
            except requests.exceptions.RequestException as e:
                self.logger.error(f"Unspecified Download Error - {repr(e)}")
                return _("Unspecifed Download Error")
        else:
            return 200

    def currconv(self, rates, sourcecurr, destcurr, amount):
        converted = []

        # Change the decimal precision to match the number of digits in the amount
        if "." in amount:
            dec_prec = len(amount.split(".")[1])
        # Default to precision of 3 decimal places
        else:
            dec_prec = 3

        # sourcerate = 1
        destrate = 1
        if destcurr.upper() == "EUR":
            for rate in rates:
                if rate == "date":
                    converted.append(rates[rate])
                if rate == sourcecurr.upper():
                    converted.append(
                        (1 / decimal.Decimal(rates[rate])) * decimal.Decimal(amount)
                    )
                    converted.append(dec_prec)
                    return converted
        else:
            for rate in rates:
                if rate == "date":
                    converted.append(rates[rate])
                if rate == destcurr.upper():
                    # If source is EURO then straight convert and return
                    if sourcecurr.upper() == "EUR":
                        converted.append(
                            decimal.Decimal(rates[rate]) * decimal.Decimal(amount)
                        )
                        converted.append(dec_prec)
                        return converted
                    else:
                        destrate = rates[rate]
                if rate == sourcecurr.upper():
                    sourcerate = rates[rate]
        # Convert via the EURO
        sourceEuro = (1 / decimal.Decimal(sourcerate)) * decimal.Decimal(amount)
        converted.append(decimal.Decimal(sourceEuro) * decimal.Decimal(destrate))
        converted.append(dec_prec)
        return converted


if __name__ == "__main__":
    Currency()
