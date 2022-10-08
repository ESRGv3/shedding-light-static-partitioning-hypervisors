#!/usr/bin/python3

import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from functools import reduce
import copy

palette=sns.color_palette("tab20c")

hyp_label = "hyp"
hypervisors = [
    "jailhouse",
    "bao",
]

test_label = "test"
tests = [
    "solo",
    "col",
    "interf",
    "interf+col",
    "interf+col+hypcol"
]

metrics = [
    ["irqlat"],
]


def lighten_color(color, amount=0.5):
    import matplotlib.colors as mc
    import colorsys
    c = mc.to_rgb(color)
    c = colorsys.rgb_to_hls(*mc.to_rgb(c))
    return colorsys.hls_to_rgb(c[0], 1 - amount * (1 - c[1]), c[2])

colors_base = [
    ("tab:orange", 1),
    ("tab:blue", 1),
]
colors = [[lighten_color(c, 1/(i/4+1))] for (c, r) in colors_base for i in range(0,r)]
colors = reduce(lambda x, y: x + y, colors)
colors_attenuated = [[lighten_color(c, 0.2)] for (c, r) in colors_base for i in range(0,r)]
colors_attenuated = reduce(lambda x, y: x + y, colors_attenuated)


fig_count = int(math.ceil(math.sqrt(len(metrics))))
fig_count = fig_count*100 + fig_count*10

def hyp_frame(hyp, test):
    try:
        file = open(hyp + "+" + test)
    except FileNotFoundError:
        return pd.DataFrame([])

    separators = []
    lines = []
    file.readline() # skip first line
    for i, line in enumerate(file.readlines()):
        stripped_line = line.strip()
        lines.append(stripped_line.split())
        if len(line) == 0 or all(c == line[0] for c in stripped_line):
            separators.append(i)
    separators.append(len(lines))
    lines=lines[:-1]

    data = np.array(lines[0:separators[0]])
    frame = pd.DataFrame(data=data[1:].astype(float), columns=data[0])
    for s, e in zip(separators, separators[1:]):
        data = np.array(lines[s+1:e])
        frame = pd.concat([frame, pd.DataFrame(data=data[1:].astype(float), columns=data[0])], axis=1)

    frame[hyp_label] = [hyp] * len(frame)
    frame[test_label] = [test] * len(frame)
    return frame


tests = [(hyp, test) for test in tests for hyp in hypervisors]
frames = pd.concat([hyp_frame(hyp, test) for (hyp,test) in tests])
frames = frames.loc[:,~frames.columns.duplicated()]
frames['irqlat'] = frames['irqlat']*10

########################################

frames_base = frames

fig = plt.figure(figsize=(6,3))
background_columns=copy.deepcopy(frames_base)
background_columns['irqlat'] = 1000000
ax1 = sns.barplot(data=background_columns, x=test_label, y="irqlat", palette=colors_attenuated, hue=hyp_label)
ax2 = sns.violinplot(data=frames_base, x=test_label, y="irqlat", hue=hyp_label, scale="width", palette=colors)
plt.legend(loc = 'upper left').set_title(None)
plt.xlabel(None)
plt.ylim(0,3300)
plt.ylabel('Interrupt Latency (ns)')
handles, labels = ax2.get_legend_handles_labels()
plt.legend(handles[:2], labels[:2], loc = 'upper left', ).set_title(None)
plt.subplots_adjust(left=0.13, right=0.995, top=0.990, bottom=0.1)
plt.grid(which='both', axis='y', linestyle='--')

df = frames[(frames['test'] == 'solo')][['hyp', 'irqlat']]
print(df.pivot_table(index=df.index, columns='hyp', values='irqlat', aggfunc='first').mean())

df = frames[(frames['test'] == 'interf')][['hyp', 'irqlat']]
print(df.pivot_table(index=df.index, columns='hyp', values='irqlat', aggfunc='first').mean())

df = frames[(frames['test'] == 'interf+col')][['hyp', 'irqlat']]
print(df.pivot_table(index=df.index, columns='hyp', values='irqlat', aggfunc='first').mean())

plt.show()
