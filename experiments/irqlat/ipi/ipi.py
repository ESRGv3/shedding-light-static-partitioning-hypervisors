#!/usr/bin/python3

import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from functools import reduce
import sys

hyp_label = "hyp"
hypervisors = [
    "baremetal",
    "jailhouse",
    "xen",
    "bao",
    "sel4",
]

colors = [
    ("tab:cyan", 1),
    ("tab:orange", 1),
    ("tab:green", 1),
    ("tab:blue", 1),
    ("tab:red", 1)
]

def hyp_frame(hyp, file):

    if len(file) == 0:
        return  pd.DataFrame()

    separators = []
    lines = []
    file = file[1:] # skip first line
    for i, line in enumerate(file):
        stripped_line = line.strip()
        lines.append(stripped_line.split())
        if len(line) == 0 or all(c == line[0] for c in stripped_line):
            separators.append(i)
    separators.append(len(lines))
    lines = lines

    data = np.array(lines[0:separators[0]-1])
    frame = pd.DataFrame(data=data[2:,:].astype(float), columns=data[0,:])
    for s, e in zip(separators, separators[1:]):
        data = np.array(lines[s+1:e])
        frame = pd.concat([frame, pd.DataFrame(data=data[4:,:].astype(float), columns=data[0,:])], axis=1)

    frame[hyp_label] = [hyp] * len(frame)

    return frame

def separate_file(hyp):
    try:
        file = open(hyp)
    except:
        return ([], [])
    lines = file.readlines()
    separator = next((n+1 for (n, line) in enumerate(lines) if line.find("TARGET") >= 0))
    return (lines[:separator-1], lines[separator:-1])

def extract_col(frame, hyp, column):
    frame = frame[frame['hyp'] == hyp]
    values = frame[column].values.flatten() * 10
    return values[~np.isnan(values)]

(files) = [(hyp, separate_file(hyp)) for hyp in hypervisors]

trap_frames = pd.concat([hyp_frame(hyp, contents) for (hyp, (contents, _)) in files])
lat_frames =  pd.concat([hyp_frame(hyp, contents) for (hyp, (_, contents)) in files])

plt.figure(figsize=(6,2.5))
full_frame = pd.DataFrame()
for hyp in hypervisors:
    sgi_lat = extract_col(trap_frames, hyp, 'sgi-lat')
    trap_lat = extract_col(trap_frames,  hyp, 'trap-lat')
    ipi_lat = extract_col(lat_frames,  hyp, 'ipi-lat')
    frame = pd.DataFrame([sgi_lat, trap_lat, ipi_lat], index=["sgi-lat", "trap-lat", "ipi-lat"]).transpose()
    frame[hyp_label] = [hyp] * len(frame)
    full_frame = full_frame.append(frame)

full_frames_melted = pd.melt(full_frame, id_vars=[hyp_label], value_vars=["sgi-lat", "trap-lat", "ipi-lat"])

colors = ["tab:cyan", "tab:orange", "tab:green", "tab:blue", "tab:red"]
sns.barplot(data=full_frames_melted, x='variable', y="value", hue='hyp', edgecolor='black', errwidth = 1.5, palette=colors)

plt.grid(which='both', axis='y', linestyle='--')
plt.legend(loc = 'upper left').set_title(None)
plt.xlabel(None)
plt.xticks([0,1,2,], ["Emulation", "Trap", "IPI"])
plt.ylabel('Time (ns)')
plt.subplots_adjust(left=0.125, right=0.995, top=0.995, bottom=0.085)



plt.show()
