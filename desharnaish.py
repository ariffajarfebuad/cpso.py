import random  # akses ke fungsi acak
import dataset as dt  # untuk memasukkan modul/file yang bernama dataset
import math  # menyediakan fungsi matematika seperti perpangkatan
import statistics
import sys
import numpy as np



class Analogy:
    def __init__(self, parameter):
        self.jumlahPartikel = parameter['jumlahPartikel']
        self.c1 = parameter['c1']
        self.c2 = parameter['c2']
        self.wMax = parameter['wMax']
        self.wMin = parameter['wMin']
        self.iterMax = parameter['iterMax']
        # =====================================
        self.perhitunganJarak = parameter['perhitunganJarak']
        self.nilaiP = parameter['nilaiP']
        self.adaptasiAnalogy = parameter['adaptasiAnalogy']
        self.nilaiK = parameter['nilaiK']
        self.indexFitur = parameter['indexFitur']
        self.posisiSize = parameter['posisiSize']
        self.posisiEffortAktual = parameter['posisiEffortAktual']
        self.namaDataset = parameter['namaDataset']
        
 
        

    def dataset(self, namaDataset):
        if namaDataset == 1:
            dataset = self.dataset_maxwell()
        elif namaDataset == 2:
            dataset = self.dataset_desharnais()
        elif namaDataset == 3:
            dataset = self.dataset_silhavy()
        elif namaDataset == 4:
            dataset = self.dataset_silhavy2()
        elif namaDataset == 5:
            dataset = self.dataset_cocomo()
        else:
            print("MAAF DATASET TIDAK TERSEDIA")
            sys.exit()
        return dataset

 

    def dataset_desharnais(self):
        return dt.Desharnais

    def dataset_silhavy(self):
        return dt.Silhavy

    def dataset_silhavy2(self):
        return dt.Silhavy2

    def dataset_cocomo(self):
        return dt.cocomo
    

    def atribut_pilihan(self, namaDataset):
        dataset = self.dataset(namaDataset)
        indexFitur = self.indexFitur
        atributPilihan = []
        for data in dataset:
            atributPilihan.append([data[i] for i in indexFitur])
        return atributPilihan

    def variabel_desain(self, jumlahAtribut):
        variabelDesain = []
        for i in range(jumlahAtribut):
            variabelDesain.append([0, 1])
        return variabelDesain

    def populasi(self):
        dataset = self.atribut_pilihan(self.namaDataset)
        populasi = []
        partikel = []
        variabelDesain = self.variabel_desain(len(dataset[0]))
        ranges = variabelDesain
        for i in range(self.jumlahPartikel):
            for j in range(len(ranges)):
                partikel.append(random.uniform(ranges[j][0], ranges[j][1]))
            populasi.append(partikel)
            partikel = []
        return populasi

    def euclidien(self, dataUji, dataset, populasi):
        similarity = []
        for i in range(len(dataset)):
            temp = []
            for j in range(len(populasi)):
                total = 0
                for k in range(len(populasi[j])):
                    if isinstance(dataUji[k] or dataset[i][k], str):
                        if dataUji[k] == dataset[i][k]:
                            nilai = 0
                        else:
                            nilai = 1
                        total += (populasi[j][k] *
                                  (abs(nilai)**2))
                    else:
                        total += (populasi[j][k] *
                                  (abs(dataUji[k]-dataset[i][k])**2))
                temp.append(math.sqrt(total))
            similarity.append(temp)

        data = self.dataset(self.namaDataset)
        for i in range(len(dataset)):
            dataset[i].append(similarity[i])
            dataset[i].append(data[i][self.posisiSize])
            dataset[i].append(data[i][self.posisiEffortAktual])
        return dataset

    def manhattan(self, dataUji, dataset, populasi):
        similarity = []
        for i in range(len(dataset)):
            temp = []
            for j in range(len(populasi)):
                total = 0
                for k in range(len(populasi[j])):
                    if isinstance(dataUji[k] or dataset[i][k], str):
                        if dataUji[k] == dataset[i][k]:
                            nilai = 0
                        else:
                            nilai = 1
                        total += (populasi[j][k] *
                                  (abs(nilai)))
                    else:
                        total += (populasi[j][k] *
                                  (abs(dataUji[k]-dataset[i][k])))
                temp.append(total)
            similarity.append(temp)

        data = self.dataset(self.namaDataset)
        for i in range(len(dataset)):
            dataset[i].append(similarity[i])

            dataset[i].append(data[i][self.posisiSize])
            dataset[i].append(data[i][self.posisiEffortAktual])
        return dataset

    def minkowski(self, dataUji, dataset, populasi):
        similarity = []
        for i in range(len(dataset)):
            temp = []
            for j in range(len(populasi)):
                total = 0
                for k in range(len(populasi[j])):
                    if isinstance(dataUji[k] or dataset[i][k], str):
                        if dataUji[k] == dataset[i][k]:
                            nilai = 0
                        else:
                            nilai = 1
                        total += (populasi[j][k] *
                                  (abs(nilai)**self.nilaiP))
                    else:
                        total += (populasi[j][k] *
                                  (abs(dataUji[k]-dataset[i][k])**self.nilaiP))
                temp.append(total**(1/self.nilaiP))
            similarity.append(temp)

        data = self.dataset(self.namaDataset)
        for i in range(len(dataset)):
            dataset[i].append(similarity[i])
            dataset[i].append(data[i][self.posisiSize])
            dataset[i].append(data[i][self.posisiEffortAktual])
        return dataset

    def sort_similarity(self, similarity):
        dataset = []
        for i in range(len(similarity[1][-3])):
            dataset.append(sorted(similarity, key=lambda x: x[-3][i]))
        return dataset

    def mean_k(self, dataset):
        # mencari nilai mean effort proyek terdekat
        nilaiK = self.nilaiK
        effortTerdekat = []

        for i in range(1, nilaiK+1):
            effortTerdekat.append(dataset[i][-1])

        effortTerdekat = statistics.mean(effortTerdekat)

        # mencari nilai mean size proyek terdekat
        sizeTerdekat = []

        for i in range(1, nilaiK+1):

            sizeTerdekat.append(dataset[i][-2])
        sizeTerdekat = statistics.mean(sizeTerdekat)

        # mencari estimasi effort proyek baru

        estimasiEffort = effortTerdekat/sizeTerdekat * \
            dataset[0][-2]
        # print(estimasiEffort, "=", effortTerdekat,
        #       "/", sizeTerdekat, "x", dataset[0][-2])

        return estimasiEffort

    def median_k(self, dataset):
        nilaiK = self.nilaiK
        effortTerdekat = []
        for i in range(1, nilaiK+1):
            effortTerdekat.append(dataset[i][-1])

        sizeTerdekat = []
        for i in range(1, nilaiK+1):

            sizeTerdekat.append(dataset[i][-2])

        effortTerdekat = statistics.median(effortTerdekat)
        sizeTerdekat = statistics.median(sizeTerdekat)

        estimasiEffort = effortTerdekat/sizeTerdekat * \
            dataset[0][-2]

        # print(estimasiEffort, "=", effortTerdekat,
        #       "/", sizeTerdekat, "x", dataset[0][-2])

        return estimasiEffort

    def irwa_k(self, dataset):
        nilaiK = self.nilaiK
        effortTerdekat = []
        for i in range(1, nilaiK+1):
            effortTerdekat.append(dataset[i][-1])

        sizeTerdekat = []
        for i in range(1, nilaiK+1):
            sizeTerdekat.append(dataset[i][-2])
        if nilaiK == 2:
            CA = (effortTerdekat[0]/sizeTerdekat[0] *
                  dataset[0][-2])
            # print("CA:", CA)
            SC = (effortTerdekat[1]/sizeTerdekat[1] *
                  dataset[0][-2])
            # print("SC:", SC)
            estimasiEffort = ((2*CA)+(SC))/10
            # print("Estimasi: ", estimasiEffort)

        elif nilaiK == 3:
            CA = (effortTerdekat[0]/sizeTerdekat[0] *
                  dataset[0][-2])
            # print("CA:", CA)
            SC = (effortTerdekat[1]/sizeTerdekat[1] *
                  dataset[0][-2])
            # print("SC: ", SC)
            TC = (effortTerdekat[2]/sizeTerdekat[2] *
                  dataset[0][-2])
            # print("TC: ", TC)
            estimasiEffort = ((3*CA)+(2*SC)+TC)/10
            # print("Estimasi: ", estimasiEffort)

        elif nilaiK == 4:
            CA = (effortTerdekat[0]/sizeTerdekat[0] *
                  dataset[0][-2])
            # print("CA:", CA)
            SC = (effortTerdekat[1]/sizeTerdekat[1] *
                  dataset[0][-2])
            # print("SC: ", SC)
            TC = (effortTerdekat[2]/sizeTerdekat[2] *
                  dataset[0][-2])
            # print("TC: ", TC)
            LA = (effortTerdekat[3]/sizeTerdekat[3] *
                  dataset[0][-2])
            # print("LA: ", LA)
            estimasiEffort = ((4*CA)+(3*SC)+(2*TC)+(LA))/10
            # print("Estimasi: ", estimasiEffort)

        elif nilaiK == 5:
            CA = (effortTerdekat[0]/sizeTerdekat[0] *
                  dataset[0][-2])
            # print("CA:", CA)
            SC = (effortTerdekat[1]/sizeTerdekat[1] *
                  dataset[0][-2])
            # print("SC: ", SC)
            TC = (effortTerdekat[2]/sizeTerdekat[2] *
                  dataset[0][-2])
            # print("TC: ", TC)
            FA = (effortTerdekat[3]/sizeTerdekat[3] *
                  dataset[0][-2])
            # print("FA:",FA)
            LA = (effortTerdekat[4]/sizeTerdekat[4] *
                  dataset[0][-2])
            # print("LA: ", LA)
            estimasiEffort = ((5*CA)+(4*SC)+(3*TC)+(2*FA)+(LA))/10
            # print("Estimasi: ", estimasiEffort)
        else:
            print("NILAI K TIDAK BISA DIPROSES")
            sys.exit()
        return estimasiEffort

    def estimasi_effort(self, dataset):
        estimasiEffort = []
        for i in range(len(dataset)):
            if self.adaptasiAnalogy == 1:
                estimasiEffort.append(self.mean_k(dataset[i]))
            elif self.adaptasiAnalogy == 2:
                estimasiEffort.append(self.median_k(dataset[i]))
            elif self.adaptasiAnalogy == 3:
                estimasiEffort.append(self.irwa_k(dataset[i]))
        return estimasiEffort


    def hitung_ae(self, dataUji, estimasi):
        ae = []
        for i in range(len(estimasi)):
            ae.append(abs(estimasi[i] - dataUji[-1]))
            # print(abs(estimasi[i] - dataUji[-1]),
            #       "=", estimasi[i], "-", dataUji[-1])
        return ae
    def hitung_w(self, iteration):
        W = self.wMax-((self.wMax-self.wMin)/self.iterMax)*iteration
        return W

    def update_velocity(self, iteration, pBest, gBest, populasi, velocity, cosine_value):
        w = self.hitung_w(iteration)
        r1 = self.a_constant(iteration, cosine_value)
        r2 = self.populasi()
        c1 = self.c1
        c2 = self.c2
        newVelocity = []
        for i in range(len(populasi)):
            temp = []
            for j in range(len(gBest)):
                hasil = w * velocity[i][j]+c1*r1* \
                    (pBest[i][j]-populasi[i][j])+c2 * \
                    r2[i][j]*(gBest[j]-populasi[i][j])
                temp.append(hasil)
                # print("velocity =", w,
                #       "x ", velocity[i][j], " + ", c1, " x", r1[i][j], "x (", Pbest[i][j], " -", populasi[i][j], ") + ", c2, " x ", r2[i][j], "x(", Gbest[j], "-", populasi[i][j], ")")
            newVelocity.append(temp)
        return newVelocity
    
    def update_posisi(self, populasi, velocity):
        newPosisi = []
        for i in range(len(populasi)):
            temp = []
            for j in range(len(populasi[i])):
                hasil = populasi[i][j]+velocity[i][j]
                if hasil < 0:
                    temp.append(0)
                elif hasil > 1:
                    temp.append(1)
                else:
                    temp.append(hasil)
            newPosisi.append(temp)
        return newPosisi

    def pbest(self, oldPBest, oldPBestEstimasi, oldPBestAe, newPopulasi, newEstimasi, newAe):
        pBest = []
        pBestEstimasi = []
        pBestAe = []
        for i in range(len(oldPBestAe)):
            if (newAe[i] <= oldPBestAe[i]):
                pBest.append(newPopulasi[i])
                pBestEstimasi.append(newEstimasi[i])
                pBestAe.append(newAe[i])

            else:
                pBest.append(oldPBest[i])
                pBestEstimasi.append(oldPBestEstimasi[i])
                pBestAe.append(oldPBestAe[i])
        return pBest, pBestEstimasi, pBestAe

    def ae_mbre(self, dataUji, estimasi):
        ae = abs(estimasi-dataUji[-1])/min(estimasi, dataUji[-1])
        # print(ae, "=|", estimasi, "-",
        #       dataUji[-1], "|/", min(estimasi, dataUji[-1]))
        return ae

    def ae_mibre(self, dataUji, estimasi):
        ae = abs(estimasi-dataUji[-1])/max(estimasi, dataUji[-1])
        # print(ae, "=|", estimasi, "-",
        #       dataUji[-1], "|/", min(estimasi, dataUji[-1]))
        return ae

    def hitung_ae_aktual(self, namaDataset):
        dataset = self.dataset(namaDataset)
        aktual = []
        for i in range(len((dataset))):
            aktual.append(dataset[i][self.posisiEffortAktual])
        meanAktual = statistics.mean(aktual)
        hasil = []
        for i in range(len((dataset))):
            hasil.append(abs(dataset[i][self.posisiEffortAktual]-meanAktual))
        return hasil

    def sa(self, mae, mae0):
        sa = 1 - (mae/mae0)
        return sa

    def hitung_es(self, mae, mae0, namaDataset):
        dataset = self.dataset(namaDataset)
        aktual = []
        for i in range(len((dataset))):
            aktual.append(dataset[i][self.posisiEffortAktual])
        s0 = statistics.stdev(aktual)
        es = abs((mae-mae0)/s0)
        return es
    
    # def cosine(self, t_max):
    #     iteration = self.iterMax
    #     for i in range(iteration):
    #         if i==0:
    #             I = 0
    #             return math.cos((self.I * math.pi) / t_max);
    def cosine(self, iterMax, I):
         # Initialize I  to 0
        return math.cos((I * math.pi) / iterMax)
    
    def a_constant(self, iterMax, cosine_value):
         # Initialize I to 0
        # cosine_value = self.cosine(iterMax, I)
        if cosine_value <= iterMax / 6:
            return 4 / 3
        if (iterMax / 6) < cosine_value <= (5 * iterMax / 6):
            return 16 / 3
        if (5 * iterMax / 6) < cosine_value <= iterMax:
            return 2 / 9
        
    
    def main_analogy(self):
        estimasiEffort = []
        nilaiAe0 = []
        nilaiAe = []
        nilaiAeMbre = [] 
        nilaiAeMibre = [] 
        dataset = self.atribut_pilihan(self.namaDataset)
        # print("Dataset yang terdiri dari", len(dataset),  "proyek: ")
        # print(dataset)

        for x in range(len(dataset)):
            # print("\nData Uji ", x+1)
            populasi = self.populasi()
           
            
            # print("\nInisialiasai Swarm:"), print(populasi)
            velocity = np.zeros((self.jumlahPartikel, len(populasi[0])))
            # print("\nKecepatan Awal:"), print(velocity)
            dataUji = dataset[x]
            # print("Data Uji:"), print(dataUji)
            if self.perhitunganJarak == 1:
                similarity = self.euclidien(dataUji, dataset, populasi)
            elif self.perhitunganJarak == 2:
                similarity = self.manhattan(dataUji, dataset, populasi)
            elif self.perhitunganJarak == 3:
                similarity = self.minkowski(dataUji, dataset, populasi)
            # print("\nSimilarity:"), print(similarity)

            sortPso = self.sort_similarity(similarity)
            # print("\nsort Similarity:"), print(sortPso)

            estimasi = self.estimasi_effort(sortPso)
            # print("\nEstimasi effort:"), print(estimasi)

            ae = self.hitung_ae(dataUji, estimasi)
            # print("\nAE effort-aktual:"), print(ae)

            aeTerkecil = min(ae)
            index_partikel = ae.index(aeTerkecil)
            gBest = populasi[index_partikel]
            # print("\nGlobal Best Partikel ke",
            #       index_partikel+1, "Yaitu :"), print(gBest)
            pBest = populasi
            pBestEstimasi = estimasi
            pBestAe = ae

        iteration = self.iterMax
        # print(iteration)
        # xyz = self.iterMax
        # abd = self.a_constant(xyz)
        for i in range(iteration):
            if i==0:
                I = 0
                cosine_value = self.cosine(self.iterMax,I)
            else:
                # panggil fungsi aConstant
                cosine_value = self.cosine(self.iterMax, I) 
                I = self.a_constant(self.iterMax, cosine_value)   
        # print("\nIterasi ke ", i+1)
                velocity = self.update_velocity(
                i, pBest, gBest, populasi, velocity, cosine_value)
        # print("\nVelocity :"), print(velocity)
        newPopulasi = self.update_posisi(populasi, velocity)
        # print("\nPosisi Baru:"), print(newPopulasi)
        dataset = self.atribut_pilihan(self.namaDataset)
        dataUji = dataset[x]
        if self.perhitunganJarak == 1:
            similarity = self.euclidien(dataUji, dataset, populasi)
        elif self.perhitunganJarak == 2:
            similarity = self.manhattan(dataUji, dataset, populasi)
        elif self.perhitunganJarak == 3:
            similarity = self.minkowski(dataUji, dataset, populasi)
        sortPso = self.sort_similarity(similarity)
        newEstimasi = self.estimasi_effort(sortPso)
        print("\nEstimasi Effort:"), print(newEstimasi)
        newAe = self.hitung_ae(dataUji, newEstimasi)
        # print("\nAE effort-aktual : "), print(newAe)
        pBest, pBestEstimasi, pBestAe = self.pbest(pBest, pBestEstimasi, pBestAe,
                                                    newPopulasi, newEstimasi, newAe)
        # print("\nPersonal Best : "), print(pBest)
        aeTerkecil = min(pBestAe)
        index_partikel = pBestAe.index(aeTerkecil)
        gBest = pBest[index_partikel]
        # print("\nGlobal Best Partikel ke",
        #       index_partikel+1, "Yaitu :"), print(gBest)
        # print("\nEstimasi :"), print(pBestEstimasi[index_partikel])
        # print("\nAE:"), print(pBestAe[index_partikel])
        populasi = newPopulasi
        # print("==================================================")
    # print(sortPso)
        estimasiEffort.append(pBestEstimasi[index_partikel])
        # print("Estimasi:", pBestEstimasi[index_partikel])
        nilaiAe.append(pBestAe[index_partikel])
        # print("AE:", pBestAe[index_partikel])
        aeMbre = self.ae_mbre(dataUji, pBestEstimasi[index_partikel])
        nilaiAeMbre.append(aeMbre)
        aeMibre = self.ae_mibre(dataUji, pBestEstimasi[index_partikel])
        nilaiAeMibre.append(aeMibre)
        NilaiAeAktual = self.hitung_ae_aktual(self.namaDataset)
        mae0 = statistics.mean(NilaiAeAktual)
         # print("\nNilai MAE Awal adalah:"), print(mae0)
        mae = statistics.mean(nilaiAe)
        # print("\nNilai MAE ADALAH:"), print(mae)
        mbre = statistics.mean(nilaiAeMbre)
        # print("\nNilai MBRE ADALAH:"), print(mbre)
        sa = self.sa(mae, mae0)
        # print("\nNilai SA ADALAH:"), print(sa)
        mibre = statistics.mean(nilaiAeMibre)
        # print("\nNilai MIBre ADALAH:"), print(mibre)
        es = self.hitung_es(mae, mae0, self.namaDataset)
        # print("\nNilai ES ADALAH:"), print(es)
        return {'mae': mae, 'mbre': mbre, 'sa': sa, 'mibre': mibre, 'es': es}


kodeJarak = [1, 2, 3]
namaJarak = ["Euclidien", "Manhattan", "minkowski"]
jumlahPartikel = [5, 10, 15, 20, 25, 30]


# --------Desharnaish
tabelCocomo = []
print("Sedang Hitung Cocomo...")
for j in range(len(jumlahPartikel)):
    temp = []
    temp.append(jumlahPartikel[j])
    for i in range(len(kodeJarak)):
        print("Partikel: ", jumlahPartikel[j],
              "--> Adaptasi Analogy: ", namaJarak[i])
        temp2 = []
        parameter = {
            # ================================================ Keperluan PSO
            "jumlahPartikel": jumlahPartikel[j],
            "c1": 2,
            "c2": 2,
            "wMax": 0.9,
            "wMin": 0.4,
            "iterMax": 30,
            # ================================================ Keperluan Estimasi
            # [1]Euclidien, [2]Manhattan, [3]Minkowski
            "perhitunganJarak": kodeJarak[i],
            "nilaiP": 3,
            # [1]mean, [2]median, [3]IRWA ------------------ubah manual
            "adaptasiAnalogy": 1, 
            # 1,2,3,4 ------------------ubah manual
            "nilaiK":1,
            # Maxwell(23,24,26), Desharnais(1,2,4,6,7,8,9,10,11), Silhavy(10, 11, 14, 15),Silhavy(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 17)
            "indexFitur": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
            # Maxwell(24,26) ,Desharnais(8,5) ,Silhavy(11,12)
            "posisiSize": 16,
            "posisiEffortAktual": 17,
            # [1]Maxwell, [2]Desharnais, [3]Silhavy, [4]Silhavy2,[5]cocomo
            "namaDataset": 5
    }
        desharnaish = Analogy(parameter)
        hasil = desharnaish.main_analogy()
        temp2.append(hasil['mae'])
        temp2.append(hasil['mbre'])
        temp2.append(hasil['sa'])
        temp2.append(hasil['mibre'])
        temp2.append(hasil['es'])
        temp.append(temp2)
    # print("Jumlah partikel :", jumlahPartikel[j])
    # print(temp)
tabelDesharnaish.append(temp)
print("tabelDesharnaish:"), print(tabelDesharnaish)

print("Hitung Desharnaish Selesai")

print("======= Desharnaish ======")
for i in range(len(tabelDesharnaish)):
    for j in range(len(tabelDesharnaish[i])):
        if j == 0:
            print("Jumlah Partikel-:", tabelDesharnaish[i][j])
        elif j == 1:
            print("Euclidien-------:", tabelDeshanaish[i][j])
        elif j == 2:
            print("Manhattan-------:", tabelCocomo[i][j])
        elif j == 3:
            print("Minkowski-------:", tabelCocomo[i][j])
print()       
