#!/usr/bin/env python
# coding:utf-8

import os
import commands
import string

disks = ["sda", "sdb", "sdc", "sdd", "sde", "sdf"]
present_disks = []
present_disks_size = []


def disk_info():
        for a in disks:
                disk = a
                check_disk_command = commands.getoutput('fdisk -l /dev/'+disk)
                output = string.split(check_disk_command)
                if len(output) == 0:
                        break
                else:
                        disk_label_raw = output[9]
                        find_colon = disk_label_raw.find(":")
                        disk_label = disk_label_raw[0:find_colon]
                        disk_size_raw = output[10]
                        find_coma = disk_size_raw.find('.')
                        disk_size = disk_size_raw[0:find_coma]
                        present_disks.append(disk_label)
                        present_disks_size.append(disk_size)
                        print disk_label, disk_size

disk_info()
print present_disks
print present_disks_size


def zeruj():
        disk_choose = raw_input("Ktory dysk chcesz wyzerowac (np: /dev/sda): ")
        if disk_choose not in present_disks:
                print "Nie ma takiego dysku"
                return disk_info(), zeruj()
        else:
            disk_position = present_disks.index(disk_choose)
            size_position = disk_position
            zerowany_dysk = "of="+str(present_disks[disk_position])
            rozmiar_dysku = str(present_disks_size[size_position])+"G"
            komenda =  "cat /dev/zero | pv -bpt -s ", rozmiar_dysku,"|dd", zerowany_dysk, " bs=1M"
            command = string.join(komenda)
            os.system(command)


def pv_check():
        command = commands.getoutput('dpkg -l|grep pv')
        output = string.split(command)
        return output


def pv_install():
    check_pv = pv_check()
    if len(check_pv) == 0:
        print "PV nie jest zainstalowane. "
        print "Trwa odswierzanie repozutorum"
        commands.getoutput('apt-get update')
        print "Trwa instalacja pakietu pv"
        commands.getoutput('apt-get install pv')
        print "instalacja zakonczona"
    else:
        print "Pakiet pv jest już zainstalowany"

pv_install()
zeruj()
