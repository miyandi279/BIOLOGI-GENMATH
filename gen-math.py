#bin/python
#code by MIYANDI1927
#Team : BCSET-TEKNOLOGI
#YT TEAM : RISKIS7 CHANNEL
#TOOLS :MATHGEN

##################################################
no recode ya bangsat,mandul 7 turunan kalau reode
##################################################

import numpy as np
import random
import matplotlib.pyplot as plt


print(";;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;")
print(";;;;;;code by miyandi1927  ;;;;;;")
print(";;;;;;team BCSET TEKNOLOGI ;;;;;;")
print(";;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;")

def hitung_fitness(x):
    #y = 1000 * (x[0] - 2 * x[1])**2 + (1 - x[0])**2
    y = 1 / (x[0]**2 + x[1]**2 + 0.001)
    y = round(y, 3)
    return y

def dekode_biner_to_desimal(krom):
    idx_awal = 0
    idx_akhir = jum_gen_per_var
    desimal = []
    for i in range(jum_var):
        k = krom[idx_awal:idx_akhir]
        temp1 = 0
        temp2 = 0
        
        for j in range(jum_gen_per_var):
            temp1 = temp1 + (k[j] * 2**(-(j+1)))
            temp2 = temp2 + 2**(-(j+1))
        temp_desimal = bts_bawah + ((bts_atas - bts_bawah)/temp2) * temp1
        
        desimal.append(round(temp_desimal, 3))
        idx_awal = idx_akhir
        idx_akhir = idx_akhir + jum_gen_per_var 
    return desimal

def roulette_wheel(krom, fitness):
    # menskalakan nilai fitness dengan linear fitness ranking
    LFR = linear_fitness_ranking(fitness)

    # membuat proporsi nilai fitness tiap kromosom
    kumulatif_fitness = 0
    acak = random.uniform(0,1)
    idx_induk = 0
    for i in range(uk_pop):
        kumulatif_fitness = kumulatif_fitness + (LFR[i] / sum(LFR))
        if (kumulatif_fitness > acak):
            idx_induk = i
            break 
    
    return idx_induk

def linear_fitness_ranking(fitness):
    sort_fitness = sorted(fitness)
    max_fitness = np.argmax(sort_fitness)
    min_fitness = np.argmin(sort_fitness)
    LFR = []
    for i in range(uk_pop):
        LFR.append(max_fitness - (max_fitness - min_fitness) * (i-1) / (uk_pop-1))
    return LFR

def crossover_1_titik(krom1, krom2):
    # konversi array ke list agar bisa diconcate
    krom1 = list(krom1)
    krom2 = list(krom2)

    # tentukan titik potong
    titik = int(np.fix(np.random.rand() * jum_gen) + 1)
    
    # tukar gen
    anak1 = krom1[0:titik] + krom2[titik:]
    anak2 = krom2[0:titik] + krom1[titik:]
    
    return anak1, anak2

def crossover_n_titik(krom1, krom2, jum_titik_potong=1):
    # konversi array ke list agar bisa diconcate
    krom1 = list(krom1)
    krom2 = list(krom2)

    # tentukan titik potong
    batas = 0
    titik = []
    pembagi = int(np.fix(jum_gen / jum_titik_potong))
    for i in range(jum_titik_potong):
        acak = int(np.fix(np.random.rand() * pembagi+1))
        batas = batas + acak
        titik.append(batas)
    titik.append(jum_gen)
    
    # tukar gen
    anak1 = []
    anak2 = []
    idx = 0
    for i in range(len(titik)):
        # tukar gen ketika i genap (agar pertukaran selang-seling antara ganjil dan genap)
        if (i % 2 == 0):
            anak1 = anak1 + krom2[idx:titik[i]]
            anak2 = anak2 + krom1[idx:titik[i]]
        else:
            anak1 = anak1 + krom1[idx:titik[i]]
            anak2 = anak2 + krom2[idx:titik[i]]
        idx = titik[i]
    
    return anak1, anak2

def crossover_uniform(krom1, krom2):
    pola = np.round(np.random.rand(jum_gen))
    anak1 = krom1
    anak2 = krom2
    
    for i in range(jum_gen):
        if (pola[i] == 1):
            # tukar gen
            anak1[i], anak2[i] = anak2[i], anak1[i]

    return anak1, anak2

def mutasi_biner(krom):
    acak = random.uniform(0,1)
    for j in range(jum_gen):
        if (acak <= pm):
            krom[j] = 1 - krom[j]
    return krom

# Inisialisasi parameter GA
uk_pop = 50
max_generasi = 100
bts_bawah = -5.12
bts_atas = 5.12
jum_var = 2
jum_gen_per_var = 14
jum_gen = jum_var * jum_gen_per_var
pc = 0.8
pm = 0.1
best_kromosom = []
best_fitness = 0
best_genotipe = []
list_best_fitness = []
max_fitness = 1000

# Inisialisasi populasi biner
kromosom = np.round(np.random.rand(uk_pop, jum_gen))

#------------------------------------------------------
# Proses evolusi kromosom
#------------------------------------------------------
generasi = 0
while (generasi < max_generasi and best_fitness < max_fitness):
    # dekode kromosom dan evaluasi fitness
    desimal = []
    fitness = []
    for j in range(uk_pop):
        desimal.append(dekode_biner_to_desimal(kromosom[j]))
        fitness.append(hitung_fitness(desimal[j]))
    
    if (generasi == 0):
        best_fitness = np.max(fitness)
    else:
        if (best_fitness < np.max(fitness)):
            best_fitness = np.max(fitness)

    idx_best_kromosom = np.argmax(fitness)
    best_kromosom = kromosom[idx_best_kromosom]
    best_genotipe = desimal[idx_best_kromosom]
    list_best_fitness.append(best_fitness)

    # tampilkan informasi tiap generasi
    print("Generasi ke-" + str(generasi) + " ==> " + str(best_genotipe) + " = " + str(best_fitness))

    # elitisme
    kromosom_anak = []
    if (uk_pop % 2 == 0):
        kromosom_anak.append(best_kromosom)
        kromosom_anak.append(best_kromosom)
        iterasi_seleksi = 2
    else:
        kromosom_anak.append(best_kromosom)
        iterasi_seleksi = 1

    # seleksi induk/ orang tua
    idx_induk = []
    for iterasi_seleksi in range(uk_pop):
        idx_induk.append(roulette_wheel(kromosom, fitness))
    random.shuffle(idx_induk)
            
    # crossover kromosom
    jum_pasangan_induk = int(len(idx_induk) / 2)
    for i in range(jum_pasangan_induk):
        induk1 = kromosom[idx_induk[i]]
        induk2 = kromosom[idx_induk[i+1]]
        acak = random.uniform(0,1)
        
        if (acak <= pc):
            anak1, anak2 = crossover_1_titik(induk1, induk2)
            #anak1, anak2 = crossover_n_titik(induk1, induk2, jum_titik_potong=3)
            #anak1, anak2 = crossover_uniform(induk1, induk2)
            kromosom_anak.append(anak1)
            kromosom_anak.append(anak2)
        else:
            kromosom_anak.append(induk1)
            kromosom_anak.append(induk2)
        i += 2
    
    # mutasi kromosom
    for i in range(uk_pop):
        kromosom_anak[i] = mutasi_biner(kromosom_anak[i])
    
    # generational replacement
    kromosom = kromosom_anak

    generasi += 1

# tampilkan hasil optimasi
print(str(best_genotipe) + " = " + str(best_fitness) + " (" + str(idx_best_kromosom) + ")")
print("Best Kromosom = " + str(best_kromosom))
plt.title("Grafik Evolusi Algoritma Genetika")
plt.plot(list_best_fitness)
plt.show(block=False)
plt.waitforbuttonpress()
