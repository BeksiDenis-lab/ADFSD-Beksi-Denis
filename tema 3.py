meniu = ['papanasi'] * 10 + ['ceafa'] * 3 + ["guias"] * 6
preturi = [["papanasi", 7], ["ceafa", 10], ["guias", 5]]
studenti = ["Liviu", "Ion", "George", "Ana", "Florica"]
comenzi = ["guias", "ceafa", "ceafa", "papanasi", "ceafa"]
tavi = ["tava"] * 7
istoric_comenzi = []


comenzi_numar = {"papanasi": 0, "ceafa": 0, "guias": 0}
total_incasari = 0


for student in studenti:
    if not comenzi:
        break
    comanda = comenzi.pop(0)
    tava = tavi.pop() if tavi else "nu mai sunt tăvi"


    print(f"{student} a comandat {comanda}.")
    istoric_comenzi.append((student, comanda))
    comenzi_numar[comanda] += 1


    pret_comanda = next(pret[1] for pret in preturi if pret[0] == comanda)
    total_incasari += pret_comanda


print("\nRezumat comenzi:")
for produs, numar in comenzi_numar.items():
    print(f"S-au comandat {numar} {produs}.")

print(f"Mai sunt {len(tavi)} tavi disponibile.")
print("Mai este ceafa:", comenzi_numar["ceafa"] < meniu.count("ceafa"))
print("Mai sunt papanasi:", comenzi_numar["papanasi"] < meniu.count("papanasi"))
print("Mai sunt guias:", comenzi_numar["guias"] < meniu.count("guias"))


print(f"\nCantina a încasat: {total_incasari} lei.")

produse_ieftine = [produs for produs in preturi if produs[1] <= 7]
print("Produse care costă cel mult 7 lei:", produse_ieftine)