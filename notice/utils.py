
from ast import pattern
import re


class Utils():
    @staticmethod
    def nepaliNumberToEnglish(nepaliNumber):
        """
        Converts Nepali number to English number.
        """

        rep = {'०': '0', '१': '1', '२': '2', '३': '3', '४': '4',
               '५': '5', '६': '6', '७': '7', '८': '8', '९': '9'}
        english = ''
        rep = dict((re.escape(k), v) for k, v in rep.items())
        pattern = re.compile("|".join(rep.keys()))
        text = pattern.sub(lambda m: rep[re.escape(m.group(0))], nepaliNumber)

        return text
