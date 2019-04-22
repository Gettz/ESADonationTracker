import requests
import time
from decimal import Decimal


def main():  # Main function, holds all logic for the tracker
    total = Decimal(0.00)  # aggregate donation total pulled from the ESA site.
    currency = Decimal(0.00)  # the donation total but correctly formatted to 2 decimal places.
    output = Decimal(0.00)  # the amount currently saved in the output.txt file, useful for update checks.
    first = True  # Bool to see if first run of script
    h = {"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US;"
         "rv:1.9.2.8) Gecko/20100722 Firefox/3.6.8 GTB7.1 (.NET CLR 3.5.30729)",
         "Referer": "https://donations.esamarathon.com"}
    eventid = input("What is your Event ID (2 digit number): ")
    url = requests.get("https://donations.esamarathon.com/{0}?json".format(eventid), headers=h, timeout=5)
    if url.status_code == 200:
        print("Valid event found. \nNow parsing donation totals to output.txt \n \nPress Ctrl + C to restart script\n")
        try:
            while True:
                r = requests.get("https://donations.esamarathon.com/13?json", headers=h, timeout=5)
                if r.status_code == 200:
                    data = r.json()
                    if(Decimal(data['agg']['amount'])) > total:
                        total = (Decimal(data['agg']['amount']))
                        x = total
                        currency = round(x, 2)
                    if first:
                        print("Current donation total: ${0}".format(str(currency)))
                        first = False
                        output = currency
                    elif currency > output:
                        print("New donation of: $" + str(currency - output))
                        with open('output.txt', 'w') as text_file:
                            text_file.write('${0}'.format(str(currency)))
                            text_file.close()
                            output = currency
                else:
                    print("404, trying again in 5 seconds")
                time.sleep(5)
        except KeyboardInterrupt:
            main()


main()