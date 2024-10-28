# Definirea datelor inițiale
meniu = ['papanasi'] * 10 + ['ceafa'] * 3 + ["guias"] * 6
preturi = [["papanasi", 7], ["ceafa", 10], ["guias", 5]]
studenti = ["Liviu", "Ion", "George", "Ana", "Florica"]  # coada FIFO
comenzi = ["guias", "ceafa", "ceafa", "papanasi", "ceafa"]  # coada FIFO
tavi = ["tava"] * 7  # stiva LIFO
istoric_comenzi = []

# Dictionar pentru a stoca numărul comenzilor per produs
comenzi_numar = {"papanasi": 0, "ceafa": 0, "guias": 0}
total_incasari = 0

# 1. Simularea servirea comenzilor
for student in studenti:
    if not comenzi:
        break  # În caz că nu mai sunt comenzi
    comanda = comenzi.pop(0)  # Preia comanda din coadă
    tava = tavi.pop() if tavi else "nu mai sunt tăvi"  # Scoate tava din stivă

    # Afișarea și actualizarea comenzilor și istoricului
    print(f"{student} a comandat {comanda}.")
    istoric_comenzi.append((student, comanda))
    comenzi_numar[comanda] += 1  # Actualizează numărul de comenzi pentru produs

    # Găsește prețul comenzii și adaugă la total
    pret_comanda = next(pret[1] for pret in preturi if pret[0] == comanda)
    total_incasari += pret_comanda

# 2. Inventar
print("\nRezumat comenzi:")
for produs, numar in comenzi_numar.items():
    print(f"S-au comandat {numar} {produs}.")

print(f"Mai sunt {len(tavi)} tavi disponibile.")
print("Mai este ceafa:", comenzi_numar["ceafa"] < meniu.count("ceafa"))
print("Mai sunt papanasi:", comenzi_numar["papanasi"] < meniu.count("papanasi"))
print("Mai sunt guias:", comenzi_numar["guias"] < meniu.count("guias"))

# 3. Finanțe
print(f"\nCantina a încasat: {total_incasari} lei.")

produse_ieftine = [produs for produs in preturi if produs[1] <= 7]
print("Produse care costă cel mult 7 lei:", produse_ieftine)