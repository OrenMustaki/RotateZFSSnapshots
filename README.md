# RotateZFSSnapshots

A tool to rotate and delete zfs snapshots.
this script will delete all snapshot excluding the last N snapshots
of each one of the following types : hourly, daily, weekly.

crontab lines used to create snapshots:

00 00 * * * /sbin/zfs snapshot pool01@$(/bin/date "+\%Y_\%m_\%d-\%H_\%M_\%S.daily")

00 00-23,3 * * * /sbin/zfs snapshot pool01@$(/bin/date "+\%Y_\%m_\%d-\%H_\%M_\%S.hourly")

00 00 * * 6 /sbin/zfs snapshot pool01@$(/bin/date "+\%Y_\%m_\%d-\%H_\%M_\%S.weekly")

