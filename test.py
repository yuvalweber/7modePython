from module.netapp import Controller
import datetime
import re

netapp_controller = Controller("<ip>","<user>","<password>")
volumes = netapp_controller.get_volumes()
for volume in volumes.keys():
    snapshots = netapp_controller.get_snapshots(volume)
    for snapshot in snapshots.keys():
        snap_date = datetime.datetime.fromtimestamp(int(snapshots[snapshot]['access-time']))
        print("{} --> {}".format(snapshot,snap_date))