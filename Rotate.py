#!/usr/bin/env python3
#
#
# snapshot was created by the following crontab line :
# 00 00 * * * /sbin/zfs snapshot pool01@$(/bin/date "+\%Y_\%m_\%d-\%H_\%M_\%S.daily")
# 00 00-23,3 * * * /sbin/zfs snapshot pool01@$(/bin/date "+\%Y_\%m_\%d-\%H_\%M_\%S.hourly")
# 00 00 * * 6 /sbin/zfs snapshot pool01@$(/bin/date "+\%Y_\%m_\%d-\%H_\%M_\%S.weekly")
#

import subprocess as sp
import argparse
import os

parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter, description=f"")
parser.add_argument('-q', '--quiet', help='destroy snapshots without confirmation', action='store_true', default=False)
a = parser.parse_args()

# number of most recent snapshots to keep
_h = 24 * 7
_d = 30
_w = 52

zfs_list = f'zfs list -H -t snapshot'

snapshots = sp.getoutput(zfs_list).splitlines()
snaps = {'daily':[], 'hourly':[], 'weekly':[]}
for line in snapshots:
    snapshot = line.split()[0]
    schedule = snapshot.split('.')[-1]
    snaps[schedule].append(snapshot)

h_del = snaps['hourly'][:len(snaps['hourly']) - _h]
d_del = snaps['daily'][:len(snaps['daily']) - _d]
w_del = snaps['weekly'][:len(snaps['weekly']) - _w]

destroy_list = h_del
destroy_list += d_del
destroy_list += w_del

for snapshot in destroy_list:
    cmd = f'zfs destroy {snapshot}'
    print(f'Running : {cmd}')
    if not a.quiet:
        answer = input(' - Continue ? (y) : ')
        if not answer.lower() == 'y':
            print('skipping')
            continue 
    print('deleting')
    print(sp.getoutput(f'{cmd}'))

print(f"""
deleted : {len(w_del)} hourly snapshots'
          {len(d_del)} daily snapshots'
          {len(w_del)} weekly snapshots'
""")


