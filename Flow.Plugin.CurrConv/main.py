import requests
import decimal
import xml.etree.ElementTree as ET
import os
import datetime
import math
from wox import FlowLauncher


class Main(FlowLauncher):
    """Main class required for Python plugins"""
    
    def request(self,url):
        """Checks for proxy set and uses that for a Requests library 'get' call

        Parameters
        ----------
        self:
            Method instance
        url : str
            URL to request

        Returns
        -------
        requests.models.Response
            Requests library response classa
        """
    
        #If user set the proxy, you should handle it.
        if self.proxy and self.proxy.get("enabled") and self.proxy.get("server"):
            proxies = {
              "http":"http://{}:{}".format(self.proxy.get("server"),self.proxy.get("port")),
              "https":"http://{}:{}".format(self.proxy.get("server"),self.proxy.get("port"))}
            return requests.get(url,proxies = proxies)
        else:
            return requests.get(url)

    def populate_rates(self, xml):
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
        for root_Cube in root.findall('{http://www.ecb.int/vocabulary/2002-08-01/eurofxref}Cube'):
            for time_Cube in root_Cube.findall('{http://www.ecb.int/vocabulary/2002-08-01/eurofxref}Cube'):
                 rates.update({"date":"{}".format(time_Cube.attrib['time'])})
                 for currency_Cube in time_Cube.findall('{http://www.ecb.int/vocabulary/2002-08-01/eurofxref}Cube'):
                    rates.update({"{}".format(currency_Cube.attrib['currency']):"{}".format(currency_Cube.attrib['rate'])})
        return rates

    def getrates_xml(self):
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
        
        xmlfile = 'eurofxref-daily.xml'
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
            r = self.request(URL)
            with open(xmlfile, 'wb') as file:
                file.write(r.content) 
            return r.status_code        
        else:
            return 200
            
    def currconv(self, rates, sourcecurr, destcurr, amount):
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
            Date from the currency XML file and the converted amount
        """
        
        converted = []
        
        # Change the decimal precision to match the number of digits in the amount
        # so it will display correctly
        # First get integer digits
        places = int(float(amount))
        if places > 0:
            digits = int(math.log10(places))+1
        elif places == 0:
            digits = 1
        else:
            digits = int(math.log10(-places))+2 # +1 if you don't count the '-' 
        # Now get fractional digits
        if "." in amount:
            frac = len(amount.split(".")[1].rstrip("0"))
        else:
            frac = 0
                      
        decimal.getcontext().prec = digits+frac

        destrate = 0.0
        if destcurr.upper() == 'EUR':
            for rate in rates:
                if rate == 'date':
                    converted.append(rates[rate])
                if rate == sourcecurr.upper():
                    converted.append((1 / decimal.Decimal(rates[rate])) * decimal.Decimal(amount))
                    return converted
        else:            
            for rate in rates:
                if rate == 'date':
                    converted.append(rates[rate])
                if rate == destcurr.upper():
                    # If source is EURO then straight convert and return
                    if sourcecurr.upper() == 'EUR':
                        converted.append(decimal.Decimal(rates[rate]) * decimal.Decimal(amount))
                        return converted
                    else:
                        destrate = rates[rate]
                if rate == sourcecurr.upper():
                    sourcerate = rates[rate]
        # Convert via the EURO
        sourceEuro = (1/decimal.Decimal(sourcerate)) * decimal.Decimal(amount)
        converted.append(decimal.Decimal(sourceEuro) * decimal.Decimal(destrate))
        return converted
        
    def query(self, query):
        results = []
        args = query.split(' ')
        currencies = ['AUD' , 'BGN' , 'BRL' , 'CAD' , 'CHF' , 'CNY' , 'CZK' , 'DKK' , 'GBP', 'HKD' , 'HRK' , 'HUF' , 'IDR' , 'ILS' , 'INR' , 'ISK' , 'JPY' , 'KRW', 'MXN','MYR' , 'NOK' , 'NZD' , 'PHP' , 'PLN' , 'RON' , 'RUB' , 'SEK', 'SGD' , 'THB' , 'TRY' , 'USD' , 'ZAR' , 'EUR']
        if len(args) == 3:
            # Check first argument is valid currency code
            if args[1].upper() not in currencies: 
                results.append({
                        "Title": "Error - {} not a valid currency".format(args[1].upper()),
                        "IcoPath":"Images/app.png",
                        "ContextData": "ctxData"
                    })
                return results
            # Check second argument is valid currency code    
            elif len(args[2]) == 3 and args[2].upper() not in currencies:
                results.append({
                    "Title": "Error - {} not a valid currency".format(args[2].upper()),
                    "IcoPath":"Images/app.png",
                    "ContextData": "ctxData"
                })
                return results
            # Do the conversion but only after three char code entered
            elif len(args[2]) == 3:
                # If source and dest currencies the same just return entered amount
                if args[1].upper() == args[2].upper():
                    results.append({
                        "Title": "{} {} = {} {}".format(args[0], args[1].upper(), args[0], args[2].upper()),
                        "IcoPath":"Images/app.png",
                        "ContextData": "ctxData"
                    })
                    return results
                else:
                    try:
                        ratesxml_returncode = self.getrates_xml()
                        ratedict = self.populate_rates('eurofxref-daily.xml')
                        conv = self.currconv(ratedict, args[1], args[2], args[0])
                        results.append({
                            "Title": "{} {} = {} {} (1 {} = {} {})".format(args[0], args[1].upper(), decimal.Decimal(conv[1]), args[2].upper(), args[1].upper(), decimal.Decimal(conv[1])/decimal.Decimal(args[0]),args[2].upper()),
                            "SubTitle": "Rates date : {}".format(conv[0]),
                            "IcoPath":"Images/app.png",
                            "ContextData": "ctxData"
                        })
                    # Show exceptions (for debugging as much as anything else)
                    except Exception as e:
                        results.append({
                            "Title": "Error - {}".format(repr(e)),
                            "IcoPath":"Images/app.png",
                            "ContextData": "ctxData"
                        })
                    return results
        # Always show the usage while there isn't a valid query
        else:
            results.append({
                "Title": "Currency Converter",
                #"SubTitle": "Query: {}".format(query),
                "SubTitle": "<Hotkey> <Amount> <Source currency> <Destination currency>",
                "IcoPath":"Images/app.png",
                "ContextData": "ctxData"
            })
            return results

if __name__ == "__main__":
    Main()