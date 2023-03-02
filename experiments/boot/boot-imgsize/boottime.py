#!/bin/python3

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import scipy as sp
import numpy as np
from os import path
from functools import reduce
from glob import glob
import re

def lighten_color(color, amount=0.5):
    import matplotlib.colors as mc
    import colorsys
    c = mc.to_rgb(color)
    c = colorsys.rgb_to_hls(*mc.to_rgb(c))
    return colorsys.hls_to_rgb(c[0], 1 - amount * (1 - c[1]), c[2])


hypervisors = [
    'jailhouse',
    'xen',
    'bao',
    'sel4',
]

size_dict = {
    'k': 1024, 'K': 1024, 'm': 1024*1024, 'M': 1024*1024, 'g': 1024*1024*1024, 'G': 1024*1024*1024
}
    

def get_boot_data(hyp):
    df = pd.DataFrame(columns=['size', 'stage', 'time'])
    for filename in glob(hyp + '-*'):
        b, e = re.search(hyp + '-([0-9]*)([k|K|m|M|G|g])', filename).groups()
        sz = (int(b)*size_dict[e])/1024
        file = open(filename, 'r', encoding='latin-1')
        contents = file.read()
        for r in re.findall('boottime-(.*) ([0-9]*)', contents):
            stage = r[0]
            time = int(r[1]) * 10 / 10**6
            df = pd.concat([df, pd.DataFrame([[sz, stage, time]], columns=['size', 'stage', 'time'])], ignore_index=True)
    
    df = pd.pivot_table(df, values='time',  index='size', columns=['stage'])
    df = df.reindex(df.mean().sort_values().index, axis=1)
    labels = ['fsbl'] + list(df.columns.values[:-1])
    labels = [l.replace('hyp', hyp) for l in labels]
    df.set_axis(labels, axis=1, inplace=True)
    return df
        

############################################################################

colors = [
    [("#BDEBEB", 1), ("#9673A6",1),("#D6B656", 1),("tab:orange", 2),],
    [("#BDEBEB", 1), ("#9673A6",1),("#D6B656", 1),("tab:green", 1),],
    [("#BDEBEB", 1), ("#9673A6",1),("#D6B656", 1),("tab:blue", 1),],
    [("#BDEBEB", 1), ("#9673A6",1),("#D6B656", 1),("tab:red", 3),],
]

# for j, hyp in enumerate(hypervisors):
#     file = 'vmsize/' + hyp
#     palete = [[lighten_color(c, 1/(i/4+1))] for (c, r) in colors[j] for i in range(0,r)]
#     palete = reduce(lambda x, y: x + y, palete)
#     if not path.exists(file):
#         continue
#     data = pd.read_csv(file)
#     data = data.melt(id_vars=['size'])
#     fig = plt.figure(figsize=(4,3))
#     fig.canvas.set_window_title(hyp)
#     plt.tight_layout()
#     ax = sns.lineplot(data=data, x='size', y='value', hue='variable', marker='o', palette=palete)
#     # ax.set_xscale('log')
#     ax.get_xaxis().get_major_formatter().set_scientific(False)
#     plt.grid(which='both', axis='x', linestyle='--')
#     plt.grid(which='both', axis='y', linestyle='--')
#     plt.ylim(0, 7000)
#     plt.legend().remove()
#     plt.subplots_adjust(left=0.2, right=0.995, top=0.990, bottom=0.05)
#     plt.ylabel(None)
#     plt.xlabel(None)
#     ax.set_xticklabels([])
#     ax.set_yticklabels([])
#     # plt.ylabel('Time (ms)')
#     # plt.xlabel('VM Image Size (KiB)')
#     plt.tight_layout()
#     # if j == 1 or j == 3:
#     #     ax.axes.yaxis.set_ticklabels([])
#     #     ax.axes.yaxis.label.set_visible(False)
#     # if j == 0 or j == 1:
#     #     ax.axes.xaxis.set_ticklabels([])
#     #     ax.axes.xaxis.label.set_visible(False)

############################################################################

plt.figure(figsize=(8,6))

for j, hyp in enumerate(hypervisors):
    print(hyp)
    
    palete = [[lighten_color(c, 1/(i/4+1))] for (c, r) in colors[j] for i in range(0,r)]
    palete = reduce(lambda x, y: x + y, palete)

    # file = 'imgsize/' + hyp
    # if not path.exists(file):
    #     continue
    # data = pd.read_csv(file)
    data = get_boot_data(hyp)
    print(data)
    data = data.melt(ignore_index=False)
    print(data)
    # fig = plt.figure(figsize=(4,3))
    plt.subplot(2,2, j+1)
    # fig.canvas.set_window_title(hyp)
    plt.tight_layout()
    ax = sns.lineplot(data=data, x='size', y='value', hue='variable', style="variable", markers=True, palette=palete)
    # ax.set_xscale('log')
    ax.get_xaxis().get_major_formatter().set_scientific(False)
    if hyp == 'sel4':
        hyp = 'sel4/camkes-vmm'
    # ax.set_title(hyp)
    plt.grid(which='both', axis='x', linestyle='--')
    plt.grid(which='both', axis='y', linestyle='--')
    plt.ylim(0, 13500)
    # plt.legend().remove()
    plt.legend(loc='upper left', ncol=2).set_title(None)
    plt.subplots_adjust(left=0.2, right=0.995, top=0.990, bottom=0.05)
    plt.ylabel('Time (ms)')
    plt.xlabel('VM Image Size (MiB)')

    if j == 1 or j == 3:
        ax.axes.yaxis.set_ticklabels([])
        ax.axes.yaxis.label.set_visible(False)
    if j == 0 or j == 1:
        ax.axes.xaxis.set_ticklabels([])
        ax.axes.xaxis.label.set_visible(False)

plt.tight_layout()

############################################################################

# plt.figure(figsize=(8,6))

# for j, hyp in enumerate(hypervisors):
#     file = 'imgsize-dual/' + hyp
#     palete = [[lighten_color(c, 1/(i/4+1))] for (c, r) in colors[j] for i in range(0,r)]
#     palete = reduce(lambda x, y: x + y, palete)
#     if not path.exists(file):
#         continue
#     data = pd.read_csv(file)
#     data = data.melt(id_vars=['size'])
#     # fig = plt.figure(figsize=(4,3))
#     plt.subplot(2,2, j+1)
#     # fig.canvas.set_window_title(hyp)
#     plt.tight_layout()
#     ax = sns.lineplot(data=data, x='size', y='value', hue='variable', marker='o', palette=palete)
#     # ax.set_xscale('log')
#     ax.get_xaxis().get_major_formatter().set_scientific(False)
#     ax.set_title(hyp)
#     plt.grid(which='both', axis='x', linestyle='--')
#     plt.grid(which='both', axis='y', linestyle='--')
#     plt.ylim(0, 10000)
#     plt.legend().remove()
#     plt.subplots_adjust(left=0.2, right=0.995, top=0.990, bottom=0.05)
#     plt.ylabel('Time (ms)')
#     plt.xlabel('VM Image Size (KiB)')
#     # plt.ylabel(None)
#     # plt.xlabel(None)
#     # ax.set_xticklabels([])
#     # ax.set_yticklabels([])

    
#     if j == 1 or j == 3:
#         ax.axes.yaxis.set_ticklabels([])
#         ax.axes.yaxis.label.set_visible(False)
#     if j == 0 or j == 1:
#         ax.axes.xaxis.set_ticklabels([])
#         ax.axes.xaxis.label.set_visible(False)

# plt.tight_layout()

############################################################################


# colors = [
#     ("tab:orange", 1),
#     ("tab:green", 1),
#     ("tab:blue",1),
#     ("tab:red", 1)
# ]
# colors = [[lighten_color(c, 1/(i/4+1))] for (c, r) in colors for i in range(0,r)]
# colors = reduce(lambda x, y: x + y, colors)

# # plt.figure(figsize=(6,4))
# # data = pd.read_csv('vmsize/hyps')
# # data = data.melt(id_vars=['size'])
# # print(data)
# # ax = sns.lineplot(data=data, x='size', y='value', hue='variable', marker='o', palette=colors)
# # # # ax.set_xscale('log')
# # ax.get_xaxis().get_major_formatter().set_scientific(False)
# # plt.grid(which='both', axis='x', linestyle='--')
# # plt.grid(which='both', axis='y', linestyle='--')
# # plt.legend().set_title(None)
# # plt.ylabel('Time (ms)')
# # plt.xlabel('VM Memory Size (KiB)')
# # plt.subplots_adjust(left=0.13, right=0.990, top=0.990, bottom=0.15)

# plt.figure(figsize=(6,2))
# data = pd.read_csv('imgsize/hyps')
# data = data.melt(id_vars=['size'])
# print(data)
# ax = sns.lineplot(data=data, x='size', y='value', hue='variable', marker='o', palette=colors)
# # # ax.set_xscale('log')
# plt.grid(which='both', axis='x', linestyle='--')
# plt.grid(which='both', axis='y', linestyle='--')
# plt.legend().set_title(None)
# plt.legend().remove()
# plt.ylabel('Time (ms)')
# plt.xlabel('VM Image Size (KiB)')
# plt.tight_layout()
# plt.subplots_adjust(left=0.11, right=0.995, top=0.999, bottom=0.25)

############################################################################

plt.show()
