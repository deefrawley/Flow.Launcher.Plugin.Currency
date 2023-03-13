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
    ratesURL = "http://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml"
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
        "XXX",
        "EUR",
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.max_age = self.settings.get("max_age")
        self.logger_level("info")

    def query(self, query):
        q = query.strip()
        args = q.split(" ")
        if len(args) == 1:
            self.add_item(
                title=_("<Amount> <Source currency code> <Destination currency code>"),
                subtitle=_(
                    "There will be a short delay if the currency rates file needs to be downloaded"
                ),
            )

        elif len(args) == 2:
            hint = self.applicablerates(args[1])
            self.add_item(
                title=(f", ".join([f"{x}" for x in hint])),
                subtitle=_("Source currency"),
            )
        elif len(args) == 3:
            if len(args[2]) <= 2:
                hint = self.applicablerates(args[2])
                self.add_item(
                    title=(f", ".join([f"{x}" for x in hint])),
                    subtitle=_("Destination currency"),
                )
            else:
                # Check codes are three letters
                if len(args[1]) != 3 or len(args[2]) != 3:
                    self.add_item(
                        title=_("Please enter three character currency codes")
                    )

                # Check first argument is valid currency code
                elif len(args[1]) == 3 and args[1].upper() not in self.CURRENCIES:
                    self.add_item(title=_("Error - source is not a valid currency"))

                # Check second argument is valid currency code
                elif len(args[2]) == 3 and args[2].upper() not in self.CURRENCIES:
                    self.add_item(
                        title=_("Error - destination is not a valid currency")
                    )

                # Check amount is an int or a float
                elif (
                    not args[0].isdigit() and not args[0].replace(".", "", 1).isdigit()
                ):
                    self.add_item(title=_("Error - amount must be numeric"))

                # If source and dest currencies the same just return entered amount
                elif args[1].upper() == args[2].upper():
                    self.add_item(
                        title="{} {} = {} {}".format(
                            args[0], args[1].upper(), args[0], args[2].upper()
                        )
                    )
                # Do the conversion
                else:
                    # First strip any commas from the amount
                    args[0] = args[0].replace(",", "")
                    # Get the rates
                    ratesxml_returncode = self.getrates_xml(self.max_age)
                    if ratesxml_returncode == 200:
                        ratedict = self.populate_rates("eurofxref-daily.xml")
                        conv = self.currconv(ratedict, args[1], args[2], args[0])
                        if len(conv) == 1:
                            # Something has gone wrong
                            self.add_item(title="{}".format(conv[0]))
                        else:
                            # Set up some decimal precisions to use in the result
                            # amount and converted amount use precision as entered. Conversion rate uses min 3 places
                            if "." in args[0]:
                                dec_prec = len(args[0].split(".")[1])
                                if dec_prec < 3:
                                    dec_prec2 = 3
                                else:
                                    dec_prec2 = dec_prec
                            else:
                                dec_prec = 1
                                dec_prec2 = 3
                            fmt_str = "%.{0:d}f".format(dec_prec)

                            self.add_item(
                                title=(
                                    f"{locale.format_string(fmt_str, float(args[0]), grouping=True)} {args[1].upper()} = "
                                    f"{locale.format_string(fmt_str, round(decimal.Decimal(conv[1]), dec_prec), grouping=True)} "
                                    f"{args[2].upper()} "
                                    f"(1 {args[1].upper()} = "
                                    f"{round(decimal.Decimal(conv[1]) / decimal.Decimal(args[0]),dec_prec2,)} "
                                    f"{args[2].upper()})"
                                ),
                                subtitle=_("Rates date : {}").format(conv[0]),
                            )
                    else:
                        self.add_item(
                            title=_("Couldn't download the rates file"),
                            subtitle=_("{} - check log for more details").format(
                                ratesxml_returncode
                            ),
                        )

        else:
            pass

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
                r = requests.get(self.ratesURL)
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
        # converted list - if error return error message, if not error return date and converted amount
        converted = []
        # Check source currency is in the rates dict -catch odd errors like the bank suspending some rates
        if (not sourcecurr.upper() in rates and sourcecurr.upper() != "EUR") or (
            not destcurr.upper() in rates and destcurr.upper() != "EUR"
        ):
            self.logger.error(
                f"Source or destination currency not in rates dict - {sourcecurr} or {destcurr}"
            )
            converted.append(
                _("Error - expected source or destination currency not in rates file")
            )
            return converted
        # Check for zero amount, warn and don't convert
        if decimal.Decimal(amount) == 0:
            converted.append(_("Warning - amount entered must be greater than zero"))
            return converted 

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
                        return converted
                    else:
                        destrate = rates[rate]
                if rate == sourcecurr.upper():
                    sourcerate = rates[rate]
        # Convert via the EURO
        sourceEuro = (1 / decimal.Decimal(sourcerate)) * decimal.Decimal(amount)
        converted.append(decimal.Decimal(sourceEuro) * decimal.Decimal(destrate))
        return converted

    def applicablerates(self, ratestr):
        choices = [i for i in self.CURRENCIES if i.upper().startswith(ratestr.upper())]
        if not choices:
            choices.append(_("No matches found"))
        return choices


if __name__ == "__main__":
    Currency()
