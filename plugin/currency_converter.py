# -*- coding: utf-8 -*-
import textwrap
import plugin.utils
import decimal
import locale

from plugin.translation import _
from flox import Flox


class Currency(Flox):
    locale.setlocale(locale.LC_ALL, "")
    # TODO - save list to settings and update from each XML download and just use this list as a first time default
    currencies = [
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

    def query(self, query):
        q = query.strip()
        args = q.split(" ")
        if len(args) == 3:
            # Check codes are three letters
            if len(args[1]) != 3 or len(args[2]) != 3:
                self.add_item(title=_("Please enter three character currency codes"))

            # Check first argument is valid currency code
            elif len(args[1]) == 3 and args[1].upper() not in self.currencies:
                self.add_item(title=_("Error - {} not a valid currency")).format(
                    args[1].upper()
                )
            # Check second argument is valid currency code
            elif len(args[2]) == 3 and args[2].upper() not in self.currencies:
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
                    try:
                        # First strip any commas from the amount
                        args[0] = args[0].replace(",", "")
                        # TODO Handle non 200 return code
                        ratesxml_returncode = plugin.utils.getrates_xml()
                        ratedict = plugin.utils.populate_rates("eurofxref-daily.xml")
                        conv = plugin.utils.currconv(
                            ratedict, args[1], args[2], args[0]
                        )
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
                    # Show exceptions (for debugging as much as anything else)
                    except Exception as e:
                        self.add_item("Error - {}").format(repr(e))
        # Always show the usage while there isn't a valid query
        else:
            self.add_item(
                title=_("<Amount> <Source currency code> <Destination currency code>"),
                subtitle=_(
                    "There will be a short delay if the currency rates file needs to be downloaded"
                ),
            )
            title = _("Available currencies:")
            subtitle = ", ".join(self.currencies)
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
            # self.add_item(
            #    title=_("Currencies available:"),
            #    subtitle=_(f"{', '.join(self.currencies)}"),
            # )


if __name__ == "__main__":
    Currency()
