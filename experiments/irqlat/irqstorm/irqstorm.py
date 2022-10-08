#!/usr/bin/python3

import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from functools import reduce
import sys

palette=sns.color_palette("tab20c")

hyp_label = "hyp"
hypervisors = [
    "baremetal",
    "jailhouse",
    "xen",
    "bao",
    "sel4",
]

test_label = "test"
tests = [
    "",
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

colors = [
    ("tab:cyan", 1),
    ("tab:orange", 1),
    ("tab:green", 1),
    ("tab:blue", 1),
    ("tab:red", 1)
]
colors = [[lighten_color(c, 1/(i/4+1))] for (c, r) in colors for i in range(0,r)]
colors = reduce(lambda x, y: x + y, colors)

fig_count = int(math.ceil(math.sqrt(len(metrics))))
fig_count = fig_count*100 + fig_count*10

def hyp_frame(hyp):
    try:
        file = open(hyp)
    except FileNotFoundError:
        return pd.DataFrame([])

    separators = []
    lines = []
    for i, line in enumerate(file.readlines()):
        stripped_line = line.strip()
        lines.append(stripped_line.split())
        print(len(stripped_line))
        if len(stripped_line) !=0 and all(c == stripped_line[0] for c in stripped_line):
            separators.append(i)
    separators.append(len(lines))
    print(separators)
    columns=lines[separators[0]+1]
    data=np.matrix(lines[separators[0]+2:])
    frame = pd.DataFrame(data=data.astype(float), columns=columns)
    # for s, e in zip(separators, separators[1:]):
    #     data = np.array(lines[s+1:e])
    #     frame = pd.concat([frame, pd.DataFrame(data=data[3:,:].astype(float), columns=data[0,:])], axis=1)

    frame = frame.melt(var_name='iter')
    frame[hyp_label] = [hyp] * len(frame)
    return frame

frames = pd.concat([hyp_frame(hyp) for hyp in hypervisors])
# frames = frames.loc[:,~frames.columns.duplicated()]
frames['value'] = frames['value']*10

print(frames)
# ########################################

fig = plt.figure(figsize=(6,3))
hart = sns.barplot(data=frames, x='iter', y="value", hue=hyp_label, edgecolor='black', errwidth = 1.5, palette=colors)
plt.legend().set_title(None)
plt.xlabel(None)
plt.ylabel('Interrupt Latency (ns)')
# plt.yscale("log")
# plt.ylim(top=11**5)
plt.subplots_adjust(left=0.14, right=0.995, top=0.990, bottom=0.1)
plt.grid(which='both', axis='y', linestyle='--')

plt.show()
