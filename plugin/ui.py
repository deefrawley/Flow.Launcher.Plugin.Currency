# -*- coding: utf-8 -*-

import copy
import plugin.utils
import decimal

from typing import List
from plugin.templates import RESULT_TEMPLATE, ACTION_TEMPLATE
from flowlauncher import FlowLauncher


class Main(FlowLauncher):
    messages_queue = []

    def sendNormalMess(self, title: str, subtitle: str):
        message = copy.deepcopy(RESULT_TEMPLATE)
        message["Title"] = title
        message["SubTitle"] = subtitle

        self.messages_queue.append(message)

    def sendActionMess(self, title: str, subtitle: str, method: str, value: List):
        # information
        message = copy.deepcopy(RESULT_TEMPLATE)
        message["Title"] = title
        message["SubTitle"] = subtitle

        # action
        action = copy.deepcopy(ACTION_TEMPLATE)
        action["JsonRPCAction"]["method"] = method
        action["JsonRPCAction"]["parameters"] = value
        message.update(action)

        self.messages_queue.append(message)

    def query(self, param: str) -> List[dict]:
        q = param.strip()
        args = q.split(" ")

        # Do your job at here.
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
        if len(args) == 3:
            # Check first argument is valid currency code
            if args[1].upper() not in currencies:
                self.sendNormalMess(
                    "Error - {} not a valid currency".format(args[1].upper(), "")
                )
            # Check second argument is valid currency code
            elif len(args[2]) == 3 and args[2].upper() not in currencies:
                self.sendNormalMess(
                    "Error - {} not a valid currency".format(args[2].upper(), "")
                )
            # Do the conversion but only after three char code entered
            elif len(args[2]) == 3:
                # If source and dest currencies the same just return entered amount
                if args[1].upper() == args[2].upper():
                    self.sendNormalMess(
                        "{} {} = {} {}".format(
                            args[0], args[1].upper(), args[0], args[2].upper()
                        ),
                        "",
                    )
                else:
                    try:
                        ratesxml_returncode = plugin.utils.getrates_xml()
                        ratedict = plugin.utils.populate_rates("eurofxref-daily.xml")
                        conv = plugin.utils.currconv(
                            ratedict, args[1], args[2], args[0]
                        )
                        self.sendNormalMess(
                            "{} {} = {} {} (1 {} = {} {})".format(
                                args[0],
                                args[1].upper(),
                                decimal.Decimal(conv[1]),
                                args[2].upper(),
                                args[1].upper(),
                                decimal.Decimal(conv[1]) / decimal.Decimal(args[0]),
                                args[2].upper(),
                            ),
                            "Rates date : {}".format(conv[0]),
                        )
                    # Show exceptions (for debugging as much as anything else)
                    except Exception as e:
                        self.sendNormalMess("Error - {}".format(repr(e)), "")
        # Always show the usage while there isn't a valid query
        else:
            self.sendNormalMess(
                "Currency Converter",
                "<Hotkey> <Amount> <Source currency> <Destination currency>",
            )

        return self.messages_queue
