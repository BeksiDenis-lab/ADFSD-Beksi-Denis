import random
import csv
import time


class HashTable:
    def init(self, size):
        self.size = size
        self.table = [[] for _ in range(size)]
        self.coliziuni = 0
        self.lungime_maxima_lant = 0

    def functie_hash(self, cheie):
        """Funcție de hash personalizată pentru CNP-uri"""
        valoare_hash = 0
        for caracter in cheie:
            # Folosim un multiplicator prim pentru o distribuție mai bună
            valoare_hash = (valoare_hash * 31 + ord(caracter)) % self.size
        return valoare_hash

    def inserare(self, cnp, nume):
        """Inserează o pereche CNP-nume în tabela hash"""
        index = self.functie_hash(cnp)

        # Verificăm dacă este o coliziune
        if len(self.table[index]) > 0:
            self.coliziuni += 1

        # Adăugăm în lanțul de la acest index
        self.table[index].append((cnp, nume))

        # Actualizăm lungimea maximă a lanțului
        lungime_lant = len(self.table[index])
        if lungime_lant > self.lungime_maxima_lant:
            self.lungime_maxima_lant = lungime_lant

    def cautare(self, cnp):
        """Caută un CNP în tabela hash și returnează iterațiile necesare"""
        index = self.functie_hash(cnp)
        iteratii = 1  # Căutarea inițială se numără ca 1

        # Căutăm în lanțul de la acest index
        for i, (cnp_stocat, nume) in enumerate(self.table[index]):
            if i > 0:  # După primul element, iterăm în lanț
                iteratii += 1
            if cnp_stocat == cnp:
                return nume, iteratii

        return None, iteratii

    def statistici(self):
        """Returnează statistici despre tabela hash"""
        slot_uri_ocupate = sum(1 for slot in self.table if slot)
        factor_incarcare = slot_uri_ocupate / self.size
        return {
            'dimensiune': self.size,
            'slot_uri_ocupate': slot_uri_ocupate,
            'factor_incarcare': factor_incarcare,
            'coliziuni': self.coliziuni,
            'lungime_maxima_lant': self.lungime_maxima_lant
        }


def calculeaza_cifra_control(cnp_partial):
    """Calculează cifra de control pentru un CNP"""
    const = "279146358279"
    suma = 0
    for i in range(12):
        suma += int(cnp_partial[i]) * int(const[i])
    cifra_control = suma % 11
    if cifra_control == 10:
        cifra_control = 1
    return str(cifra_control)


def genereaza_cnp_valid():
    """Generează un CNP valid românesc"""
    # Sex și secol: 1-9
    # 1,2: bărbat/femeie născut între 1900-1999
    # 3,4: bărbat/femeie născut între 1800-1899
    # 5,6: bărbat/femeie născut între 2000-2099
    # 7,8: bărbați/femei rezidenți
    # 9: persoane străine
    sex_secol = random.choices([1, 2, 5, 6], weights=[40, 40, 10, 10])[0]

    # Data nașterii
    if sex_secol in [1, 2]:  # 1900-1999
        an = random.randint(1950, 1999)
        an_scurt = str(an % 100).zfill(2)
    else:  # 2000-2099
        an = random.randint(2000, 2023)
        an_scurt = str(an % 100).zfill(2)

    luna = str(random.randint(1, 12)).zfill(2)

    # Determinăm numărul de zile în luna respectivă
    if int(luna) in [4, 6, 9, 11]:
        max_zile = 30
    elif int(luna) == 2:
        if (an % 4 == 0 and an % 100 != 0) or (an % 400 == 0):
            max_zile = 29
        else:
            max_zile = 28
    else:
        max_zile = 31

    zi = str(random.randint(1, max_zile)).zfill(2)

    # Codul județului: 01-52
    # Distribuția reală bazată pe populație
    judete = [f"{i:02d}" for i in range(1, 53)]
    # Ponderi aproximative bazate pe distribuția populației
    ponderi_judete = [
        4.5,  # 01-Alba
        5.7,  # 02-Arad
        3.8,  # 03-Argeș
        3.1,  # 04-Bacău
        2.9,  # 05-Bihor
        4.3,  # 06-Bistrița-Năsăud
        2.2,  # 07-Botoșani
        5.9,  # 08-Brașov
        3.2,  # 09-Brăila
        3.1,  # 10-Buzău
        1.9,  # 11-Caraș-Severin
        3.0,  # 12-Cluj
        8.4,  # 13-Constanța
        2.3,  # 14-Covasna
        3.9,  # 15-Dâmbovița
        3.5,  # 16-Dolj
        3.2,  # 17-Galați
        3.0,  # 18-Gorj
        2.2,  # 19-Harghita
        2.1,  # 20-Hunedoara
        3.3,  # 21-Ialomița
        4.0,  # 22-Iași
        3.1,  # 23-Ilfov
        2.2,  # 24-Maramureș
        2.1,  # 25-Mehedinți
        2.8,  # 26-Mureș
        2.4,  # 27-Neamț
        2.3,  # 28-Olt
        4.0,  # 29-Prahova
        2.1,  # 30-Satu Mare
        2.5,  # 31-Sălaj
        2.6,  # 32-Sibiu
        3.0,  # 33-Suceava
        2.2,  # 34-Teleorman
        3.5,  # 35-Timiș
        2.0,  # 36-Tulcea
        2.1,  # 37-Vaslui
        2.2,  # 38-Vâlcea
        2.0,  # 39-Vrancea
        9.5,  # 40-București
        0.5,  # 41-București S1
        0.5,  # 42-București S2
        0.5,  # 43-București S3
        0.5,  # 44-București S4
        0.5,  # 45-București S5
        0.5,  # 46-București S6
        0.4,  # 47-București S7 (nu mai există)
        0.4,  # 48-București S8 (nu mai există)
        0.1,  # 49-51 (rezervate)
        0.1,
        0.1,
        0.1  # 52 (non-rezident)
    ]

    judet = random.choices(judete[:len(ponderi_judete)], weights=ponderi_judete)[0]

    # Număr de ordine pentru ziua respectivă (3 cifre)
    nr_ordine = str(random.randint(1, 999)).zfill(3)

    # Construim CNP-ul (fără cifra de control)
    cnp_partial = f"{sex_secol}{an_scurt}{luna}{zi}{judet}{nr_ordine}"

    # Calculăm cifra de control
    cifra_control = calculeaza_cifra_control(cnp_partial)

    # CNP-ul complet
    cnp = cnp_partial + cifra_control

    return cnp


def genereaza_nume():
    """Generează un nume aleatoriu românesc"""
    prenume_barbati = ["Alexandru", "Andrei", "Adrian", "Bogdan", "Cătălin", "Ciprian", "Claudiu",
                       "Constantin", "Cristian", "Daniel", "David", "Dorin", "Dragoș", "Dumitru",
                       "Eduard", "Emil", "Eugen", "Florin", "Gabriel", "George", "Gheorghe", "Grigore",
                       "Ion", "Ioan", "Ionuț", "Ilie", "Iulian", "Laurențiu", "Liviu", "Lucian",
                       "Marian", "Marius", "Matei", "Mihai", "Mihail", "Nicolae", "Paul", "Petre",
                       "Petrișor", "Radu", "Răzvan", "Robert", "Sergiu", "Silviu", "Ștefan", "Teodor",
                       "Tudor", "Valentin", "Vasile", "Victor", "Vlad"]

    prenume_femei = ["Adina", "Alexandra", "Alina", "Ana", "Anca", "Andreea", "Angela", "Camelia",
                     "Carmen", "Cătălina", "Claudia", "Cristina", "Daniela", "Diana", "Elena",
                     "Elisabeta", "Florentina", "Gabriela", "Georgiana", "Ileana", "Ioana", "Ionela",
                     "Irina", "Laura", "Loredana", "Lucia", "Luminița", "Magdalena", "Maria", "Marilena",
                     "Marina", "Mihaela", "Mirela", "Monica", "Nicoleta", "Oana", "Paula", "Ramona",
                     "Raluca", "Rodica", "Roxana", "Silvia", "Simona", "Sorina", "Ștefania", "Tamara",
                     "Teodora", "Valentina", "Vasilica", "Veronica", "Victoria"]

    nume_familie = ["Albu", "Ardelean", "Avram", "Badea", "Barbu", "Bejan", "Bratu", "Bucur", "Cojocaru",
                    "Constantin", "Cristea", "Dima", "Dobre", "Dobrescu", "Drăgan", "Dragomir", "Dumitrescu",
                    "Dumitru", "Florescu", "Gheorghe", "Gheorghiu", "Ghiță", "Grigorescu", "Iancu", "Ionescu",
                    "Iordache", "Istrate", "Lazăr", "Luca", "Lungu", "Manea", "Marin", "Marinescu", "Matei",
                    "Mazilu", "Mihai", "Mihăilescu", "Munteanu", "Mureșan", "Nedelcu", "Neagu", "Niculae",
                    "Nistor", "Oprea", "Păun", "Pavel", "Popa", "Popescu", "Preda", "Radu", "Roman", "Roșu",
                    "Rotaru", "Rus", "Rusu", "Sandu", "Simion", "Stan", "Stancu", "Stănescu", "Stoian",
                    "Stroe", "Tănase", "Toma", "Tudor", "Ungureanu", "Vasile", "Vasilescu", "Vintilă", "Voinea"]

    # Determinăm sexul din prima cifră a CNP-ului
    sex = random.choice(["M", "F"])

    if sex == "M":
        prenume = random.choice(prenume_barbati)
    else:
        prenume = random.choice(prenume_femei)

    nume = random.choice(nume_familie)

    return f"{prenume} {nume}"


def genereaza_fisier_csv(numar_inregistrari=1000000, nume_fisier="cnp_data.csv"):
    """Generează un fișier CSV cu CNP-uri și nume asociate"""
    print(f"Generare {numar_inregistrari} CNP-uri și nume...")
    cnp_uri = set()  # Folosim un set pentru a ne asigura că CNP-urile sunt unice

    with open(nume_fisier, 'w', newline='', encoding='utf-8') as fisier:
        writer = csv.writer(fisier)
        writer.writerow(["CNP", "Nume"])

        while len(cnp_uri) < numar_inregistrari:
            cnp = genereaza_cnp_valid()
            if cnp not in cnp_uri:
                cnp_uri.add(cnp)
                nume = genereaza_nume()
                writer.writerow([cnp, nume])

                # Afișăm progresul
                if len(cnp_uri) % 10000 == 0:
                    print(f"Progres: {len(cnp_uri)} CNP-uri generate")

    print(f"Fisierul {nume_fisier} a fost generat cu succes!")
    return nume_fisier


def incarca_date_din_csv(nume_fisier):
    """Încarcă datele din fișierul CSV și returnează lista de perechi CNP-nume"""
    date = []
    with open(nume_fisier, 'r', encoding='utf-8') as fisier:
        reader = csv.reader(fisier)
        next(reader)  # Sărim peste antet
        for rand in reader:
            cnp, nume = rand
            date.append((cnp, nume))
    return date


def populeaza_hash_table(date, dimensiune_tabla=1500000):
    """Populează tabela hash cu datele din fișierul CSV"""
    tabla_hash = HashTable(dimensiune_tabla)

    start_timp = time.time()
    for cnp, nume in date:
        tabla_hash.inserare(cnp, nume)
    sfarsit_timp = time.time()

    timp_total = sfarsit_timp - start_timp
    print(f"Timpul de populare a tabelei hash: {timp_total:.2f} secunde")

    return tabla_hash


def test_cautare(tabla_hash, date, numar_cautari=1000):
    """Realizează teste de căutare pe tabela hash"""
    # Selectăm aleator CNP-uri pentru căutare
    cnp_uri_de_cautat = random.sample([cnp for cnp, _ in date], numar_cautari)

    total_iteratii = 0
    iteratii_maxime = 0
    iteratii_minime = float('inf')
    timp_start = time.time()

    for cnp in cnp_uri_de_cautat:
        _, iteratii = tabla_hash.cautare(cnp)
        total_iteratii += iteratii
        iteratii_maxime = max(iteratii_maxime, iteratii)
        iteratii_minime = min(iteratii_minime, iteratii)

    timp_total = time.time() - timp_start

    # Rezultate statistice
    rezultate = {
        'numar_cautari': numar_cautari,
        'timp_total': timp_total,
        'timp_mediu_per_cautare': timp_total / numar_cautari,
        'medie_iteratii': total_iteratii / numar_cautari,
        'iteratii_maxime': iteratii_maxime,
        'iteratii_minime': iteratii_minime
    }

    return rezultate


def main():
    # Etapa 1: Generarea datelor
    nume_fisier = genereaza_fisier_csv(1000000)  # Generăm 1.000.000 de CNP-uri

    # Etapa 2: Implementarea și popularea tabelei hash
    print("\nÎncărcăm datele din fișierul CSV...")
    date = incarca_date_din_csv(nume_fisier)
    print(f"Au fost încărcate {len(date)} înregistrări.")

    print("\nPopulăm tabela hash...")
    tabla_hash = populeaza_hash_table(date)

    # Afișăm statistici despre tabela hash
    stats = tabla_hash.statistici()
    print("\nStatistici Hash Table:")
    print(f"Dimensiune tabelă: {stats['dimensiune']}")
    print(f"Slot-uri ocupate: {stats['slot_uri_ocupate']}")
    print(f"Factor de încărcare: {stats['factor_incarcare']:.4f}")
    print(f"Număr de coliziuni: {stats['coliziuni']}")
    print(f"Lungimea maximă a unui lanț: {stats['lungime_maxima_lant']}")

    # Etapa 3: Prezentarea rezultatelor statistice
    print("\nRealizăm 1000 de căutări aleatorii...")
    rezultate_cautare = test_cautare(tabla_hash, date, 1000)

    print("\nRezultate căutare:")
    print(f"Număr de căutări: {rezultate_cautare['numar_cautari']}")
    print(f"Timp total căutare: {rezultate_cautare['timp_total']:.4f} secunde")
    print(f"Timp mediu per căutare: {rezultate_cautare['timp_mediu_per_cautare'] * 1000:.4f} milisecunde")
    print(f"Media iterațiilor per căutare: {rezultate_cautare['medie_iteratii']:.2f}")
    print(f"Număr maxim de iterații: {rezultate_cautare['iteratii_maxime']}")
    print(f"Număr minim de iterații: {rezultate_cautare['iteratii_minime']}")


if __name__ == "__main__":
    nume_fisier = genereaza_fisier_csv(1000000)
    date = incarca_date_din_csv(nume_fisier)
    tabla = populeaza_hash_table(date, dimensiune_tabla=1500000)
    rezultate = test_cautare(tabla, date)

    print("\nStatistici Hash Table:")
    print(tabla.statistici())

    print("\nRezultate căutare:")
    for cheie, valoare in rezultate.items():
        print(f"{cheie}: {valoare}")

