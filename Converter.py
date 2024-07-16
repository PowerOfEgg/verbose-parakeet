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
from scipy.signal import find_peaks


class TDMSConverter:

    def __init__(self, folder_path, folder_path_Rohdaten, output_folder, output_folder_pkl, output_folder_pkl_cuts,
                 output_folder_pkl_mean):
        self.folder_path = folder_path
        self.folder_path_Rohdaten = folder_path_Rohdaten
        self.output_folder = output_folder
        self.output_folder_pkl = output_folder_pkl
        self.output_folder_pkl_cuts = output_folder_pkl_cuts
        self.output_folder_pkl_mean = output_folder_pkl_mean

    def get_Name(self, folder, output_folder, number):
        pkl_paths = []
        tdms_filenames = os.listdir(folder)
        for tdms_filename in tdms_filenames:
            if tdms_filename.endswith('.tdms'):
                tdms_path = os.path.join(folder, tdms_filename)
                pkl_filename = tdms_filename.replace(".tdms", ".pkl")
                pkl_path = os.path.join(output_folder, pkl_filename)
                pkl_paths.append(pkl_path)
        return pkl_paths[number]

    def get_Name_(self, folder, output_folder, number):
        pkl_paths = []
        tdms_filenames = os.listdir(folder)
        for tdms_filename in tdms_filenames:
            if tdms_filename.endswith('.tdms'):
                tdms_path = os.path.join(folder, tdms_filename)
                pkl_filename = tdms_filename.replace(".tdms", ".pkl")
                pkl_path = os.path.join(output_folder, pkl_filename)
                pkl_paths.append(pkl_filename)
        return pkl_paths[number]

    def tdms_to_pkl(self):

        if not os.path.isdir(self.output_folder):
            os.mkdir(self.output_folder)
        if not os.path.isdir(self.output_folder_pkl_cuts):
            os.mkdir(self.output_folder_pkl_cuts)
        if not os.path.isdir(self.output_folder_pkl):
            os.mkdir(self.output_folder_pkl)
        if not os.path.isdir(self.output_folder_pkl_mean):
            os.mkdir(self.output_folder_pkl_mean)
        if not os.path.isdir(self.output_folder_pkl_cuts + "tabel\\"):
            os.mkdir(self.output_folder_pkl_cuts + "tabel\\")
        if not os.path.isdir(self.output_folder_pkl_mean + "tabel\\"):
            os.mkdir(self.output_folder_pkl_mean + "tabel\\")
        if not os.path.isdir(self.output_folder_pkl + "tabel\\"):
            os.mkdir(self.output_folder_pkl + "tabel\\")
        pkl_filename = self.get_Name(self.folder_path_Rohdaten, self.output_folder_pkl, 3)
        tdms_file = TdmsFile.read(tdms_path)
        df = tdms_file.as_dataframe()
        if df.shape[1] > 19:
            for i in range(11):
                df.pop(df.columns[0])
        df.to_pickle(pkl_path)
        print(f"TDMS-Datei {tdms_filename} wurde in pkl-Datei {pkl_filename} konvertiert.")

    def ALL_plot(self):
        path = self.output_folder_pkl_cuts
        save_path = path + "Uebersicht_alle_Signale\\"
        Name_Ordner = os.listdir(path)
        data = pd.DataFrame()
        if not os.path.isdir(path + "Uebersicht_alle_Signale"):
            os.mkdir(path + "Uebersicht_alle_Signale")
        if not os.path.isdir(save_path):
            os.mkdir(save_path)
        if not os.path.isdir(save_path + "\\Plot"):
            os.mkdir(save_path + "\\Plot")
        if "Uebersicht_alle_Signale" in Name_Ordner:
            Name_Ordner.remove("Uebersicht_alle_Signale")
        Name_dataframe = os.listdir(path + Name_Ordner[1])
        for ii in Name_dataframe:
            data = pd.DataFrame()
            for i in range(len(Name_Ordner)):
                load_path = path + Name_Ordner[i]
                if ii.endswith(".pkl"):
                    if Name_Ordner[i] == "Forces":
                        print(ii)
                        load_Data = pd.read_pickle(load_path + "\\_" + ii)
                        data = pd.concat([data, load_Data])
                        for n in data.columns:
                            path_plot = path + "Uebersicht_alle_Signale\\Plot\\" + ii
                            if not os.path.isdir(path + "Uebersicht_alle_Signale\\Plot\\" + ii):
                                os.mkdir(path + "Uebersicht_alle_Signale\\Plot\\" + ii)
                            data[n].plot()
                            plt.savefig(path_plot + "\\" + n.replace("/", "") + ".png")
                            plt.close()
                    elif Name_Ordner[i] == "Maschinendaten":
                        load_Data = pd.read_pickle(load_path + "\\" + ii + ".pkl")
                        data = pd.concat([data, load_Data])
                        for n in data.columns:
                            path_plot = path + "Uebersicht_alle_Signale\\Plot\\" + ii
                            if not os.path.isdir(path + "Uebersicht_alle_Signale\\Plot\\" + ii):
                                os.mkdir(path + "Uebersicht_alle_Signale\\Plot\\" + ii)
                            data[n].plot()
                            plt.savefig(path_plot + "\\" + n.replace("/", "") + ".png")
                            plt.close()
                    else:
                        load_Data = pd.read_pickle(load_path + "\\" + ii)
                        data = pd.concat([data, load_Data])
                        for n in data.columns:
                            path_plot = path + "Uebersicht_alle_Signale\\Plot\\" + ii
                            if not os.path.isdir(path + "Uebersicht_alle_Signale\\Plot\\" + ii):
                                os.mkdir(path + "Uebersicht_alle_Signale\\Plot\\" + ii)
                            data[n].plot()
                            plt.savefig(path_plot + "\\" + n.replace("/", "") + ".png")
                            plt.close()
                    data.to_pickle(save_path + "\\" + ii + ".pkl")

    def plot_pkl(self, number, folder, outputfolder):
        data = self.open_pkl(number, folder)
        for i in range(data.shape[1]):
            name = self.get_Name_(self.folder_path_Rohdaten, self.output_folder, number)
            name = name.replace(".pkl", "")

            if not os.path.isdir(outputfolder + "Plots\\"):
                os.mkdir(outputfolder + "Plots\\")
            if not os.path.isdir(outputfolder + "Plots\\" + "#sortiert_nach_schrieben\\"):
                os.mkdir(outputfolder + "Plots\\" + "#sortiert_nach_schrieben\\")
            if not os.path.isdir(outputfolder + "Plots\\" + "#sortiert_nach_schrieben\\" + str(
                    re.sub("/", "", data.columns[i])) + "\\"):
                os.mkdir(outputfolder + "Plots\\" + "#sortiert_nach_schrieben\\" + str(
                    re.sub("/", "", data.columns[i])))
            data[data.columns[i]].plot()
            if data.columns[i]=="/'Unbenannt'/'Fx'":
                plt.xlim(-2000,len(data))
                plt.ylim(-100,50)
            else:
                plt.xlim(-2000,len(data))
                plt.ylim(0,4000)
            # plt.ylabel(str(re.sub("/", "", data.columns[i])))
            # plt.xlabel("Versuchspunkte in --")
            plt.savefig(outputfolder + "Plots" "\\" + "#sortiert_nach_schrieben\\" + str(
                re.sub("/", "", data.columns[i]))+"\\" +name + ".png")
            plt.close()

    def get_list_of_pkl(self, filepath):
        items = os.listdir(filepath)
        newlist = []
        for names in items:
            if names.endswith(".pkl"):
                newlist.append(names)
        return newlist

    def open_pkl(self, number, filepath):
        filename = []
        pkl_filename = os.listdir(self.output_folder_pkl)
        for pkl_filename in pkl_filename:
            if pkl_filename.endswith(".pkl"):
                filename.append(pkl_filename)
        data = pd.read_pickle(filepath + filename[number])
        return data

    def cut_Peaks_forces(self, number, filepath):
        output_Data = self.output_folder_pkl_cuts + "Forces\\"
        output_Plot = output_Data + "Plots\\"
        if not os.path.isdir(output_Data):
            os.mkdir(output_Data)
        if not os.path.isdir(output_Plot):
            os.mkdir(output_Plot)
        data = self.open_pkl(number, filepath)
        data.reset_index(inplace=True, drop=False)
        maximum = data["/'Unbenannt'/'Fz'"].max()
        gate = maximum * 0.07
        cuttingpoints = []
        nummerierung = 1
        peak = []
        add_left = 0
        add_right = 0
        s = 0
        index_abstand = 10
        signifikante_steigung = 2
        n = 0
        cut_Data = pd.DataFrame()

        for index, value in data["/'Unbenannt'/'Fz'"].items():
            if float(value) > gate:
                peak.append(index)
        cuttingpoints.append(peak[0])
        cuttingpoints.append(peak[len(peak) - 1])
        if len(cuttingpoints) >= 2:
            for index, value in data["/'Unbenannt'/'Fz'"].iloc[cuttingpoints[1]:].items():
                if value < 50:
                    cuttingpoints[1] = index
                    break
            for i in reversed(range(0, cuttingpoints[0])):
                if data["/'Unbenannt'/'Fz'"].iloc[i] < 50:
                    cuttingpoints[0] = i
                    break

        for ii in ["/'Unbenannt'/'Fx'", "/'Unbenannt'/'Fy'", "/'Unbenannt'/'Fz'"]:
            column_name = ii
            for i in range(len(cuttingpoints) - 1):
                if i + 1 <= len(cuttingpoints):
                    if cuttingpoints[i] - add_left >= 0 and cuttingpoints[i + 1] + add_right < len(data[ii]):
                        cut_Data[column_name] = data[ii].iloc[
                                                cuttingpoints[i] - add_left:cuttingpoints[i + 1] + add_right]
                    if cuttingpoints[i] - add_left < 0:
                        cut_Data[column_name] = data[ii].iloc[cuttingpoints[i]:cuttingpoints[i + 1] + add_right]
                    if cuttingpoints[i + 1] + add_right >= len(data[ii]):
                        cut_Data[column_name] = data[ii].iloc[cuttingpoints[i] - add_left:cuttingpoints[i + 1]]
        cut_Data.reset_index(inplace=True, drop=False)
        cut_Data.to_pickle(output_Data + self.get_list_of_pkl(filepath)[number])

    def plot_tooth(self, folderpath,folder):
        leng = len(os.listdir(folderpath))
        for i in range(len(os.listdir(folderpath))-1):
            name = self.get_list_of_pkl(folderpath)[i]
            data = pd.read_pickle(folderpath + name)
            for ii in range(data.shape[1]):
                if not os.path.isdir(folderpath + "Plots\\"):
                    os.mkdir(folderpath + "Plots\\")
                if not os.path.isdir(folderpath + "Plots\\" ):
                    os.mkdir(folderpath + "Plots\\" )
                if not os.path.isdir(folderpath + "Plots\\"  + str(
                        re.sub("/", "", data.columns[ii])) + "\\"):
                    os.mkdir(
                        folderpath + "Plots\\"  + str(re.sub("/", "", data.columns[ii])))
                if not os.path.isdir(folder  +"#Plots_sortiert_nach_peaks\\"):
                    os.mkdir(folder  +"#Plots_sortiert_nach_peaks\\")
                if not os.path.isdir(folder +  "#Plots_sortiert_nach_peaks\\"+ str(name.split('_')[-1].split('.')[0])+"\\"):
                    os.mkdir(folder  + "#Plots_sortiert_nach_peaks\\" + str(name.split('_')[-1].split('.')[0])+"\\")
                data[data.columns[ii]].plot()
                # plt.ylabel(str(re.sub("/", "", data.columns[i])))
                # plt.xlabel("Versuchspunkte in --")
                plt.savefig(folderpath + "Plots" "\\"  + str(
                    re.sub("/", "", data.columns[ii])) + "//" + name + ".png")
                plt.savefig(folder  + "#Plots_sortiert_nach_peaks\\" +str(name.split('_')[-1].split('.')[0])+"\\" + name + ".png")
                plt.close()

    def cut_Peaks_forces(self, number, filepath):
        output_Data = self.output_folder_pkl_cuts + "Forces\\"
        output_Plot = output_Data + "Plots\\"
        if not os.path.isdir(output_Data):
            os.mkdir(output_Data)
        if not os.path.isdir(output_Plot):
            os.mkdir(output_Plot)
        data = self.open_pkl(number, filepath)
        data.reset_index(inplace=True, drop=False)
        maximum = data["/'Unbenannt'/'Fz'"].max()
        gate = maximum * 0.2
        gate1 = maximum * 0.2
        cuttingpoints = []
        nummerierung = 1
        peak = []
        add_left = 0
        add_right = 0
        s = 0
        index_abstand = 10
        signifikante_steigung = 2
        n = 0
        cut_Data = pd.DataFrame()

        for index, value in data["/'Unbenannt'/'Fz'"].items():
            if float(value) > gate:
                peak.append(index)
        cuttingpoints.append(peak[0])
        cuttingpoints.append(peak[len(peak) - 1])
        if len(cuttingpoints) >= 2:
            for index, value in data["/'Unbenannt'/'Fz'"].iloc[cuttingpoints[1]:].items():
                if value < gate1:
                    cuttingpoints[1] = index
                    break
            for i in reversed(range(0, cuttingpoints[0])):
                if data["/'Unbenannt'/'Fz'"].iloc[i] < gate1 :
                    cuttingpoints[0] = i
                    break
        i=0
        f=0
        for index, value in data["/'Unbenannt'/'Fz'"].iloc[(cuttingpoints[1]+10):(cuttingpoints[1]+100)].items():
                i=i+1
                f=f*(i-1)/i+value/i
        f=f
        if len(cuttingpoints) >= 2:
            for i in reversed(range(0, cuttingpoints[0])):
                if data["/'Unbenannt'/'Fz'"].iloc[i] < gate1*0.15:
                    cuttingpoints[0] = i
                    break
            for index, value in data["/'Unbenannt'/'Fz'"].iloc[cuttingpoints[1]:].items():
                if value < f:
                    cuttingpoints[1] = index
                    break
        for ii in ["/'Unbenannt'/'Fx'", "/'Unbenannt'/'Fy'", "/'Unbenannt'/'Fz'"]:
            column_name = ii
            for i in range(len(cuttingpoints) - 1):
                if i + 1 <= len(cuttingpoints):
                    if cuttingpoints[i] - add_left >= 0 and cuttingpoints[i + 1] + add_right < len(data[ii]):
                        cut_Data[column_name] = data[ii].iloc[
                                                cuttingpoints[i] - add_left:cuttingpoints[i + 1] + add_right]
                    if cuttingpoints[i] - add_left < 0:
                        cut_Data[column_name] = data[ii].iloc[cuttingpoints[i]:cuttingpoints[i + 1] + add_right]
                    if cuttingpoints[i + 1] + add_right >= len(data[ii]):
                        cut_Data[column_name] = data[ii].iloc[cuttingpoints[i] - add_left:cuttingpoints[i + 1]]
        cut_Data.reset_index(inplace=True, drop=False)
        cut_Data.to_pickle(output_Data + self.get_list_of_pkl(filepath)[number])
        #self.plot_pkl(number, output_Data + self.get_list_of_pkl(filepath)[number],
                      #self.output_folder_pkl_cuts + "Forces\\")
        self.plot_pkl(number, output_Data,
                      self.output_folder_pkl_cuts + "Forces\\")

    def cut_Peaks_forces_tooth(self, number, filepath, output):
        data = self.open_pkl(number, filepath)
        name = self.get_list_of_pkl(filepath)[number].replace(".pkl","")
        if not os.path.isdir(output):
            os.mkdir(output)
        if not os.path.isdir(output + "\\" + name):
            os.mkdir(output + "\\" + name)
        output_real = output + "\\" + name + "\\"
        index_abstand = 50
        cut_data_z = pd.DataFrame()
        cut_data_y = pd.DataFrame()
        cut_data_x = pd.DataFrame()
        max = data["/'Unbenannt'/'Fz'"].max()
        signifikante_steigung = 0.00057 * max * 0.9
        signifikante_steigung_runter = 0.00285714 * max * 0.9
        minimaler_hoehendifferenz = 0.01428571 * max * 1
        min_laenge= len(data)*0.012*2

        peak = []
        cuttingpoints = [0]
        data["steigung"] = (data["/'Unbenannt'/'Fz'"].shift(index_abstand) - data["/'Unbenannt'/'Fz'"]).div(
            index_abstand)
        data = data.reset_index(inplace=False)
        for index, value in data["steigung"].items():
            if abs(value) > abs(signifikante_steigung):
                peak.append(index)
        for i in range(len(peak) - index_abstand - 1):
            if peak[i + index_abstand] == peak[i] + index_abstand:
                cuttingpoints.append(peak[i])
        if cuttingpoints[len(cuttingpoints) - 1] != peak[len(peak) - 1]:
            cuttingpoints.append(peak[len(peak) - 1])
        i = 0
        while i < len(cuttingpoints) - 1:
            if abs(cuttingpoints[i] + 1 - cuttingpoints[i + 1]) < minimaler_hoehendifferenz:
                cuttingpoints.pop(i + 1)
                i = 0
            else:
                i = i + 1



        for i in range(0, len(cuttingpoints) - 2, 1):
            Mittelwert = data["/'Unbenannt'/'Fz'"].iloc[cuttingpoints[i]:cuttingpoints[i + 1]].mean()
            if Mittelwert > data["/'Unbenannt'/'Fz'"].iloc[cuttingpoints[i]] or (
                    Mittelwert > data["/'Unbenannt'/'Fz'"].iloc[cuttingpoints[i + 1]] and len(
                    data["/'Unbenannt'/'Fz'"]) * 0.8 < cuttingpoints[i + 1]):

                if data["/'Unbenannt'/'Fz'"].loc[cuttingpoints[i]] > max * 0.5 and data["/'Unbenannt'/'Fz'"].loc[
                    cuttingpoints[i]] < data["/'Unbenannt'/'Fz'"].loc[cuttingpoints[i + 1]]:

                    for index, value in data["/'Unbenannt'/'Fz'"].loc[cuttingpoints[i + 1]:(cuttingpoints[i + 1]+200)].items():
                        if data["/'Unbenannt'/'Fz'"].loc[cuttingpoints[i]] > value * 0.95:
                            cuttingpoints[i + 1] = index
                            break

        i = 0
        while i < len(cuttingpoints) - 1:
            if abs(cuttingpoints[i] - cuttingpoints[i + 1]) < min_laenge:
                cuttingpoints.pop(i + 1)
                i = 0
            else:
                i = i + 1
        if len(cuttingpoints) % 2 == 1:
            cuttingpoints.append(len(data["steigung"]))





        a=minimaler_hoehendifferenz*19
        Nummer_cut = 1
        for i in range(0, len(cuttingpoints) - 2, 1):
            Mittelwert = data["/'Unbenannt'/'Fz'"].iloc[cuttingpoints[i]:cuttingpoints[i + 1]].mean()
            if Mittelwert*0.9 > data["/'Unbenannt'/'Fz'"].iloc[cuttingpoints[i]] or (
                    Mittelwert > data["/'Unbenannt'/'Fz'"].iloc[cuttingpoints[i + 1]] and len(
                    data["/'Unbenannt'/'Fz'"]) * 0.8 < cuttingpoints[i + 1]) :
                #if not abs(cuttingpoints[i] - cuttingpoints[i + 1]) < a and not abs(Mittelwert-cuttingpoints[i]) < a  and not abs(Mittelwert-cuttingpoints[i + 1]) <a:
                cut_data_z["/'Unbenannt'/'Fz'"] = data["/'Unbenannt'/'Fz'"].loc[cuttingpoints[i]:cuttingpoints[i + 1]]
                cut_data_z["/'Unbenannt'/'Fx'"] = data["/'Unbenannt'/'Fx'"].loc[cuttingpoints[i]:cuttingpoints[i + 1]]
                cut_data_z["/'Unbenannt'/'Fy'"] = data["/'Unbenannt'/'Fy'"].loc[cuttingpoints[i]:cuttingpoints[i + 1]]
                cut_data_z.to_pickle(output_real +   name + "_"+str(Nummer_cut)+ ".pkl")
                cut_data_z = pd.DataFrame()
                Nummer_cut = Nummer_cut + 1
        return output_real

    def get_peak_Index(self,number,filepath):
        name=self.get_Name_(self.folder_path_Rohdaten,self.folder_path,number)
        name=name.replace(".pkl","")
        name="_"+name
        cut= pd.DataFrame({'Index0': [], 'Index1': []})
        for i in range(1,len(os.listdir(filepath +name+"\\"))):
            data = self.open_pkl_for_get_peak_index(number,filepath + name+"\\",i)
            new_row=pd.DataFrame({'Index0': [data.index[0]], 'Index1': [data.index[-1]]})
            cut=pd.concat([cut,new_row])
            cut= cut.reset_index(drop=True)
        return cut

    def open_pkl_for_get_peak_index(self, number, filepath, i):
        filename = []
        pkl_filename = os.listdir(self.output_folder_pkl)
        for pkl_filename in pkl_filename:
            if pkl_filename.endswith(".pkl"):
                filename.append(pkl_filename)
        filename[number] = filename[number].replace(".pkl", "")
        filename[number] = filename[number] + "_" + str(i)
        filename[number] = filename[number] + ".pkl"
        data = pd.read_pickle(filepath + filename[number])
        return data

    def cut_1_LM(self, number, filepath, output_folder):
        data = self.open_pkl(number, filepath)
        data_Fc = self.open_pkl(number, self.output_folder_pkl_cuts + "\\Forces\\")
        LM = pd.DataFrame()
        name = self.get_Name_(self.folder_path_Rohdaten, self.output_folder, number)
        name = name.replace(".pkl", "")
        mean = data["/'Unbenannt'/'I1-LM'"].iloc[0:100].mean()
        mean_R = data["/'Unbenannt'/'I1-LM'"].iloc[len(data) - 100:len(data)].mean()
        h = [mean + 0.1, mean - 0.1]
        j = [mean_R + 0.1, mean_R - 0.1]
        # findet die Punkte an denen die Leistung geschnitten werden soll
        for index, value in data["/'Unbenannt'/'I1-LM'"].items():
            if h[0] < value or h[1] > value:
                cut_points = [index]
                break
        for index, value in data["/'Unbenannt'/'I1-LM'"].iloc[::-1].items():
            if j[0] < value or j[1] > value:
                cut_points.append(index)
                break
        if len(cut_points) == 0:
            cut_points = [0, len(data) - 1]
        # speichert die geschnittenen Daten in LM
        for i in ["/'Unbenannt'/'I1-LM'", "/'Unbenannt'/'I2-LM'", "/'Unbenannt'/'Wirkleistung'", "/'Unbenannt'/'U2-LM'",
                  "/'Unbenannt'/'U1-LM'", "/'Unbenannt'/'I1-JP'", "/'Unbenannt'/'I2-JP'", "/'Unbenannt'/'I3-JP'"]:
            LM[i] = data[i].iloc[cut_points[0]:cut_points[1]]
        LM.reset_index(inplace=True, drop=False)
        cut = []
        gate = [LM["/'Unbenannt'/'I1-LM'"].max() * 0, LM["/'Unbenannt'/'I2-LM'"].max() * 0]
        gate_low = [LM["/'Unbenannt'/'I1-LM'"].min() * 0, LM["/'Unbenannt'/'I2-LM'"].min() * 0]
        # gibt in cut alle Daten aus, die größer als 0 sind
        for index, value in LM["/'Unbenannt'/'I1-LM'"].items():
            if value > gate[0]:
                cut.append(index)
        cut2 = []

        for index, value in LM["/'Unbenannt'/'I2-LM'"].items():
            if value > gate[0]:
                cut2.append(index)
        i = 0
        # erstellt in cut_tr die positiven Parabeln
        cut_tr2 = []
        while i < len(cut2) - 1:
            if abs(cut2[i] - cut2[i + 1]) > 50:
                cut_tr2.append(cut2[i])
                cut_tr2.append(cut2[i + 1])
                i = i + 1
            else:
                i = i + 1
        # cut_tr2.append(cut2[len(cut2)-1])
        i = 0
        cut_tr = []
        while i < len(cut) - 1:
            if abs(cut[i] - cut[i + 1]) > 50:
                cut_tr.append(cut[i])
                cut_tr.append(cut[i + 1])
                i = i + 1
            else:
                i = i + 1
        # cut_tr.append(cut[len(cut)-1])

        v_locmax = pd.DataFrame({'Index': [0], 'Peaks LM': [0]})
        for i in range(len(cut_tr)):
            if LM["/'Unbenannt'/'I1-LM'"].iloc[cut_tr[i]] - LM["/'Unbenannt'/'I1-LM'"].iloc[cut_tr[i] + 10] < 0:
                if len(cut_tr) > i + 1:
                    locmax = int((abs(cut_tr[i] - cut_tr[i + 1])) / 2) + cut_tr[i]
                    new_row = pd.DataFrame({'Index': [locmax], 'Peaks LM': [LM["/'Unbenannt'/'I1-LM'"].loc[locmax]]})
                    v_locmax = pd.concat([v_locmax, new_row], ignore_index=True)
        for i in range(len(cut_tr)):
            if LM["/'Unbenannt'/'I1-LM'"].iloc[cut_tr[i]] - LM["/'Unbenannt'/'I1-LM'"].iloc[cut_tr[i] + 10] > 0:
                if len(cut_tr) > i + 1:
                    locmax = int((abs(cut_tr[i] - cut_tr[i + 1])) / 2) + cut_tr[i]
                    new_row = pd.DataFrame({'Index': [locmax], 'Peaks LM': [LM["/'Unbenannt'/'I1-LM'"].loc[locmax]]})
                    v_locmax = pd.concat([v_locmax, new_row], ignore_index=True)
        for i in range(len(cut_tr2)):
            if LM["/'Unbenannt'/'I2-LM'"].iloc[cut_tr2[i]] - LM["/'Unbenannt'/'I2-LM'"].iloc[cut_tr2[i] + 10] < 0:
                if len(cut_tr2) > i + 1:
                    locmax = int((abs(cut_tr2[i] - cut_tr2[i + 1])) / 2) + cut_tr2[i]
                    new_row = pd.DataFrame({'Index': [locmax], 'Peaks LM': [LM["/'Unbenannt'/'I2-LM'"].loc[locmax]]})
                    v_locmax = pd.concat([v_locmax, new_row], ignore_index=True)
        for i in range(len(cut_tr2)):
            if LM["/'Unbenannt'/'I2-LM'"].iloc[cut_tr2[i]] - LM["/'Unbenannt'/'I2-LM'"].iloc[cut_tr2[i] + 10] > 0:
                if len(cut_tr2) > i + 1:
                    locmax = int((abs(cut_tr2[i] - cut_tr2[i + 1])) / 2) + cut_tr2[i]
                    new_row = pd.DataFrame({'Index': [locmax], 'Peaks LM': [LM["/'Unbenannt'/'I2-LM'"].loc[locmax]]})
                    v_locmax = pd.concat([v_locmax, new_row], ignore_index=True)
        v_locmax = v_locmax.sort_values(by="Index", ascending=True)
        v_locmax = v_locmax.drop(index=0)
        v_locmax = v_locmax.reset_index(drop=True)
        l = len(data_Fc)
        tr_loc = pd.DataFrame({'Index0': [], 'Index1': [], "Mean_Peaks_LM": []})
        for ii in range(len(v_locmax)):
            c = v_locmax["Index"].iloc[ii]
            v = v_locmax["Peaks LM"].iloc[ii]
            t = 0
            for i in range(len(v_locmax)):
                match i:
                    case x if (v_locmax["Index"].iloc[i] - c) > l and t == 0:
                        new_roww = pd.DataFrame({'Index0': [ii], 'Index1': [i],
                                                 "Mean_Peaks_LM": [abs(v_locmax["Peaks LM"].iloc[ii:i]).mean()]})
                        tr_loc = pd.concat([tr_loc, new_roww])
                        t = 1

        tr_loc = tr_loc.reset_index(drop=True)
        min_mean_peaks_lm = tr_loc['Mean_Peaks_LM'].min()
        min_index = tr_loc[tr_loc['Mean_Peaks_LM'] == min_mean_peaks_lm].index[0]
        cutfinal = [int(tr_loc.loc[min_index, 'Index0']), int(tr_loc.loc[min_index, 'Index1'])]  #

        cutfinal = [v_locmax.loc[cutfinal[0], "Index"], v_locmax.loc[cutfinal[1], "Index"]]

        delta = cutfinal[1] - cutfinal[0]
        if delta != l:
            delta = l - delta
        cutfinal[0] = int(cutfinal[0] + delta / 2)
        cutfinal[1] = int(cutfinal[1] + delta / 2)
        sync = LM.iloc[cutfinal[0]:cutfinal[1]]
        sync = sync.reset_index(drop=True)
        Fc_peaks = converter_1.get_peak_Index(number, self.output_folder + "Cuts\\Forces\\peaks_only\\")

        if not os.path.isdir(output_folder):
            os.mkdir(output_folder)
        if not os.path.isdir(output_folder + "I_LM\\"):
            os.mkdir(output_folder + "I_LM\\")
        if not os.path.isdir(output_folder + "I_LM\\#peaks\\"):
            os.mkdir(output_folder + "I_LM\\#peaks\\")
        if not os.path.isdir(output_folder + "I_LM\\#peaks\\Plots\\"):
            os.mkdir(output_folder + "I_LM\\#peaks\\Plots\\")
        if not os.path.isdir(output_folder + "I_LM\\Plots"):
            os.mkdir(output_folder + "I_LM\\Plots")
        if not os.path.isdir(output_folder + "I_LM\\Plots"):
            os.mkdir(output_folder + "I_LM\\Plots")
        # for i in range(1, 3):
        #     if not os.path.isdir(output_folder + "I_LM\\Plots\\" + str(re.sub("/", "", sync.columns[i])) + "\\"):
        #         os.mkdir(output_folder + "I_LM\\Plots\\" + str(re.sub("/", "", sync.columns[i])) + "\\")
        #     LM[LM.columns[i]].plot()
        #     plt.ylim(-2, 2)
        #     plt.savefig(output_folder + "I_LM\\Plots\\" + str(re.sub("/", "", sync.columns[i])) + "\\" + name + ".png")
        #     plt.close()
        # sync.to_pickle(output_folder + "I_LM\\" + name + ".pkl")
        for i in range(1, 3):
            if not os.path.isdir(output_folder + "I_LM\\Plots\\" + str(re.sub("/", "", sync.columns[i])) + "\\"):
                os.mkdir(output_folder + "I_LM\\Plots\\" + str(re.sub("/", "", sync.columns[i])) + "\\")

            sync[sync.columns[i]].plot()
            plt.ylim(-2, 2)
            plt.savefig(output_folder + "I_LM\\Plots\\" + str(re.sub("/", "", sync.columns[i])) + "\\" + name + ".png")
            plt.close()
        sync.to_pickle(output_folder + "I_LM\\" + name + ".pkl")
        if not os.path.isdir(output_folder + "I_LM\\#peaks\\" + name + "\\"):
            os.mkdir(output_folder + "I_LM\\#peaks\\" + name + "\\")
        for i in range(len(Fc_peaks)):
            syn = sync.loc[Fc_peaks["Index0"].loc[i]:Fc_peaks["Index1"].loc[i]]
            for ii in range(1, 3):
                if not os.path.isdir(
                        output_folder + "I_LM\\#peaks\\Plots\\" + str(re.sub("/", "", syn.columns[ii])) + "\\"):
                    os.mkdir(output_folder + "I_LM\\#peaks\\Plots\\" + str(re.sub("/", "", syn.columns[ii])) + "\\")
                syn[syn.columns[ii]].plot()
                plt.ylim(-2, 2)
                plt.savefig(output_folder + "I_LM\\#peaks\\Plots\\" + str(
                    re.sub("/", "", syn.columns[ii])) + "\\" + name + "_" + str(i) + ".png")
                plt.close()
            syn.to_pickle(output_folder + "I_LM\\#peaks\\" + name + "\\" + name + "_" + str(i) + ".pkl")
    # def save_Interns(self,data,filepath,output_folder):
    #
    #     free=pd.DataFrame({"/'Unbenannt'/'I1-LM'", "/'Unbenannt'/'I2-LM'", "/'Unbenannt'/'Wirkleistung'", "/'Unbenannt'/'U2-LM'", "/'Unbenannt'/'U1-LM'", "/'Unbenannt'/'I1-JP'","/'Unbenannt'/'I2-JP'","/'Unbenannt'/'I3-JP'"})
    #     cutfinal=[1,1]
    #     paare_haeufigkeit = data.groupby(['0', '1']).size().reset_index(name='Häufigkeit')
    #     paare_haeufigkeit = paare_haeufigkeit.sort_values(by='Häufigkeit', ascending=False)
    #     paare_haeufigkeit = paare_haeufigkeit.reset_index(drop=True)
    #     if len(paare_haeufigkeit) > 100:
    #         cutfinal[0]=paare_haeufigkeit["0"].loc[0]
    #         cutfinal[1]=paare_haeufigkeit["1"].loc[0]
    #     else:
    #         paare_haeufigkeit = data.groupby(['0']).size().reset_index(name='Häufigkeit')
    #         paare_haeufigkeit = paare_haeufigkeit.sort_values(by='Häufigkeit', ascending=False)
    #         paare_haeufigkeit = paare_haeufigkeit.reset_index(drop=True)
    #         print(paare_haeufigkeit)
    #         cutfinal[0] = paare_haeufigkeit["0"].loc[0]
    #         cutfinal[1] = paare_haeufigkeit["1"].loc[0]
    #     for g in range(1,len(data)+1):
    #         print(cutfinal)
    #         free = pd.DataFrame(
    #             {"/'Unbenannt'/'I1-LM'":[], "/'Unbenannt'/'I2-LM'":[], "/'Unbenannt'/'Wirkleistung'":[], "/'Unbenannt'/'U2-LM'":[],
    #              "/'Unbenannt'/'U1-LM'":[], "/'Unbenannt'/'I1-JP'":[], "/'Unbenannt'/'I2-JP'":[], "/'Unbenannt'/'I3-JP'":[]})
    #         name = self.get_Name_(self.folder_path_Rohdaten, self.output_folder, g)
    #         name = name.replace(".pkl", "")
    #         data = self.open_pkl(g, filepath)
    #         print(data)
    #         for i in ["/'Unbenannt'/'I1-LM'", "/'Unbenannt'/'I2-LM'", "/'Unbenannt'/'Wirkleistung'", "/'Unbenannt'/'U2-LM'", "/'Unbenannt'/'U1-LM'", "/'Unbenannt'/'I1-JP'","/'Unbenannt'/'I2-JP'","/'Unbenannt'/'I3-JP'"]:
    #             free[i] = data[i].iloc[cutfinal[0]:cutfinal[1]]
    #         print(free)
    #         sync = free
    #         # sync = sync.reset_index(drop=True)
    #         Fc_peaks = converter_1.get_peak_Index(g, self.output_folder + "Cuts\\Forces\\peaks_only\\")
    #         if not os.path.isdir(output_folder):
    #             os.mkdir(output_folder)
    #         if not os.path.isdir(output_folder + "I_LM\\"):
    #             os.mkdir(output_folder + "I_LM\\")
    #         if not os.path.isdir(output_folder + "I_LM\\#peaks\\"):
    #             os.mkdir(output_folder + "I_LM\\#peaks\\")
    #         if not os.path.isdir(output_folder + "I_LM\\#peaks\\Plots\\"):
    #             os.mkdir(output_folder + "I_LM\\#peaks\\Plots\\")
    #         if not os.path.isdir(output_folder + "I_LM\\Plots"):
    #             os.mkdir(output_folder + "I_LM\\Plots")
    #         if not os.path.isdir(output_folder + "I_LM\\Plots"):
    #             os.mkdir(output_folder + "I_LM\\Plots")
    #         # for i in range(1, 3):
    #         #     if not os.path.isdir(output_folder + "I_LM\\Plots\\" + str(re.sub("/", "", sync.columns[i])) + "\\"):
    #         #         os.mkdir(output_folder + "I_LM\\Plots\\" + str(re.sub("/", "", sync.columns[i])) + "\\")
    #         #     LM[LM.columns[i]].plot()
    #         #     plt.ylim(-2, 2)
    #         #     plt.savefig(output_folder + "I_LM\\Plots\\" + str(re.sub("/", "", sync.columns[i])) + "\\" + name + ".png")
    #         #     plt.close()
    #         # sync.to_pickle(output_folder + "I_LM\\" + name + ".pkl")
    #         for i in range(1, 3):
    #             if not os.path.isdir(output_folder + "I_LM\\Plots\\" + str(re.sub("/", "", sync.columns[i])) + "\\"):
    #                 os.mkdir(output_folder + "I_LM\\Plots\\" + str(re.sub("/", "", sync.columns[i])) + "\\")
    #
    #             sync[sync.columns[i]].plot()
    #             plt.ylim(-2, 2)
    #             plt.savefig(output_folder + "I_LM\\Plots\\" + str(re.sub("/", "", sync.columns[i])) + "\\" + name + ".png")
    #             plt.close()
    #         sync.to_pickle(output_folder + "I_LM\\" + name + ".pkl")
    #         if not os.path.isdir(output_folder + "I_LM\\#peaks\\" + name + "\\"):
    #             os.mkdir(output_folder + "I_LM\\#peaks\\" + name + "\\")
    #         for i in range(len(Fc_peaks)):
    #             syn = sync.loc[Fc_peaks["Index0"].loc[i]:Fc_peaks["Index1"].loc[i]]
    #             for ii in range(1, 3):
    #                 if not os.path.isdir(
    #                         output_folder + "I_LM\\#peaks\\Plots\\" + str(re.sub("/", "", syn.columns[ii])) + "\\"):
    #                     os.mkdir(output_folder + "I_LM\\#peaks\\Plots\\" + str(re.sub("/", "", syn.columns[ii])) + "\\")
    #                 syn[syn.columns[ii]].plot()
    #                 plt.ylim(-2, 2)
    #                 plt.savefig(output_folder + "I_LM\\#peaks\\Plots\\" + str(
    #                     re.sub("/", "", syn.columns[ii])) + "\\" + name + "_" + str(i) + ".png")
    #                 plt.close()
    #             syn.to_pickle(output_folder + "I_LM\\#peaks\\" + name + "\\" + name + "_" + str(i) + ".pkl")
#___________________________________________________________________________________________________________________________-
        # for j in range(len(v_locmax)-2):
        #     start=v_locmax["Peaks LM"].iloc[j]
        #     start_index = v_locmax["Index"].iloc[j]
        #     mittlere_Steigung=(abs(v_locmax["Peaks LM"].iloc[j+1])-abs(v_locmax["Peaks LM"].iloc[j]))/(v_locmax["Index"].iloc[j+1]-v_locmax["Index"].iloc[j])
        #     for i in range(v_locmax["Index"].iloc[j],v_locmax["Index"].iloc[j+1],2):
        #         new_row = pd.DataFrame({'Index': [i], 'Peaks LM': [abs(start + mittlere_Steigung*(i-start_index))]})
        #         #new_row = pd.DataFrame({'Index': [i], 'Peaks LM': [abs(start )]})
        #         envelope = pd.concat([envelope, new_row], ignore_index=True)
        # envelope=envelope.sort_values(by="Index", ascending=True)
        # envelope.reset_index(drop=True)

        # sync=pd.DataFrame()
        # sync["/'Unbenannt'/'I1-LM'"]=LM["/'Unbenannt'/'I1-LM'"].iloc[a:b]
        # sync["/'Unbenannt'/'I2-LM'"]=LM["/'Unbenannt'/'I2-LM'"].iloc[a:b]
        # sync.reset_index(inplace=True, drop=False)
        # if not os.path.isdir(output_folder):
        #     os.mkdir(output_folder)
        # if not os.path.isdir(output_folder+"I_LM\\"):
        #     os.mkdir(output_folder+"I_LM\\")
        # if not os.path.isdir(output_folder+"I_LM\\Plots"):
        #     os.mkdir(output_folder+"I_LM\\Plots")
        # for i in range(1,3):
        #     if not os.path.isdir(output_folder+"I_LM\\Plots\\"+ str(re.sub("/", "", sync.columns[i])) + "\\"):
        #         os.mkdir(output_folder+"I_LM\\Plots\\"+ str(re.sub("/", "", sync.columns[i])) + "\\")
        #     sync[sync.columns[i]].plot()
        #     plt.ylim(-2,2)
        #     plt.savefig(output_folder+"I_LM\\Plots\\"+ str(re.sub("/", "", sync.columns[i])) + "\\"+ name+".png")
        #     plt.close()
        # sync.to_pickle(output_folder+"I_LM\\"+ name+".pkl")

    def cut_interns(self, number, folderpath, output_folder):
        name = self.get_Name_(self.folder_path_Rohdaten, self.folder_path_Rohdaten, number)
        data1 = pd.DataFrame()
        data = pd.read_pickle(folderpath + "_" + name)
        cuttingpoints = []
        index_abstand = 10
        data1 = pd.DataFrame(
            {"/'Unbenannt'/'Z_Wirkleistung'": [], "/'Unbenannt'/'Z_Drehmoment'": [], "/'Unbenannt'/'Z_Strom'": [],
             "steigung": []})
        for index, value in data["/'Unbenannt'/'Z_Wirkleistung'"].items():
            match value:
                case x if abs(value) > 10:
                    cuttingpoints.append(index)
                    break
        for i in reversed(range(len(data["/'Unbenannt'/'Z_Wirkleistung'"]))):
            match i:
                case x if abs(data["/'Unbenannt'/'Z_Wirkleistung'"].iloc[i]) > 10:
                    cuttingpoints.append(i)
                    break
        data1["steigung"] = (data["/'Unbenannt'/'Z_Wirkleistung'"].shift(index_abstand) - data[
            "/'Unbenannt'/'Z_Wirkleistung'"]).div(index_abstand).dropna()
        data1["steigung"].reset_index(drop=True)
        data1["/'Unbenannt'/'Z_Wirkleistung'"] = data["/'Unbenannt'/'Z_Wirkleistung'"].dropna()
        data1["/'Unbenannt'/'Z_Drehmoment'"] = data["/'Unbenannt'/'Z_Drehmoment'"].dropna()
        data1["/'Unbenannt'/'Z_Strom'"] = data["/'Unbenannt'/'Z_Strom'"].dropna()
        for index, value in data1["steigung"].iloc[cuttingpoints[0]:].items():
            if abs(value) < 2:
                cuttingpoints[0] = index
                break
        i = 0
        f = 0
        for index, value in data1["/'Unbenannt'/'Z_Wirkleistung'"].iloc[
                            (cuttingpoints[0] + 10):(cuttingpoints[0] + 60)].items():
            i = i + 1
            f = f * (i - 1) / (i) + value / i
        gate = abs(f * 0.99)
        new_zero = []
        for index, value in data1["/'Unbenannt'/'Z_Wirkleistung'"].items():
            if abs(value) > gate:
                new_zero.append(index)
        i = 0
        d=0
        new_z = []
        while i < len(new_zero)-1:
            if abs(new_zero[i]-new_zero[i+1])>50:
                new_z=[new_zero[i],new_zero[i+1]]
            i=i+1

        cuttingpoints = [new_z[0] - 1, new_z[1] + 1]

        cuttingpoints[0]=data1["/'Unbenannt'/'Z_Wirkleistung'"].iloc[:cuttingpoints[0]].idxmin()
        cuttingpoints[1]=data1["/'Unbenannt'/'Z_Wirkleistung'"].iloc[cuttingpoints[1]:].idxmin()
        gate = data1["steigung"].iloc[cuttingpoints[0]:(cuttingpoints[1]-20)].max()
        print(len(data1["steigung"]))
        if cuttingpoints[1]>len(data1["steigung"]):
            for i in reversed(range(len(data1["steigung"]))):
                if data1["steigung"].iloc[i] > gate*0.4:
                    cuttingpoints[1] = i
                    break
        else:
            for i in reversed(range(cuttingpoints[1])):
                if data1["steigung"].iloc[i] > gate*0.4:
                    cuttingpoints[1] = i
                    break


        # print(gate)
        for index, value in data1["steigung"].iloc[cuttingpoints[0]:cuttingpoints[1]].items():
            if abs(value)>gate*0.4:
                cuttingpoints[0] = index
                break
        # data1["steigung"].iloc[cuttingpoints[0]:cuttingpoints[1]].plot()
        # plt.show()


        # print(data["/'Unbenannt'/'Z_Wirkleistung'"].iloc[data["/'Unbenannt'/'Z_Wirkleistung'"].iloc[cuttingpoints[1]:].idxmin()])
        # print(data["/'Unbenannt'/'Z_Wirkleistung'"].iloc[cuttingpoints[1]:].min())
        data1 = data1.iloc[cuttingpoints[0]-index_abstand:cuttingpoints[1]]
        #data1 = data1.reset_index(drop=True)
        if not os.path.isdir(output_folder):
            os.mkdir(output_folder)
        if not os.path.isdir(output_folder + "Maschinendaten\\"):
            os.mkdir(output_folder + "Maschinendaten\\")
        if not os.path.isdir(output_folder + "Maschinendaten\\#peaks\\"):
            os.mkdir(output_folder + "Maschinendaten\\#peaks\\")
        if not os.path.isdir(output_folder + "Maschinendaten\\#peaks\\Plots\\"):
            os.mkdir(output_folder + "Maschinendaten\\#peaks\\Plots\\")
        if not os.path.isdir(output_folder + "Maschinendaten\\Plots"):
            os.mkdir(output_folder + "Maschinendaten\\Plots")
        for i in range(0, 3):
            if not os.path.isdir(
                    output_folder + "Maschinendaten\\Plots\\" + str(re.sub("/", "", data1.columns[i])) + "\\"):
                os.mkdir(output_folder + "Maschinendaten\\Plots\\" + str(re.sub("/", "", data1.columns[i])) + "\\")
            data1[data1.columns[i]].plot()
            plt.savefig(output_folder + "Maschinendaten\\Plots\\" + str(
                re.sub("/", "", data1.columns[i])) + "\\" + name + ".png")
            plt.close()
        data1.to_pickle(output_folder + "Maschinendaten\\" + name )
        print(name)

    def sync_interns(self):
        path=self.output_folder_pkl_cuts + "\\Maschinendaten\\"
        output_folder=self.output_folder_pkl_cuts
        path_data=[]
        b=pd.Series()
        df_ind=pd.DataFrame({"Index_0":[],"Index_1":[]})
        for name in os.listdir(path):
            if name.endswith(".pkl"):
                data2 = pd.read_pickle(path + name)
                cut=[]
                faktor=1.07
                gate=data2["/'Unbenannt'/'Z_Wirkleistung'"].max()*faktor
                for index,value in data2["/'Unbenannt'/'Z_Wirkleistung'"].items():
                    if gate<value:
                        cut.append(index)
                        break
                for i in reversed(range(data2.index[0],data2.index[-1])):
                    if data2["/'Unbenannt'/'Z_Wirkleistung'"].loc[i]>gate:
                        cut.append(i)
                        break
                if not cut==[]:
                    data=data2.loc[cut[0]:cut[1]]
                else:
                    data=data2
                peaks,_=find_peaks(data["/'Unbenannt'/'Z_Wirkleistung'"])
                #print(data["/'Unbenannt'/'Z_Wirkleistung'"].iloc[peaks])
                a=data["/'Unbenannt'/'Z_Wirkleistung'"].iloc[peaks]
                if not b.empty:
                    b=pd.concat([b,pd.Series(a.index[0])],ignore_index=True)
                else:
                    b=pd.Series(a.index[0])
        if len(b)<100:
            Eintraege_Anzahl=b.value_counts()
            erstes_max=Eintraege_Anzahl.index[4]
        else:
            Eintraege_Anzahl = b.value_counts()
            erstes_max = Eintraege_Anzahl.index[0]
        for name in os.listdir(path):
            if name.endswith(".pkl"):
                data2 = pd.read_pickle(path + name)
                cut = []
                gate = data2["/'Unbenannt'/'Z_Wirkleistung'"].max() * faktor
                for index, value in data2["/'Unbenannt'/'Z_Wirkleistung'"].items():
                    if gate < value:
                        cut.append(index)
                        break
                for i in reversed(range(data2.index[0], data2.index[-1])):
                    if data2["/'Unbenannt'/'Z_Wirkleistung'"].loc[i] > gate:
                        cut.append(i)
                        break
                if not cut == []:
                    data = data2.loc[cut[0]:cut[1]]
                else:
                    data = data2
                print(data)
                print(data2)
                peaks, _ = find_peaks(data["/'Unbenannt'/'Z_Wirkleistung'"])
                # print(data["/'Unbenannt'/'Z_Wirkleistung'"].iloc[peaks])
                a = data["/'Unbenannt'/'Z_Wirkleistung'"].iloc[peaks]
                print(name)
                print(a.index[0])
                shift_amount=erstes_max-a.index[0]

                #print(shift_amount)
                #print(shift_amount-a.index[0])

                data1=data2
                data1.index = data1.index + shift_amount
                data1.to_pickle(path + name)
                for i in range(0, 3):
                    if not os.path.isdir(
                            output_folder + "Maschinendaten\\Plots\\" + str(re.sub("/", "", data1.columns[i])) + "\\"):
                        os.mkdir(
                            output_folder + "Maschinendaten\\Plots\\" + str(re.sub("/", "", data1.columns[i])) + "\\")
                    data1[data1.columns[i]].plot()
                    plt.savefig(output_folder + "Maschinendaten\\Plots\\" + str(
                        re.sub("/", "", data1.columns[i])) + "\\" + name+ ".png")
                    plt.close()

    def schnitt10fach(self,folderpath, output_folder):
        if not os.path.isdir(output_folder):
            os.mkdir(output_folder)

        for path in os.listdir(folderpath):
            d = 0
            if not os.path.isdir(os.path.join(output_folder, path)):
                os.mkdir(os.path.join(output_folder, path))
            Pfad=os.path.join(output_folder, path)
            if not os.path.isdir(Pfad+ "\\#Plot\\"):
                os.mkdir(Pfad + "\\#Plot\\")
            for name in os.listdir(os.path.join(folderpath, path)):
                d=d+1
                print(path+str(d))
                if name.endswith(".pkl"):
                    data = pd.read_pickle(os.path.join(folderpath, path)+"\\"+name)
                    Anzahl_schnitte=10
                    Schnittlaenge=(len(data)-1)/Anzahl_schnitte
                    for i in range(Anzahl_schnitte):
                        if not os.path.isdir(os.path.join(output_folder, path)+"\\"+name.replace(".pkl","")):
                            os.mkdir(os.path.join(output_folder, path)+"\\"+name.replace(".pkl",""))
                        if not os.path.isdir(os.path.join(output_folder, path)+"\\#Plot\\"+name.replace(".pkl","")):
                            os.mkdir(os.path.join(output_folder, path)+"\\#Plot\\"+name.replace(".pkl",""))
                        cuttingpoints=[int(Schnittlaenge*i),int(Schnittlaenge*(i+1))]
                        save=data.iloc[cuttingpoints[0]:cuttingpoints[1]]
                        save.to_pickle(os.path.join(output_folder +"\\" +path + "\\", name.replace(".pkl","")+"\\"+name.replace(".pkl","")+"_"+ str(i) + ".pkl"))
                        if path =="Maschinendaten":
                            for ii in range(0,save.shape[1]-1):
                                save[save.columns[ii]].plot()
                        else:
                            for ii in range(1,save.shape[1]):
                                save[save.columns[ii]].plot()
                        plt.legend()
                        plt.savefig(os.path.join(output_folder +"\\"+ path + "\\#Plot\\", name.replace(".pkl","")+ "\\"+str(i) + ".png"))
                        plt.close()

    def All_means_funktnet(self,folderpath,output_folder):
        combined_data = pd.DataFrame()
        dividend = 1
        path=folderpath + "\\Uebersicht_alle_Signale\\"
        Name=os.listdir(path)
        Mean_Width=49
        d=0
        e=0

        def make_indices_unique(df):
            # Doppelte Indizes entfernen und eindeutige Indizes festlegen
            df = df[~df.index.duplicated(keep='first')]
            return df

        for i in Name:
            if i.endswith(".pkl") and d < Mean_Width:
                load_path = os.path.join(path, i)
                data = pd.read_pickle(load_path)

                # Indizes eindeutig machen
                data = make_indices_unique(data)

                if combined_data.empty:
                    combined_data = data
                else:
                    # Indizes von combined_data ebenfalls eindeutig machen
                    combined_data = make_indices_unique(combined_data)

                    # Sicherstellen, dass die Indizes konsistent sind
                    if combined_data.shape[0] >= data.shape[0]:
                        data = data.reindex(combined_data.index, method='ffill')
                    else:
                        combined_data = combined_data.reindex(data.index)

                    # Sicherstellen, dass die Spalten konsistent sind
                    common_columns = combined_data.columns.intersection(data.columns)
                    combined_data = combined_data[common_columns]
                    data = data[common_columns]

                    # Mittelwertberechnung
                    combined_data = combined_data.mul((dividend - 1) / dividend) + data.div(dividend)

                dividend += 1
                print(i)
                d += 1
                e += 1
            elif d==Mean_Width:
                combined_data.to_pickle(output_folder + "\\" + i)
                for nn in combined_data.columns:
                    combined_data[nn].plot()
                    if not os.path.isdir(output_folder + "\\Plot\\"):
                        os.mkdir(output_folder + "\\Plot\\")
                    if not os.path.isdir(output_folder + "\\Plot\\" + nn.replace("/","")):
                        os.mkdir(output_folder + "\\Plot\\" + nn.replace("/",""))
                    plt.savefig(output_folder + "\\Plot\\" + nn.replace("/","") + "\\" + i + ".png")
                    plt.close()
                d=0
            else:
                print("ERROR")
        return combined_data









#_____________________________________________________________________________________________________________________
for mum in range(4,10):
    Versuchspunkt = mum
    folder_path_1 = "C:\\Users\\mauri\\Desktop\\Projektarbeit\\Rohdaten\\Prozessdaten\\"
    folder_path_Rohdaten_1 = folder_path_1 + "V0" + str(Versuchspunkt) + "_014031\\"
    output_folder_1 = folder_path_1 + "V0" + str(Versuchspunkt) + "_PKLData\\"
    output_folder_pkl_1 = output_folder_1 + "Daten_pkl\\"
    output_folder_pkl_cuts_1 = output_folder_1 + "Cuts\\"
    output_folder_pkl_mean_1 = output_folder_1 + "Mean\\"
    name_spaltenüberschrift_1 = ["/'Device1'/'Fx'", "/'Device1'/'Fy'", "/'Device1'/'Fz'", "/'Device1'/'CalibrationForce'"]

    converter_1 = TDMSConverter(folder_path_1, folder_path_Rohdaten_1, output_folder_1, output_folder_pkl_1,
                                output_folder_pkl_cuts_1, output_folder_pkl_mean_1)

    #converter_1.cut_interns(1, output_folder_pkl_1, output_folder_pkl_cuts_1)

    # Erstellt mean über jeweils 50 Messungen
    # converter_1.All_means(output_folder_pkl_cuts_1,output_folder_pkl_mean_1)

    # lädt alle Synchronisierten Daten in eine PKL Datei
    # converter_1.ALL_plot()

    #erstellt 10fachen Schnitt der Singale im angegebenen Ordner
    print(f"V{mum}")
    converter_1.schnitt10fach(output_folder_pkl_cuts_1, output_folder_1 + "Schnitte_10fach")

    #erstellt interne Maschinendaten
    # for ii in range(0,len(os.listdir(output_folder_pkl_1)) - 1):
    #     converter_1.cut_interns(ii,output_folder_pkl_1,output_folder_pkl_cuts_1)
    #     print(f"V{mum}_{ii}")
    # synchroniesiert die Internen Maschinendaten
    # converter_1.sync_interns()


    #erstellen von Kraftschrieb

    # for ii in range(len(os.listdir(output_folder_pkl_1)) - 1):
    #     converter_1.cut_Peaks_forces(ii,output_folder_pkl_1)
    #     print(f"V{i}_{ii}")


    # converter_1.cut_Peaks_forces(1,output_folder_pkl_1)







# muss noch mit V03 durchlaufen
#erstellen von "Hioki_Strom"
    # a=[]
    # for d in os.listdir(output_folder_pkl_1):
    #     if d.endswith(".pkl"):
    #         a.append(d)
    # for ii in range((len(a)) - 1):
    #     cut=converter_1.cut_1_LM(ii, output_folder_pkl_1, output_folder_pkl_cuts_1)
    #     print(f"V{mum}_{ii}")




    #schneidet die Peaks der Kraftschriebe aus
    # for ii in range(len(os.listdir(output_folder_pkl_1))-1):
    #     folder = converter_1.cut_Peaks_forces_tooth(ii, output_folder_pkl_cuts_1 + "Forces\\",output_folder_pkl_cuts_1 + "Forces\\peaks_only\\")
    #     converter_1.plot_tooth(folder,output_folder_pkl_cuts_1+"Forces\\peaks_only\\")
    #     print(ii)
    # print("________"+str(i)+"_________")



# for i in range(len(os.listdir(output_folder_pkl_1))-1):
#     converter_1.cut_Peaks_forces(i,output_folder_pkl_1)
#     converter_1.plot_pkl(i,output_folder_pkl_cuts_1 + "Forces\\",output_folder_pkl_cuts_1 + "Forces\\")
#     print(i)
# converter_1.plot_pkl(i,output_folder_pkl_cuts_1 + "Forces\\",output_folder_pkl_cuts_1 + "Forces\\")

# converter_1.cut_Peaks_forces(143,output_folder_pkl_1)
# converter_1.plot_pkl(143,output_folder_pkl_cuts_1 + "Forces\\",output_folder_pkl_cuts_1 + "Forces\\")