#! /bin/python3

from glob import glob
import re
import numpy as np

hypervisors = [
    'jailhouse',
    'xen',
    'bao',
    'sel4',
]

freertos = {'single': {}, 'dual': {} }
linux = {'single': {}, 'dual': {} }
freertos_rel = {'single': {}, 'dual': {} }
linux_rel = {'single': {}, 'dual': {} }

def convert_time(t):
    return (t*10 / 10**6)

try:
    f = open('base-freertos', 'r', encoding='latin-1')
    base = f.read()
    t = np.array([int(x) for x in re.findall('boottime-freertos ([0-9]*)', base)])
    t = convert_time(t)
    freertos['single']['base'] = round(t.mean(),2)
except:
    print("not able to process base-freertos")
    exit(-1)

try:
    f = open('base-linux', 'r', encoding='latin-1')
    base = f.read()
    t = np.array([int(x) for x in re.findall('boottime-linux ([0-9]*)', base)])
    t = convert_time(t)
    linux['single']['base'] = round(t.mean(),2)
except:
    print("not able to process base-linux")
    exit(-1)

for hyp in hypervisors:
    f = open(hyp + '-freertos', 'r', encoding='latin-1')
    base = f.read()
    t = np.array([int(x) for x in re.findall('boottime-freertos ([0-9]*)', base)])
    t = convert_time(t)
    freertos['single'][hyp] = round(t.mean(),2)
    freertos_rel['single'][hyp] = round((freertos['single'][hyp]/freertos['single']['base'] - 1) * 100, 2)

    f = open(hyp + '-linux', 'r', encoding='latin-1')
    base = f.read()
    t = np.array([int(x) for x in re.findall('boottime-linux ([0-9]*)', base)])
    t = convert_time(t)
    linux['single'][hyp] = round(t.mean(),2)
    linux_rel['single'][hyp] = round((linux['single'][hyp]/linux['single']['base'] - 1) * 100, 2)

    try: 
        f = open(hyp + '-dual-freertos', 'r', encoding='latin-1')
        base = f.read()
        t = np.array([int(x) for x in re.findall('boottime-freertos ([0-9]*)', base)])
        t = convert_time(t)
        freertos['dual'][hyp] = round(t.mean(),2)
        freertos_rel['dual'][hyp] = round((freertos['dual'][hyp]/freertos['single']['base'] - 1) * 100, 2)

        f = open(hyp + '-dual-linux', 'r', encoding='latin-1')
        base = f.read()
        t = np.array([int(x) for x in re.findall('boottime-linux ([0-9]*)', base)])
        t = convert_time(t)
        linux['dual'][hyp] = round(t.mean(),2)
        linux_rel['dual'][hyp] = round((linux['dual'][hyp]/linux['single']['base'] - 1) * 100,2)
    except:
        print("not able to process " + hyp + "-dual")

print('freertos single:\t\t', freertos['single'])
print('freertos single relative:\t', freertos_rel['single'])
print('freertos dual:\t\t\t', freertos['dual'])
print('freertos dual relative:\t\t', freertos_rel['dual'])

print('linux single:\t\t\t', linux['single'])
print('linux single relative:\t\t', linux_rel['single'])
print('linux dual:\t\t\t', linux['dual'])
print('linux dual relative:\t\t', linux_rel['dual'])

