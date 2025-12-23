import re

string = "01.02.2025 - 31.03.1800"
#string = "01.03-5515"


patt = r'(0[1-9]|[12][0-9]|3[01])\.(0[1-9]|1[0,1,2])\.(19|20)\d{2}'
temp = re.findall(pattern=patt, string=string)
if temp:
    print(temp)