#!/usr/bin/python3


import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
import re
from os import path
import sys
from functools import *
import colorsys

base = [
    "jailhouse",
    "xen",
    "bao",
    "sel4"
]


benchs = [
    "qsort-small",
    "qsort-large",
    "susanc-small",
    "susanc-large",
    "susane-small",
    "susane-large",
    "susans-small",
    "susans-large",
    "bitcount-small",
    "bitcount-large",
    "basicmath-small",
    "basicmath-large",
]

base_case = "baremetal"

def process_benchmark(directory, hyp, base=None):
    file = directory + "/" +  hyp
    if not path.exists(file):
        return None
    for l in open(file, 'r'):
        l =l.strip()
        r = re.search('-> mibench/.*/.*',l)
        if r is not None:
            (m,s,b) = l.split('/')
            bench = b
            continue
        r = re.search('\d*\.\d* \(', l)
        if r is not None:
            (s,e) = r.span()
            val = float(l[s:e-2])
            if base is not None:
                val /= base[bench]
                val -= 1.0
                val *= 100
            yield [hyp, bench, val]


hypervisors=base

def lighten_color(color, amount=0.5):
    import matplotlib.colors as mc
    import colorsys
    c = mc.to_rgb(color)
    c = colorsys.rgb_to_hls(*mc.to_rgb(c))
    return colorsys.hls_to_rgb(c[0], 1 - amount * (1 - c[1]), c[2])

event_map = {
    'r08': 'inst_ret',

    'r02': 'itlb_l1_refill',
    'r05': 'dtlb_l1_refill',

    'r14': 'icache_l1',
    'r01': 'icache_l1_refill',

    'r04': 'dcache_l1',
    'r03': 'dcache_l1_refill',
    'r15': 'dcache_l1_wb',

    'r16': 'dcache_l2',
    'r17': 'dache_l2_refill',
    'r18': 'dcache_l2_wb',

    'r13': 'mem_access',
    'r19': 'bus_access',
    'r1d': 'bus_cyles',

    're7': 'stall_ldmiss',
    're8': 'stall_wrmiss',

    'r09': 'exc_taken',
    'r86': 'exc_irq',
    'r87': 'exc_fiq',
}



# ## base mibench ###############################################################
directory = "mibench-base"

colors = [
    ("tab:orange", 1),
    ("tab:green", 1),
    ("tab:blue", 1),
    ("tab:red", 1)
]
colors = [[lighten_color(c, 1/(i/4+1))] for (c, r) in colors for i in range(0,r)]
colors = reduce(lambda x, y: x + y, colors)

base = [[bench, val] for [_, bench, val] in process_benchmark(directory,base_case)]
base = pd.DataFrame(base, columns = ['bench', 'val'])
base = {b: float(base[base['bench'] == b].mean()) for b in base['bench'].unique()}

frames = [f for h in hypervisors for f in process_benchmark(directory,h, base)]
frames = pd.DataFrame(frames, columns = ['hyp', 'bench', 'val'])
frames = frames[[x in benchs for x in frames['bench']]]

fig = plt.figure(figsize=(12,3))
fig.canvas.manager.set_window_title(directory)
bp = sns.barplot(data=frames,x='bench', y='val', hue='hyp', edgecolor='black', palette=colors, errwidth = 1, capsize=0.1)
plt.xlabel(None)
plt.ylabel('% Perforance Degradation')
plt.xticks(None)
_, labels = plt.xticks()
labels = [l.get_text().replace('-','\n') for l in labels]
plt.xticks(np.arange(len(labels)), labels)
# plt.xticks(rotation=90)
plt.legend(loc = 'upper right').set_title(None)
# plt.legend(bbox_to_anchor =(0.65, 1.25)).set_title(None)
# plt.ylim(bottom=1.0)
plt.grid(which='both', axis='y', linestyle='--')
plt.yticks(np.arange(0,9,1))
plt.tight_layout()
# plt.get_current_fig_manager().window.showMaximized()

hyp_events = []
for hyp in hypervisors:
    file = directory + "/" +  hyp
    if not path.exists(file):
        continue
    events = open(file,'r')
    for line in events:
        line = line.strip()
        r = re.search('-> mibench/*', line)
        if r is not None:
            bench = r.string
            continue
        r = re.search('[0-9]+ *r[0-9A-Fa-f]+(:[ukh]+)?', line)
        if r is not None:
            (s, e) = r.span()
            (count, rawevent) = r.string[:e].split()
            if rawevent.find(':') >= 0:
                (event, level) = rawevent.split(':')
            else:
                event = rawevent
                level = 'ukh'
            event = event_map[event] + ':' + level
            bench_text = bench.removeprefix("-> mibench/")
            bench_text = bench_text[bench_text.find('/')+1:]
            hyp_events.append([hyp, bench_text, event, int(count)])

evt_df = pd.DataFrame(columns=['hyp','bench','event','value'], data=hyp_events)
evt_df = evt_df[[x in benchs for x in evt_df['bench']]]

graphs = [
    ('inst_ret:h', 'inst_ret:uk', {'ylabel': 'Guest/Hypervisor Instructions\nRetired Ratio', 'dim': (3,3)}),
    ('exc_taken:h', 'inst_ret:uk', {'ylabel':'Hyp Exceptions taken per\nInstruction Retired'}),
    ('dache_l2_refill:h', 'inst_ret:uk', {'ylabel':'Hyp L2 Cache Miss per\nInstruction Retired'}),
    ('itlb_l1_refill:uk', 'inst_ret:uk', {'ylabel':'Guest iTLB Miss per\nInstruction Retired'}),
    # ('dtlb_l1_refill:uk', 'inst_ret:uk', {'ylabel':'Guest dTLB Miss per\nInstruction Retired'}),
    # ('dache_l2_refill:uk', 'inst_ret:uk', {'ylabel':'Hyp L2 Cache Miss per\nInstruction Retired'}),
]

correlations = []
for e, b, g in graphs:
    fig_count=1
    fig = plt.figure(figsize=(4,2))
    tmp = evt_df[evt_df['event'] == e]
    tmp = tmp.drop(columns=['event'])
    data = []
    for i, r in tmp.iterrows():
        value = int(r['value'])
        if b is not None:
            value /= int(evt_df[(evt_df['event'] == b) & (evt_df['bench'] == r['bench']) & (evt_df['hyp'] == r['hyp'])]['value'])
        data.append([r['hyp'],r['bench'], value])
    tmp = pd.DataFrame(columns=['hyp','bench','value'], data=data)  
    tmp.sort_values(by=['bench'])
    sns.barplot(data=tmp,x='bench', y='value', hue='hyp', edgecolor='black', palette=colors)
    fig_count+=1
    plt.legend().set_title(None)
    # plt.legend().remove()
    plt.ylabel(None)
    plt.xlabel(None)
    # plt.xticks(rotation=45)
    # plt.xticks(ticks=range(24), labels=range(24))
    plt.xticks(None)
    _, labels = plt.xticks()
    labels = [l.get_text().replace('-','\n') for l in labels]
    plt.xticks(np.arange(len(labels)), labels)
    title = e
    if b is not None:
        title += "/" + b
    plt.grid(which='both', axis='y', linestyle='--')
    plt.ylabel(None)
    plt.xticks([])
    plt.legend().remove()
    plt.tight_layout()
    plt.subplots_adjust(left=0.2, right=0.995, top=0.995, bottom=0.05)
    fig.canvas.manager.set_window_title(g['ylabel'])

    for h in ['bao', 'jailhouse', 'xen', 'sel4']:
        x = pd.Series([frames[(frames['hyp'] == h) & (frames['bench'] == b)]['val'].mean() for b in benchs])
        y = pd.Series([i for i in tmp[tmp['hyp'] == h]['value']])
        corr = x.corr(y)
        correlations.append([h, e, corr])

correlations.sort(reverse=True, key=(lambda x: x[2]))
for h, e, v in correlations:
    print(f"{h},{e}: {v:.2f}")


# ## nosuper mibench ###############################################################

# directory = "mibench-nosuper"

# colors = [
#     ("tab:orange", 1),
#     ("tab:green", 1),
#     ("tab:blue", 1),
#     ("tab:red", 1)
# ]
# colors = [[lighten_color(c, 1/(i/4+1))] for (c, r) in colors for i in range(0,r)]
# colors = reduce(lambda x, y: x + y, colors)

# base = [[bench, val] for [_, bench, val] in process_benchmark(directory,base_case)]
# base = pd.DataFrame(base, columns = ['bench', 'val'])
# base = {b: float(base[base['bench'] == b].mean()) for b in base['bench'].unique()}

# frames = [f for h in hypervisors for f in process_benchmark(directory,h, base)]
# frames = pd.DataFrame(frames, columns = ['hyp', 'bench', 'val'])
# frames = frames[[x in benchs for x in frames['bench']]]

# fig = plt.figure(figsize=(4,2))
# fig.canvas.manager.set_window_title(directory)
# print(frames)
# bp = sns.barplot(data=frames,x='bench', y='val', hue='hyp', edgecolor='black', palette=colors, errwidth = 1, capsize=0.1)
# plt.xlabel(None)
# plt.ylabel('% Perforance Degradation')
# plt.xticks(None)
# _, labels = plt.xticks()
# labels = [l.get_text().replace('-','\n') for l in labels]
# plt.xticks(np.arange(len(labels)), labels)
# # plt.xticks(rotation=90)
# plt.legend(loc = 'upper right').set_title(None)
# # plt.legend(bbox_to_anchor =(0.65, 1.25)).set_title(None)
# # plt.ylim(bottom=1.0)
# plt.grid(which='both', axis='y', linestyle='--')
# plt.yticks(np.arange(0,9,1))
# plt.ylabel(None)
# plt.xticks([])
# plt.legend().remove()
# plt.tight_layout()
# plt.subplots_adjust(left=0.1, right=0.995, top=0.995, bottom=0.05)
# # plt.get_current_fig_manager().window.showMaximized()


# hyp_events = []
# for hyp in hypervisors:
#     file = directory + "/" +  hyp
#     if not path.exists(file):
#         continue
#     events = open(file,'r')
#     for line in events:
#         line = line.strip()
#         r = re.search('-> mibench/*', line)
#         if r is not None:
#             bench = r.string
#             continue
#         r = re.search('[0-9]+ *r[0-9A-Fa-f]+(:[ukh]+)?', line)
#         if r is not None:
#             (s, e) = r.span()
#             (count, rawevent) = r.string[:e].split()
#             (event, level) = rawevent.split(':')
#             event = event_map[event] + ':' + level
#             bench_text = bench.removeprefix("-> mibench/")
#             bench_text = bench_text[bench_text.find('/')+1:]
#             hyp_events.append([hyp, bench_text, event, int(count)])

# evt_df = pd.DataFrame(columns=['hyp','bench','event','value'], data=hyp_events)
# evt_df = evt_df[[x in benchs for x in evt_df['bench']]]

# graphs = [
#     ('itlb_l1_refill:uk', 'inst_ret:uk', {'ylabel':'Guest iTLB Miss per\nInstruction Retired'}),
#     # ('dtlb_l1_refill:uk', 'inst_ret:uk', {'ylabel':'Guest dTLB Miss per\nInstruction Retired'}),
# ]

# correlations = []
# for e, b, g in graphs:
#     fig_count=1
#     fig = plt.figure(figsize=(4,2))
#     tmp = evt_df[evt_df['event'] == e]
#     tmp = tmp.drop(columns=['event'])
#     data = []
#     for i, r in tmp.iterrows():
#         value = int(r['value'])
#         if b is not None:
#             value /= int(evt_df[(evt_df['event'] == b) & (evt_df['bench'] == r['bench']) & (evt_df['hyp'] == r['hyp'])]['value'])
#         data.append([r['hyp'],r['bench'], value])
#     tmp = pd.DataFrame(columns=['hyp','bench','value'], data=data)  
#     tmp.sort_values(by=['bench'])
#     sns.barplot(data=tmp,x='bench', y='value', hue='hyp', edgecolor='black', palette=colors)
#     fig_count+=1
#     plt.legend().set_title(None)
#     # plt.legend().remove()
#     plt.ylabel(None)
#     plt.xlabel(None)
#     # plt.xticks(rotation=45)
#     # plt.xticks(ticks=range(24), labels=range(24))
#     plt.xticks(None)
#     _, labels = plt.xticks()
#     labels = [l.get_text().replace('-','\n') for l in labels]
#     plt.xticks(np.arange(len(labels)), labels)
#     title = e
#     if b is not None:
#         title += "/" + b
#     plt.grid(which='both', axis='y', linestyle='--')
#     plt.ylabel(None)
#     plt.xticks([])
#     plt.legend().remove()
#     plt.tight_layout()
#     plt.subplots_adjust(left=0.2, right=0.995, top=0.990, bottom=0.05)
#     fig.canvas.manager.set_window_title('nosuper-' + g['ylabel'])

# # ## interference #############################################################
directory = "mibench-base"


interf = [
    "jailhouse+interf",
    "jailhouse+col",
    "jailhouse+interf+col",
    "xen+interf",
    "xen+col",
    "xen+interf+col",
    "bao+interf",
    "bao+col",
    "bao+interf+col",
    "sel4+interf",
]

hypervisors=interf

colors = [
    ("tab:orange", 3),
    ("tab:green", 3),
    ("tab:blue", 3),
    ("tab:red", 1)
]
colors = [[lighten_color(c, 1/(i/4+1))] for (c, r) in colors for i in range(0,r)]
colors = reduce(lambda x, y: x + y, colors)

base = [[bench, val] for [_, bench, val] in process_benchmark(directory,base_case)]
base = pd.DataFrame(base, columns = ['bench', 'val'])
base = {b: float(base[base['bench'] == b].mean()) for b in base['bench'].unique()}

frames = [f for h in hypervisors for f in process_benchmark(directory,h, base)]
frames = pd.DataFrame(frames, columns = ['hyp', 'bench', 'val'])
frames = frames[[x in benchs for x in frames['bench']]]

fig = plt.figure(figsize=(12,3))
fig.canvas.manager.set_window_title(directory)
print(frames)
bp = sns.barplot(data=frames,x='bench', y='val', hue='hyp', edgecolor='black', palette=colors, errwidth = 1, capsize=0.1)
plt.xlabel(None)
plt.ylabel('% Perforance Degradation')
plt.xticks(None)
_, labels = plt.xticks()
labels = [l.get_text().replace('-','\n') for l in labels]
plt.xticks(np.arange(len(labels)), labels)
# plt.xticks(rotation=90)
plt.legend(loc = 'upper right', ncol=2).set_title(None)
# plt.legend(bbox_to_anchor =(0.65, 1.25)).set_title(None)
# plt.ylim(bottom=1.0)
plt.grid(which='both', axis='y', linestyle='--')
# plt.yticks(np.arange(0,9,1))
plt.tight_layout()
# plt.get_current_fig_manager().window.showMaximized()


hyp_events = []
for hyp in [base_case] + hypervisors:
    file = directory + "/" +  hyp
    if not path.exists(file):
        continue
    events = open(file,'r')
    for line in events:
        line = line.strip()
        r = re.search('-> mibench/*', line)
        if r is not None:
            bench = r.string
            continue
        r = re.search('[0-9]+ *r[0-9A-Fa-f]+(:[ukh]+)?', line)
        if r is not None:
            (s, e) = r.span()
            (count, rawevent) = r.string[:e].split()
            (event, level) = rawevent.split(':')
            event = event_map[event] + ':' + level
            bench_text = bench.removeprefix("-> mibench/")
            bench_text = bench_text[bench_text.find('/')+1:]
            hyp_events.append([hyp, bench_text, event, int(count)])

evt_df = pd.DataFrame(columns=['hyp','bench','event','value'], data=hyp_events)
evt_df = evt_df[[x in benchs for x in evt_df['bench']]]

graphs = [
    ('dache_l2_refill:uk', 'inst_ret:uk', {'ylabel':'Guest L2 Cache miss per\nInstruction Retired'}),
    # ('dache_l2_refill:uk', None, {'ylabel':'Guest L2 Cache misses'}),
]

colors = [
    ("tab:orange", 3),
    ("tab:green", 3),
    ("tab:blue", 3),
    ("tab:red", 1)
]
colors = [[lighten_color(c, 1/(i/4+1))] for (c, r) in colors for i in range(0,r)]
colors = reduce(lambda x, y: x + y, colors)

print(evt_df)
correlations = []
for e, b, g in graphs:
    fig_count=1
    fig = plt.figure(figsize=(8,3))
    tmp = evt_df[evt_df['event'] == e]
    tmp = tmp.drop(columns=['event'])
    data = []
    for i, r in tmp.iterrows():
        value = int(r['value'])
        base_value = int(evt_df[(evt_df['event'] == e) & (evt_df['bench'] == r['bench']) & (evt_df['hyp'] == base_case)]['value'])
        if b is not None:
            value /= int(evt_df[(evt_df['event'] == b) & (evt_df['bench'] == r['bench']) & (evt_df['hyp'] == r['hyp'])]['value'])
            base_value /= int(evt_df[(evt_df['event'] == b) & (evt_df['bench'] == r['bench']) & (evt_df['hyp'] == base_case)]['value'])
            # print(f"value {value}; base_value {base_value}")
            value -= base_value
        data.append([r['hyp'],r['bench'], value])
    tmp = pd.DataFrame(columns=['hyp','bench','value'], data=data)  
    tmp.sort_values(by=['bench'])
    colors = [colors[-1]] + colors[:-1]
    sns.barplot(data=tmp,x='bench', y='value', hue='hyp', edgecolor='black', palette=colors)
    fig_count+=1
    plt.legend().set_title(None)
    # plt.legend().remove()
    plt.ylabel(None)
    plt.xlabel(None)
    # plt.xticks(rotation=45)
    # plt.xticks(ticks=range(24), labels=range(24))
    plt.xticks(None)
    _, labels = plt.xticks()
    labels = [l.get_text().replace('-','\n') for l in labels]
    plt.xticks(np.arange(len(labels)), labels)
    title = e
    if b is not None:
        title += "/" + b
    plt.grid(which='both', axis='y', linestyle='--')
    plt.ylabel(None)
    plt.xticks([])
    plt.legend().remove()
    plt.tight_layout()
    plt.subplots_adjust(left=0.0975, right=0.995, top=0.990, bottom=0.05)
    fig.canvas.manager.set_window_title(g['ylabel'])


plt.show()
