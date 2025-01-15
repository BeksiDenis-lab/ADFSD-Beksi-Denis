import string


articol = """
România a obținut o victorie importantă în cadrul campionatului european. Echipa națională a demonstrat o performanță excepțională și a învins una dintre favoritele competiției.
"""


jumatate = len(articol) // 2
partea1 = articol[:jumatate]
partea2 = articol[jumatate:]


partea1 = partea1.upper()
partea1 = partea1.strip()


partea2 = partea2[::-1]
partea2 = partea2.capitalize()
partea2 = ''.join(c for c in partea2 if c not in string.punctuation)


rezultat = partea1 + partea2


print("Rezultatul combinat:")
print(rezultat)