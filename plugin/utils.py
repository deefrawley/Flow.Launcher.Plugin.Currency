import requests
import decimal
import xml.etree.ElementTree as ET
import os
import datetime
import math


def populate_rates(xml):
    """Extracts conversion rates from European Central Bank XML file

    Note :- This ONLY uses the daily file, not historical rates

    Parameters
    ----------
    self:
        Method instance
    xml : path
        XML file to process, assumed to be in plugin directory

    Returns
    -------
    dict
        Dictionary where first pair is the date from the XML file and
        following pairs are currenct and rate (against the EURO)
    """

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


def getrates_xml():
    """Generate XML file of conversion rates from European Central Bank

    If an XML file already exists in the plugin directory, and it is less
    than two hours old it will use that. Otherwise it gets a fresh copy from
    the ECB web site

    Parameters
    ----------
    self:
        Method instance

    Returns
    -------
    str
        Status code of the web call. Forced to '200' if it just uses the
        existing file
    """

    xmlfile = "eurofxref-daily.xml"
    exists = os.path.isfile(xmlfile)
    getnewfile = True
    if exists:
        current = datetime.datetime.now()
        t = os.path.getmtime(xmlfile)
        file = datetime.datetime.fromtimestamp(t)
        if (current - file) > datetime.timedelta(hours=2):
            getnewfile = True
        else:
            getnewfile = False
    if getnewfile:
        URL = "http://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml"
        r = requests.get(URL)
        with open(xmlfile, "wb") as file:
            file.write(r.content)
        return r.status_code
    else:
        return 200


def currconv(rates, sourcecurr, destcurr, amount):
    """Converts from one currency to another

    Parameters
    ----------
    self:
        Method instance
    rates: dict
        Dictionary generated in populate_rates
    sourcecurr: str
        Source currency three char code
    destcurr: str
        Destination currency three char code
    amount: str
        Amount to convert

    Returns
    -------
    list
        Date from the currency XML file and the converted amount, and the precision
    """

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