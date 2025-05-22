import json
import random
import copy
import os

def citeste_date(filename):
    cale_completa = os.path.join(os.path.dirname(__file__), filename)
    with open(cale_completa, "r") as f:
        return json.load(f)

def rest_optim(valoare, bancnote):
    max_val = valoare + 1
    dp = [float('inf')] * max_val
    dp[0] = 0
    traseu = [{} for _ in range(max_val)]

    for suma in range(1, max_val):
        for b in bancnote:
            val = b["valoare"]
            stoc = b["stoc"]
            for k in range(1, stoc + 1):
                if suma >= k * val and dp[suma - k * val] + k < dp[suma]:
                    dp[suma] = dp[suma - k * val] + k
                    traseu[suma] = traseu[suma - k * val].copy()
                    traseu[suma][val] = traseu[suma].get(val, 0) + k

    if dp[valoare] == float('inf'):
        return None
    return traseu[valoare]

def actualizeaza_stoc(stoc, rest):
    for val, nr in rest.items():
        for b in stoc:
            if b["valoare"] == val:
                b["stoc"] -= nr

def simuleaza():
    data = citeste_date("date.json")
    bancnote = data["bancnote"]
    produse = data["produse"]

    while True:
        produs = random.choice(produse)
        pret = produs["pret"]
        plata = random.randint(pret + 1, pret + 20)
        rest_de_dat = plata - pret

        print(f"\nProdus cumpărat: {produs['nume']}")
        print(f"Preț: {pret} lei")
        print(f"Suma plătită: {plata} lei")
        print(f"Rest de dat: {rest_de_dat} lei")

        solutie = rest_optim(rest_de_dat, copy.deepcopy(bancnote))

        if solutie is None:
            print("\n❌ Nu se poate oferi restul! Simularea se oprește.")
            print("Stoc bancnote insuficient pentru rest optim.")
            break

        print("Rest oferit:")
        for val, nr in sorted(solutie.items(), reverse=True):
            print(f"  {nr} x {val} lei")

        actualizeaza_stoc(bancnote, solutie)

if __name__ == "__main__":
    simuleaza()