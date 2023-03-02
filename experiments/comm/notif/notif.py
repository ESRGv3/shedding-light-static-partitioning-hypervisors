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
    # "baremetal",
    "jailhouse",
    "xen",
    "bao",
    "sel4",
]

test_label = "test"
tests = [
    "",
    "+col",
    "+interf",
    "+interf+col",
    "+interf+col+hypcol"
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
    # ("tab:cyan", 1),
    ("tab:orange", 1),
    ("tab:green", 1),
    ("tab:blue", 1),
    ("tab:red", 1)
]
colors = [[lighten_color(c, 1/(i/4+1))] for (c, r) in colors_base for i in range(0,r)]
colors = reduce(lambda x, y: x + y, colors)
colors_attenuated = [[lighten_color(c, 0.2)] for (c, r) in colors_base for i in range(0,r)]
colors_attenuated = reduce(lambda x, y: x + y, colors_attenuated)


fig_count = int(math.ceil(math.sqrt(len(metrics))))
fig_count = fig_count*100 + fig_count*10

def hyp_frame(hyp, test):
    try:
        file = open(hyp + test)
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
    lines=lines

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

################################################

frames_base = frames

fig = plt.figure(figsize=(6,3))
plt.grid(which='both', axis='y', linestyle='--')
cap_width = 1 / (len(test_label)*2.5)
background_columns=copy.deepcopy(frames_base)
background_columns['irqlat'] = 1000000
ax1 = sns.barplot(data=background_columns, x=test_label, y="irqlat", palette=colors_attenuated, hue=hyp_label)
# ax1.legend([])
ax2 = sns.violinplot(data=frames_base, x=test_label, y="irqlat", palette=colors, hue=hyp_label, scale="width", linewidth=0.5)

plt.ylim(0,63000)
plt.yticks(np.arange(0,62000,5000))
handles, labels = ax2.get_legend_handles_labels()
plt.legend(handles[:4], labels[:4], loc = 'upper left', ).set_title(None)
plt.xlabel(None)
# plt.xticks([])
plt.ylabel('Notification Latency (ns)')
# plt.subplots_adjust(left=0.13, right=0.995, top=0.990, bottom=0.01)

# ################################################

# frames_base = frames[frames['test'] == 'base']

# fig = plt.figure(figsize=(6,3))
# # plt.yticks(np.arange(0,10000,1000))
# plt.grid(which='both', axis='y', linestyle='--')
# cap_width = 1 / (len(test_label)*2.5)
# chart = sns.violinplot(data=frames_base, x=test_label, y="irqlat", palette=colors, hue=hyp_label, scale="width")
# plt.legend(loc = 'upper left').set_title(None)
# plt.xlabel(None)
# plt.xticks([])
# plt.ylabel('Interrupt Latency (ns)')
# # plt.subplots_adjust(left=0.13, right=0.995, top=0.990, bottom=0.01)

# # ################################################

# frames_base = frames[frames['test'] == 'interf']

# fig = plt.figure(figsize=(6,3))
# # plt.yticks(np.arange(0,10000,1000))
# plt.grid(which='both', axis='y', linestyle='--')
# cap_width = 1 / (len(test_label)*2.5)
# chart = sns.violinplot(data=frames_base, x=test_label, y="irqlat", palette=colors, hue=hyp_label, scale="width")
# plt.legend(loc = 'upper left').set_title(None)
# plt.xlabel(None)
# plt.xticks([])
# plt.ylabel('Interrupt Latency (ns)')
# # plt.subplots_adjust(left=0.13, right=0.995, top=0.990, bottom=0.01)

###########################################


## NOT USED IN THE PAPER

# metrics = [
#     ["exceptions_el1", "exceptions_el2", "irqs_el1", "irqs_el2"],
#     ["l1$i_miss_el1", "l1$i_miss_el2", "l1$d_miss_el1", "l1$d_miss_el2", "l2$d_miss_el1", "l2$d_miss_el2" ],
#     ["tlb_il1_miss_el1", "tlb_il1_miss_el2", "tlb_dl1_miss_el1", "tlb_dl1_miss_el2"],
#     ["bus_acc_el1", "bus_acc_el2"],
# ]

# def dimensions(n, max=8):
#     max_width = 4
#     l = 2
#     while True:
#         for w in range(1, max_width+1):
#             if n <= l*w:
#                 return (l, w)
#         l += 1

# for metrics in metrics:
#     fig = plt.figure()
#     fig_count = int(math.ceil(math.sqrt(len(metrics))))
#     fig_count = fig_count*100 + fig_count*10
#     fig_count=1
#     fig_l,fig_w = dimensions(len(metrics))
#     for metric in metrics:
#         frames_melted = pd.melt(frames, id_vars=[hyp_label, test_label], value_vars=metric)
#         ax = plt.subplot(fig_l,fig_w,fig_count)
#         plt.grid(which='both', axis='y', linestyle='--')
#         cap_width = 1 / (len(test_label)*2.5)
#         chart = sns.barplot(data=frames_melted, x=test_label, y='value', hue=hyp_label, edgecolor='black', errwidth = 1.5, palette=colors, capsize = cap_width)
#         plt.legend(loc = 'upper left').set_title(None)
#         plt.xlabel(None)
#         plt.xticks(None)
#         plt.title(metric)
#         plt.grid()
#         plt.tight_layout()
#         fig_count += 1

plt.show()
