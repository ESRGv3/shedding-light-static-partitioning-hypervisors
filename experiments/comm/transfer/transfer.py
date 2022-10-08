#! /usr/bin/python3

import re
import numpy as np
import pandas as pd
import matplotlib as mplt
import matplotlib.pyplot as plt
import seaborn as sns
import math
from functools import *

hypervisors = [
    "jailhouse",
    "xen",
    "bao",
    "sel4",
]

scenarios = [
    None,
    "col",
    "interf", #1cpu/2Mcache
    "interf2", #2cpu/2Mcache
    "interf-col",
    "interf-col-hypcol",
]

# interf_tests = [
#     "interf-tests/interf1", #2cpus/2Mcache
#     "interf-tests/interf2",#2cpus/1Mcache
#     "interf-tests/interf3", #1cpu/2Mcache
#     "interf-tests/interf4", #1cpu/1Mcache
#     "interf-tests/interf5", #1cpu/4Mcache
#     "interf-tests/interf6", #1cpu/8Mcache
#     "interf-tests/interf7", #2cpu/4Mcache
# ]

def lighten_color(color, amount=0.5):
    import matplotlib.colors as mc
    import colorsys
    c = mc.to_rgb(color)
    c = colorsys.rgb_to_hls(*mc.to_rgb(c))
    return colorsys.hls_to_rgb(c[0], 1 - amount * (1 - c[1]), c[2])


colors = [
    ("tab:orange", 1),
    ("tab:green", 1),
    ("tab:blue", 1),
    ("tab:red", 1)
]
colors = [[lighten_color(c, 1/(i/4+1))] for (c, r) in colors for i in range(0,r)]
colors = reduce(lambda x, y: x + y, colors)


def header_array(line):
    sizedict = {'K': 1024, 'M': 1024**2}
    return [float(size)*sizedict[base] for (size, base) in re.findall("([0-9]+)(K|M)",line)]

def hyp_frames(hyp, scn):
    filename = hyp
    if scn is not None:
        filename += '+' + scn
    else:
        scn = 'base'
    print(filename)
    try:
        file = open(filename)
    except:
        print(f'file \'{filename}\' does not exist!')
        return pd.DataFrame()

    def frames_from_tables(tables):
        for test, transfersize, metric, table in tables:
            lines = table.splitlines()
            header = lines[0].split()
            data = np.array([line.split() for line in lines[1:]]).astype(float)
            header = header_array(lines[0])
            df = pd.DataFrame(columns=header, data=data)
            df['test'] = [test.strip()] * len(df)
            df['transfersize'] = [transfersize] * len(df)
            df['hyp'] = [hyp] * len(df)
            df['scenario'] = [scn] * len(df)
            yield df

    tables = re.findall('<-(.*), ?(.*), ?(.*)\n([\S\s]*?)->', file.read())
    return pd.concat(frames_from_tables(tables))

data = pd.concat((hyp_frames(hyp, scn) for hyp in hypervisors for scn in scenarios))
data = data.melt(id_vars=['hyp', 'test', 'transfersize', 'scenario'], var_name=['bufsize'], value_name='time')
data['time'] *= 10 # compensate for timer resolution
print(data)

def dimensions(n, max=8):
    max_width = 4
    l = 2
    while True:
        for w in range(1, max_width+1):
            if n <= l*w:
                return (l, w)
        l += 1



####################################################################################

# buf_sizes= data['bufsize'].unique()
# ylim = 30000000

# plt.figure()
# plt.suptitle("interrupt")
# fig_count = int(math.ceil(math.sqrt(len(buf_sizes))))
# fig_count = fig_count*100 + fig_count*10
# fig_count=1
# fig_l,fig_w = dimensions(len(buf_sizes))
# for bufsize in buf_sizes:
#     ax = plt.subplot(fig_l,fig_w,fig_count)
#     fig_count += 1
#     bufdata = data[data['bufsize'] == bufsize]
#     sns.lineplot(bufdata[bufdata['test'] == 'interrupt'], x='transfersize', y='time', hue='hyp', style='hyp',markers=True)
#     plt.title(bufsize)
#     plt.xscale("log")
#     plt.ylim(top=ylim)

# plt.figure()
# plt.suptitle("polling")
# fig_count = int(math.ceil(math.sqrt(len(buf_sizes))))
# fig_count = fig_count*100 + fig_count*10
# fig_count=1
# fig_l,fig_w = dimensions(len(buf_sizes))
# for bufsize in buf_sizes:
#     ax = plt.subplot(fig_l,fig_w,fig_count)
#     fig_count += 1
#     bufdata = data[data['bufsize'] == bufsize]
#     sns.lineplot(bufdata[bufdata['test'] == 'polling'], x='transfersize', y='time', hue='hyp', style='hyp', markers=True)
#     plt.title(bufsize)
#     plt.xscale("log")
#     plt.ylim(top=ylim)

####################################################################################

# data=data[(data['bufsize'] == '16M')]
transfersizes= data['transfersize'].unique()
transfersize=16*1024**2
data['thruput'] = (transfersize / (data['time'] * 0.000000001)) / 1024**2



plt.figure(figsize=(8,6))
# plt.suptitle("interrupt")
fig_count = int(math.ceil(math.sqrt(len(transfersizes)*4)))
fig_count = fig_count*100 + fig_count*10
fig_count=1
fig_l,fig_w = dimensions(len(transfersizes)*4)

xticks=[2**x for x in range(10, 24)]
ylim = 1550
yticks=range(0, ylim, 250)

ax = plt.subplot(fig_l,fig_w,fig_count)
plt.tight_layout()
fig_count += 1
bufdata = data[data['transfersize'] == '16M']
bufdata = bufdata[bufdata['scenario'] == 'base']
ax = sns.lineplot(bufdata[bufdata['test'] == 'polling'], x='bufsize', y='thruput', hue='hyp', style='hyp', palette=colors, markers=True, legend=True)
plt.xscale("log")
plt.ylim(15, top=ylim)
plt.xlabel(None)
plt.ylabel(None)
plt.yticks(yticks)
plt.xticks([])
plt.legend(loc = 'lower left').set_title(None)
plt.grid(which='both', axis='both', linestyle='--')
plt.ylabel("Throughput (MiB/s)")
ax2 = ax.twiny()
ax2.xaxis.set_label_position("top")
ax2.set_xlabel("No Interference")
ax2.set_xticks([])
plt.subplots_adjust(left=0.2, right=0.995, top=0.990, bottom=0.05)

ax = plt.subplot(fig_l,fig_w,fig_count)
plt.tight_layout()
fig_count += 1
bufdata = data[data['transfersize'] == '16M']
bufdata = bufdata[bufdata['scenario'] == 'interf']
ax = sns.lineplot(bufdata[bufdata['test'] == 'polling'], x='bufsize', y='thruput', hue='hyp', style='hyp', palette=colors, markers=True, legend=False)
plt.xscale("log")
plt.ylim(15, top=ylim)
plt.xlabel(None)
plt.ylabel(None)
plt.yticks(yticks)
plt.xticks([])
ax.yaxis.set_ticklabels([])
plt.grid(which='both', axis='both', linestyle='--')
ax2 = ax.twinx()
ax2.yaxis.set_label_position("right")
ax2.set_ylabel("Polling")
ax2.set_yticks([])
ax2 = ax.twiny()
ax2.xaxis.set_label_position("top")
ax2.set_xlabel("Interference")
ax2.set_xticks([])
plt.subplots_adjust(left=0.2, right=0.995, top=0.990, bottom=0.05)

ax = plt.subplot(fig_l,fig_w,fig_count)
plt.tight_layout()
fig_count += 1
bufdata = data[data['transfersize'] == '16M']
bufdata = bufdata[bufdata['scenario'] == 'base']
ax = sns.lineplot(bufdata[bufdata['test'] == 'interrupt'], x='bufsize', y='thruput', hue='hyp', style='hyp', palette=colors, markers=True, legend=False)
plt.xscale("log")
plt.ylim(15, top=ylim)
plt.xlabel(None)
plt.ylabel(None)
plt.yticks(yticks)
plt.grid(which='both', axis='both', linestyle='--')
plt.ylabel("Throughput (MiB/s)")
plt.xlabel("Buffer Size (MiB)")
plt.subplots_adjust(left=0.2, right=0.995, top=0.990, bottom=0.05)

ax = plt.subplot(fig_l,fig_w,fig_count)
plt.tight_layout()
fig_count += 1
bufdata = data[data['transfersize'] == '16M']
bufdata = bufdata[bufdata['scenario'] == 'interf']
ax = sns.lineplot(bufdata[bufdata['test'] == 'interrupt'], x='bufsize', y='thruput', hue='hyp', style='hyp', palette=colors, markers=True, legend=False)
plt.xscale("log")
plt.ylim(15, top=ylim)
plt.xlabel(None)
plt.ylabel(None)
plt.yticks(yticks)
ax.yaxis.set_ticklabels([])
plt.grid(which='both', axis='both', linestyle='--')
plt.xlabel("Buffer Size (MiB)")
ax2 = ax.twinx()
ax2.yaxis.set_label_position("right")
ax2.set_ylabel("Interrupt")
ax2.set_yticks([])
plt.subplots_adjust(left=0.2, right=0.995, top=0.990, bottom=0.05)

# # ####################################################################################

plt.tight_layout()
plt.show()
