from nptdms import TdmsFile
import numpy as np
import pandas as pd
import csv
import os
import sys
import matplotlib.pyplot as plt
import ipywidgets as widgets
from pathlib import Path
import re

class Vergleich:
    def __init__(self,folder):
        self.folder = folder


    def Vergleich_Kraft(self):
        Ordner=os.listdir(self.folder)
        k=1
        t=300
        w=t
        y=[]
        datap=pd.DataFrame()
        for i in Ordner:
            if not os.path.isdir(self.folder +"\\" +i +"\\Vergleich"):
                os.mkdir(self.folder + "\\"+i +"\\Vergleich")
            Vergleich_Ordner=self.folder +"\\" +i +"\\Vergleich\\"
            if "PKL" in i:
                path=self.folder+"\\"+i+"\\Cuts\\Forces\\"
                name=os.listdir(path)
                for j in name:
                    if j.endswith(str(t)+".pkl"):
                        print(j)
                        data=pd.read_pickle(path+j)
                        datap["Fz_"+str(t)]=data["/'Unbenannt'/'Fz'"]
                        t=t + w
                    elif(j.endswith("001.pkl") and k==1):
                        print(j)
                        data = pd.read_pickle(path + j)
                        datap["Fz_" + str(k)] = data["/'Unbenannt'/'Fz'"]
                # datap.plot()
                # plt.ylim(-500,50)
                k = 1
                t = w
                # plt.savefig(Vergleich_Ordner + "\\" + i + "_Vergleich_Fx.png")
                pathe = Vergleich_Ordner + "\\" + i + "_Vergleich_"
                self.Vergleich_Plot_Werkzeug(datap, pathe)
                datap = pd.DataFrame()
        for i in Ordner:
            if not os.path.isdir(self.folder + "\\" + i + "\\Vergleich"):
                os.mkdir(self.folder + "\\" + i + "\\Vergleich")
            Vergleich_Ordner = self.folder + "\\" + i + "\\Vergleich\\"
            if "PKL" in i:
                path = self.folder + "\\" + i + "\\Cuts\\Forces\\"
                name = os.listdir(path)
                for j in name:
                    if j.endswith(str(t) + ".pkl"):
                        print(j)
                        data = pd.read_pickle(path + j)
                        datap["Fy_" + str(t)] = data["/'Unbenannt'/'Fy'"]
                        t = t + w
                    elif (j.endswith("001.pkl") and k == 1):
                        print(j)
                        data = pd.read_pickle(path + j)
                        datap["Fy_" + str(k)] = data["/'Unbenannt'/'Fy'"]
                # datap.plot()
                # plt.ylim(-500,50)
                k = 1
                t = w
                # plt.savefig(Vergleich_Ordner + "\\" + i + "_Vergleich_Fx.png")
                pathe = Vergleich_Ordner + "\\" + i + "_Vergleich_"
                self.Vergleich_Plot_Werkzeug(datap, pathe)
                datap = pd.DataFrame()
                plt.close()
        for i in Ordner:
            if not os.path.isdir(self.folder + "\\" + i + "\\Vergleich"):
                os.mkdir(self.folder + "\\" + i + "\\Vergleich")
            Vergleich_Ordner = self.folder + "\\" + i + "\\Vergleich\\"
            if "PKL" in i:
                path = self.folder + "\\" + i + "\\Cuts\\Forces\\"
                name = os.listdir(path)
                for j in name:
                    if j.endswith(str(t) + ".pkl"):
                        print(j)
                        data = pd.read_pickle(path + j)
                        datap["Fx_" + str(t)] = data["/'Unbenannt'/'Fx'"]
                        t = t + w
                    elif (j.endswith("001.pkl") and k == 1):
                        print(j)
                        data = pd.read_pickle(path + j)
                        datap["Fx_" + str(k)] = data["/'Unbenannt'/'Fx'"]
                # datap.plot()
                # plt.ylim(-500,50)
                k = 1
                t = w
                # plt.savefig(Vergleich_Ordner + "\\" + i + "_Vergleich_Fx.png")
                pathe=Vergleich_Ordner + "\\" + i + "_Vergleich_"
                self.Vergleich_Plot_Werkzeug(datap,pathe)
                datap = pd.DataFrame()
                # plt.close()

    def Vergleich_Hioki(self):
        Ordner = os.listdir(self.folder)
        k = 1
        t = 300
        w = t
        y = []
        datap = pd.DataFrame()
        df=pd.read_pickle("C:\\Users\\mauri\\Desktop\\Projektarbeit\\Rohdaten\\Prozessdaten\\V02_PKLData\\Cuts\\I_LM\\V02_Inco718_RexT15_h020_y4°_a4°_vc6_001.pkl")
        col=df.columns
        for i in Ordner:
            if not os.path.isdir(self.folder + "\\" + i + "\\Vergleich"):
                os.mkdir(self.folder + "\\" + i + "\\Vergleich")
            Vergleich_Ordner = self.folder + "\\" + i + "\\Vergleich\\"
            if "PKL" in i:
                path = self.folder + "\\" + i + "\\Cuts\\I_LM\\"
                name = os.listdir(path)
                for c in col:
                    for j in name:
                        if j.endswith(str(t) + ".pkl"):
                            print(j)
                            data = pd.read_pickle(path + j)
                            datap[c + str(t)] = data[c]
                            t = t + w
                        elif (j.endswith("001.pkl") and k == 1):
                            print(j)
                            data = pd.read_pickle(path + j)
                            datap[c + str(k)] = data[c]

                    datap.plot()
                    k = 1
                    t = w
                    plt.savefig(Vergleich_Ordner + "\\" + i + "_Vergleich_"+c.replace("/","")+".png")
                    datap = pd.DataFrame()
                    plt.close()

    def Vergleich_Strom(self):
        Ordner = os.listdir(self.folder)
        k = 1
        t = 300
        w = t
        y = []
        datap = pd.DataFrame()
        df = pd.read_pickle(
            "C:\\Users\\mauri\\Desktop\\Projektarbeit\\Rohdaten\\Prozessdaten\\V02_PKLData\\Cuts\\I_LM\\V02_Inco718_RexT15_h020_y4°_a4°_vc6_001.pkl")
        col = df.columns
        for i in Ordner:
            if not os.path.isdir(self.folder + "\\" + i + "\\Vergleich"):
                os.mkdir(self.folder + "\\" + i + "\\Vergleich")
            Vergleich_Ordner = self.folder + "\\" + i + "\\Vergleich\\"
            if "PKL" in i:
                path = self.folder + "\\" + i + "\\Cuts\\I_LM\\"
                name = os.listdir(path)
                for j in name:
                    print(j)
                    if j.endswith(str(t) + ".pkl"):
                        print(j)
                        data = pd.read_pickle(path + j)
                        datap["/'Unbenannt'/'I1-LM'" + str(t)] = data["/'Unbenannt'/'I1-LM'"]
                        datap["/'Unbenannt'/'I2-LM'" + str(t)] = data["/'Unbenannt'/'I2-LM'"]
                        t = t + w
                    elif (j.endswith("001.pkl") and k == 1):
                        print(j)
                        data = pd.read_pickle(path + j)
                        datap["/'Unbenannt'/'I1-LM'" + str(k)] = data["/'Unbenannt'/'I1-LM'"]
                        datap["/'Unbenannt'/'I2-LM'" + str(k)] = data["/'Unbenannt'/'I2-LM'"]

                datap.plot()
                k = 1
                t = w
                plt.savefig(Vergleich_Ordner + "\\" + i + "_Vergleich_" + "Motorstrom" + ".png")
                datap = pd.DataFrame()
                plt.close()

    def Vergleich_Interns(self):
        Ordner = os.listdir(self.folder)
        k = 1
        t = 300
        w = t
        y = []
        datap = pd.DataFrame()
        df=pd.read_pickle("C:\\Users\\mauri\\Desktop\\Projektarbeit\\Rohdaten\\Prozessdaten\\V02_PKLData\\Cuts\\Maschinendaten\\V02_Inco718_RexT15_h020_y4°_a4°_vc6_001.pkl.pkl")
        col=df.columns
        for i in Ordner:
            if not os.path.isdir(self.folder + "\\" + i + "\\Vergleich"):
                os.mkdir(self.folder + "\\" + i + "\\Vergleich")
            Vergleich_Ordner = self.folder + "\\" + i + "\\Vergleich\\"
            if "V07_PKL" in i:
                path = self.folder + "\\" + i + "\\Cuts\\Maschinendaten\\"
                name = os.listdir(path)
                for c in col:
                    for j in name:
                        if j.endswith(str(t) + ".pkl.pkl"):
                            print(j)
                            data = pd.read_pickle(path + j)

                            print(data)
                            datap[c + str(t)] = data[c]
                            t = t + w
                        elif (j.endswith("001.pkl.pkl") and k == 1):
                            print(j)
                            data = pd.read_pickle(path + j)

                            datap[c + str(k)] = data[c]
                    if not datap.empty:
                        # datap.plot()
                        pathe=Vergleich_Ordner + "\\" + i + "interns_Vergleich_"
                        self.Vergleich_Plot_Werkzeug(datap,pathe)
                        k = 1
                        t = w
                        #plt.savefig(Vergleich_Ordner + "\\" + i + "_Vergleich_"+c.replace("/","")+".png")
                        datap = pd.DataFrame()
                        plt.close()

    def Vergleich_Kraft_Peaks(self):
        Ordner = os.listdir(self.folder)
        Vergleich="C:\\Users\\mauri\\Desktop\\Projektarbeit\\Rohdaten\\Prozessdaten\\V01_PKLData\\Vergleich\\"
        k = 1
        t = 300
        w = t
        y = []
        datap = pd.Series()
        Anzahl_peaks = 11
        datap = pd.DataFrame()
        for d in ["/'Unbenannt'/'Fx'","/'Unbenannt'/'Fy'","/'Unbenannt'/'Fz'"]:
            for i in Ordner:
                Vergleich = f"C:\\Users\\mauri\\Desktop\\Projektarbeit\\Rohdaten\\Prozessdaten\\{i}\\Vergleich\\"
                if not os.path.isdir(self.folder + "\\" + i + "\\Vergleich"):
                    os.mkdir(self.folder + "\\" + i + "\\Vergleich")
                Vergleich_Ordner = self.folder + "\\" + i + "\\Vergleich\\"
                if "PKL" in i:
                    path = self.folder + "\\" + i + "\\Cuts\\Forces\\peaks_only\\"
                    #gibt die Zahl des Auszugebenden Peaks an
                    for e in range(1,Anzahl_peaks):
                        print(e)
                        #geht alle namen im Ordner peaks only durch und wählt jeweils name+001 bzw. name+300 |600 etc. aus
                        datap = pd.DataFrame()
                        for peak_name in os.listdir(path):
                            if "_Inco718_" in peak_name and (peak_name.endswith(f"001") or peak_name.endswith(f"{t}")):
                                path_data=path +"\\"+ peak_name
                                name = os.listdir(path_data)
                                #geht in den Ordner _V01_Inco718_RexT15_h020_y4°_a2°_vc3_001 rein und öffnet von diesem Peak e
                                for j in name:
                                    if j.endswith(f"_{e}.pkl"):
                                        print(j)
                                        if peak_name.endswith(f"{t}"):
                                            t = t + 300
                                            path_data=path_data + "\\"+ j
                                            data = pd.read_pickle(path_data)
                                            datap[d+"_"+str(t)]=data[d]
                                            # datap[d+"_"+str(t)].plot()
                                            # datap=pd.Series()
                                        else:
                                            path_data = path_data + "\\" + j
                                            data = pd.read_pickle(path_data)
                                            datap[d+"_"+str(t)] = data[d]
                                            # datap[d+"_"+str(t)].plot()
                                            # datap = pd.Series()
                        t = 300
                        # if e == 1:
                        #     plt.ylim(0,1000)
                        # if e == 2:
                        #     plt.ylim(300,2000)
                        # if e == 3:
                        #     plt.ylim(500,3000)
                        # if e>3:
                        #     plt.ylim(500,4500)
                        pathe=Vergleich + i + str(e)
                        self.Vergleich_Plot_Werkzeug(datap,pathe)

                        print(datap)
                        # plt.legend()
                        # plt.savefig(Vergleich + i + d.replace("/","") + f"Peak_{e}.png")
                        # plt.close()

    def Vergleich_Plot_Werkzeug(self,data,path):
        if data.shape[1] > 1:
            col = data.columns
        else:
            col = data
        # col = "/'Unbenannt'/'Fz'"
        # set elinewidth to 1 for error bars, order by Werkstoff, Drehzahl, Vorschub

        fig_Ra = plt.figure(figsize=(6.4, 2))
        ax_Ra = fig_Ra.add_subplot(111)
        farben=[[0 / 255, 84 / 255, 159 / 255],[246/255,168/255,0/255],[87/255,171/255,39/255],[204/255,7/255,30/255]]
        # farben = [0 / 255, 84 / 255, 159 / 255]
        for i,c in zip(col,farben):
            ax_Ra.plot(np.arange(len(data[i])), data[i],
                        # yerr=data["Ra_std"],
                        color=c, linestyle="-"
                        #  ,width=0.7,edgecolor="white",hatch=9 * ["", "//////"],
                        # color=2 * ["#404040"] + 2 * ["#7F7F7F"] + 2 * ["#D9D9D9"] + 2 * [
                        #     "#00549F"] + 2 * ["#8EBAE5"] + 2 * ["#E8F1FA"] + 2 * [
                        #           "#F6A800"] + 2 * ["#FFCD61"] + 2 * ["#FFEECA"], capsize=2,
                        # error_kw={"elinewidth": 1, "capthick": 1
                        )
        ax_Ra.tick_params(axis='both', which='both', direction="out", length=4, width=1,
                                  colors='black', labelsize=14)
        # remove ticks and labels for x-axis
        ax_Ra.tick_params(axis='x', which='both', bottom=False, top=False,
                                  labelbottom=True)
        # ax_Ra.set_xticks(np.arange(len(data[i]) / 50) * 50)
        ax_Ra.grid(axis='x', color='#D9D9D9', linestyle='-', linewidth=1)
        ax_Ra.grid(axis='y', color='#D9D9D9', linestyle='-', linewidth=1)
        ax_Ra.set_axisbelow(True)
        fig_Ra.tight_layout()
        # remove the top and right spines
        ax_Ra.spines['top'].set_visible(False)
        ax_Ra.spines['right'].set_visible(False)
        ax_Ra.spines['bottom'].set_visible(True)
        # if not abs(data[i].max()) < abs(data[i].min()):
        #     ax_Ra.set_ylim(0, data[i].max())
        # else:
        #     ax_Ra.set_ylim(data[i].min(), 0)
        # save figures
        # fig_Ra.savefig(f"{path}.png'", dpi=300)#
        # if not os.path.isdir(path + "\\" + "plot"):
        #     os.mkdir(path + "\\" + "plot")
        if "Unbenannt" in i:
            print(i)
            fig_Ra.savefig(path  + i.split("/")[2] + ".png")
        elif not "steigung" in i:
            fig_Ra.savefig(path + i + ".png")

        plt.pause(2)
        fig_Ra.clf()



    def plot_werkzeug(self,data,Feature,path):
        name=path.split("\\\\")[1]
        path=path.split("\\\\")[0]
        print(path)

        col = data.columns.tolist()
        # set elinewidth to 1 for error bars, order by Werkstoff, Drehzahl, Vorschub
        for i in col:
            fig_Ra = plt.figure(figsize=(6.4, 2))
            ax_Ra = fig_Ra.add_subplot(111)
            ax_Ra.plot(np.arange(len(data[i])), data[i],
                      #yerr=data["Ra_std"],
                       color=(0/255,84/255,159/255), linestyle="-"
                      #  ,width=0.7,edgecolor="white",hatch=9 * ["", "//////"],
                      # color=2 * ["#404040"] + 2 * ["#7F7F7F"] + 2 * ["#D9D9D9"] + 2 * [
                      #     "#00549F"] + 2 * ["#8EBAE5"] + 2 * ["#E8F1FA"] + 2 * [
                      #           "#F6A800"] + 2 * ["#FFCD61"] + 2 * ["#FFEECA"], capsize=2,
                      # error_kw={"elinewidth": 1, "capthick": 1
                      )
            ax_Ra.tick_params(axis='both', which='both', direction="out", length=4, width=1,
                              colors='black', labelsize=14)
            # remove ticks and labels for x-axis
            ax_Ra.tick_params(axis='x', which='both', bottom=False, top=False,
                              labelbottom=True)
            #ax_Ra.set_xticks(np.arange(len(data[i])/50)*50)
            ax_Ra.grid(axis='x', color='#D9D9D9', linestyle='-', linewidth=1)
            ax_Ra.grid(axis='y', color='#D9D9D9', linestyle='-', linewidth=1)
            ax_Ra.set_axisbelow(True)
            fig_Ra.tight_layout()
            # remove the top and right spines
            ax_Ra.spines['top'].set_visible(False)
            ax_Ra.spines['right'].set_visible(False)
            ax_Ra.spines['bottom'].set_visible(True)
            if not abs(data[i].max())<abs(data[i].min()):
                ax_Ra.set_ylim(0, data[i].max())
            else:
                ax_Ra.set_ylim(data[i].min(), 0)
            # save figures
            #fig_Ra.savefig(f"{path}.png'", dpi=300)#
            if not os.path.isdir(path +"\\"+ "plot"):
                os.mkdir(path +"\\"+ "plot")
            fig_Ra.savefig(path +"\\"+ "plot" +"\\"+ name+i.split("/")[2]+".png")
            plt.pause(2)
            fig_Ra.clf()
        data=pd.DataFrame()

    def Feature_plotting_Force(self,Feature):
        Ordner = os.listdir(self.folder)
        for i in Ordner:
            if "PKL" in i:
                print(i)

                path=self.folder+"\\"+i+"\\"+f"Features\\Schnitt10\\{Feature}\\" #Für Kraft oder Schnitt einmal den Wert ändern
                name=os.listdir(path)
                for j in name:
                    if j.endswith(".pkl"):
                        data_path = path + "\\" + j
                        data=pd.read_pickle(data_path)
                        print(data_path)
                        if not data.empty:
                            self.plot_werkzeug(data,Feature,data_path)


folder="C:\\Users\\mauri\\Desktop\\Projektarbeit\\Rohdaten\\Prozessdaten"
equal=Vergleich(folder)
#equal.Vergleich_Strom()
#equal.Vergleich_Kraft()
#equal.Vergleich_Interns()
#equal.Vergleich_Hioki()
#equal.Vergleich_Kraft_Peaks()
#equal.Feature_plotting_Force("Maximalerwert")
pat="C:\\Users\\mauri\\Desktop\\Projektarbeit\\Rohdaten\\Prozessdaten\\V04_PKLData\\Cuts\\Forces\\_V04_Inco718_RexT15_h020_y16°_a4°_vc2_900.pkl"
fac="C:\\Users\mauri\Desktop\Projektarbeit\einzelne Plots für WordPowerpoint\\"
data=pd.read_pickle(pat)
equal.Vergleich_Plot_Werkzeug(data[data.columns[1]],fac)