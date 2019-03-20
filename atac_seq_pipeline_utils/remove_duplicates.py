#!/usr/bin/python

import os,sys,subprocess

adpd = '/oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/outputs_PD'

for h in os.listdir(adpd):
    if h != 'logs':
        for i in os.listdir(adpd + '/' + h):
            for j in os.listdir(adpd + '/' + h + '/' + i):
                if len(os.listdir(adpd + '/' + h + '/' + i + '/' + j + '/cromwell-executions/atac')) > 1:
                    last_mod = {}
                    for k in os.listdir(adpd + '/' + h + '/' + i + '/' + j + '/cromwell-executions/atac'):
                        last_mod[adpd + '/' + h + '/' + i + '/' + j + '/cromwell-executions/atac/' + k] = int(subprocess.check_output('stat -c %Y ' + adpd + '/' + h + '/' + i + '/' + j + '/cromwell-executions/atac/' + k, shell=True))
                        print(adpd + '/' + h + '/' + i + '/' + j + '/cromwell-executions/atac/' + k)
                        print(subprocess.check_output('stat -c %Y ' + adpd + '/' + h + '/' + i + '/' + j + '/cromwell-executions/atac/' + k, shell=True))
                    print("FINDING DUPLICATES")
                    latest = ('',0)
                    for x in last_mod:
                        if last_mod[x] > latest[1]:
                            latest = (x,last_mod[x])
                    index = 1
                    for y in last_mod:
                        if y != latest[0]:
                            os.system('mv ' + y + ' ' + adpd + '/' + h + '/' + i + '/' + j + '/cromwell-executions/atac/duplicate_' + str(index))
                            print(str(index) + ': ' + y)
                            print(last_mod[y])
                            index += 1
                    print('')
                    print('----------')
                    print('')
