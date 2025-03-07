def save_matrix(n, fn):
    # Primeste dimensiunea n a unei matrice si numele unui fisier fn
    with open(fn, 'w') as file_output:
        for i in range(n):
            for j in range(n):
                element = input(f"Elementul de pe linia {i} si coloana {j} este: ")
                file_output.write(f"{element} ")
            file_output.write('\n')
           
def load_matrix(fn):
    # Primeste numele unui fisier si returneaza o lista
    matrice = list()
    with open(fn, 'r') as file_input:
        linie = list()
        # Citim elementele separate prin spatiu linie cu linie
        for line in file_input:
            linie = list(map(int, line.split()))
            matrice.append(linie)
    return matrice 

# Salveaza in fisierul matrix.in matricea de dimensiune 3 pe 3, citita de la tastatura
save_matrix(3, "matrix.in")

# Afisam matricea
matricea_din_fisier = load_matrix("matrix.in")
print(matricea_din_fisier)