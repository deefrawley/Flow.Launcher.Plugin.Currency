# -*- coding: utf-8 -*-

import copy
import plugin.utils
import decimal

from typing import List
from flox import Flox

class Currency(Flox):
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
                self.add_item(
                    title="Please enter three character currency codes"
                )

            # Check first argument is valid currency code
            elif len(args[1]) == 3 and args[1].upper() not in self.currencies:
                self.add_item(
                    title="Error - {} not a valid currency").format(args[1].upper()
                )
            # Check second argument is valid currency code
            elif len(args[2]) == 3 and args[2].upper() not in self.currencies:
                self.add_item(
                    title="Error - {} not a valid currency").format(args[2].upper()
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
                        ratesxml_returncode = plugin.utils.getrates_xml()
                        ratedict = plugin.utils.populate_rates("eurofxref-daily.xml")
                        conv = plugin.utils.currconv(
                            ratedict, args[1], args[2], args[0]
                        )
                        # decimal.getcontext().prec = conv[2]
                        self.add_item(
                            title = (f"{args[0]} {args[1].upper()} = " 
                                        f"{round(decimal.Decimal(conv[1]), conv[2])} " 
                                        f"{args[2].upper()} "
                                        f"(1 {args[1].upper()} = "
                                        f"{round(decimal.Decimal(conv[1]) / decimal.Decimal(args[0]),conv[2],)} "
                                        f"{args[2].upper()})"),
                            subtitle = f"Rates date : {conv[0]}")
                    # Show exceptions (for debugging as much as anything else)
                    except Exception as e:
                        self.add_item("Error - {}").format(repr(e))
        # Always show the usage while there isn't a valid query
        else:
            self.add_item(
                title = "Currency Converter 2.0",
                subtitle = f"<Hotkey> <Amount> <Source currency> <Destination currency>",
            )

if __name__ == "__main__":
    Currency()