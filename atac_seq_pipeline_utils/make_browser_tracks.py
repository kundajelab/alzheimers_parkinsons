#!/scratch/PI/akundaje/soumyak/miniconda3/bin/python

import os,sys,subprocess

def main():

    ad = '/oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/outputs'
    pd = '/oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/outputs_PD'
    ad_files = {}
    pd_files = {}
    make_dict(ad, ad_files)
    make_dict(pd, pd_files)
    missing(ad_files)
    missing(pd_files)
    make_json(ad_files, 'AD_browser_tracks.json')
    make_json(pd_files, 'PD_browser_tracks.json')

def make_dict(adpd, dic):

    for h in os.listdir(adpd):
        if h != 'logs':
            for i in os.listdir(adpd + '/' + h):
                for j in os.listdir(adpd + '/' + h + '/' + i):
                    name = '\"'+j+'\"'
                    for k in os.listdir(adpd + '/' + h + '/' + i + '/' + j + '/cromwell-executions/atac'):
                        if os.path.isdir(adpd + '/' + h + '/' + i + '/' + j + '/cromwell-executions/atac/' + k + '/call-macs2_pooled/'):
                            for l in os.listdir(adpd + '/' + h + '/' + i + '/' + j + '/cromwell-executions/atac/' + k + '/call-macs2_pooled/execution/'):
                                if l.endswith('fc.signal.bigwig'):
                                    ftype = '\"bigwig\"'
                                    tname = '\"'+j+'_fc_bigwig\"'
                                    url = '\"http://mitra.stanford.edu/kundaje/projects/alzheimers_parkinsons/outputs/' + h + '/' + i + '/' + j + '/cromwell-executions/atac/' + k + '/call-macs2_pooled/execution/' + l + '\"'
                                    mode = '\"full\"'
                                    json_item = '{\"type\": '+ftype+',\"url\": '+url+',\"mode\": '+mode+',\"name\": '+tname+'}'
                                    if name not in dic:
                                        dic[name] = {'fc_bigwig': json_item, 'pval_bigwig': '', 'hammock': ''}
                                    else:
                                        dic[name]['fc_bigwig'] = json_item
                                if l.endswith('pval.signal.bigwig'):
                                    ftype = '\"bigwig\"'
                                    tname = '\"'+j+'_pval_bigwig\"'
                                    url = '\"http://mitra.stanford.edu/kundaje/projects/alzheimers_parkinsons/outputs/' + h + '/' + i + '/' + j + '/cromwell-executions/atac/' + k + '/call-macs2_pooled/execution/' + l + '\"'
                                    mode = '\"full\"'
                                    json_item = '{\"type\": '+ftype+',\"url\": '+url+',\"mode\": '+mode+',\"name\": '+tname+'}'
                                    if name not in dic:
                                        dic[name] = {'fc_bigwig': '', 'pval_bigwig': json_item, 'hammock': ''}
                                    else:
                                        dic[name]['pval_bigwig'] = json_item
                        else:
                            if name not in dic:
                                dic[name] = {'fc_bigwig': '', 'pval_bigwig': '', 'hammock': ''}
                        if os.path.isdir(adpd + '/' + h + '/' + i + '/' + j + '/cromwell-executions/atac/' + k + '/call-reproducibility_overlap/execution/'):
                            for m in os.listdir(adpd + '/' + h + '/' + i + '/' + j + '/cromwell-executions/atac/' + k + '/call-reproducibility_overlap/execution/'):
                                if m.endswith('optimal_peak.narrowPeak.hammock.gz'):
                                    ftype = '\"hammock\"'
                                    tname = '\"'+j+'_hammock\"'
                                    url = '\"http://mitra.stanford.edu/kundaje/projects/alzheimers_parkinsons/outputs/' + h + '/' + i + '/' + j + '/cromwell-executions/atac/' + k + '/call-reproducibility_overlap/execution/' + m + '\"'
                                    mode = '\"full\"'
                                    json_item = '{\"type\": '+ftype+',\"url\": '+url+',\"mode\": '+mode+',\"name\": '+tname+'}'
                                    if name not in dic:
                                        dic[name] = {'fc_bigwig': '', 'pval_bigwig': '', 'hammock': json_item}
                                    else:
                                        dic[name]['hammock'] = json_item
                        else:
                            if name not in dic:
                                dic[name] = {'fc_bigwig': '', 'pval_bigwig': '', 'hammock': ''}

def missing(dic):

    for item in dic:
        for ftype in dic[item]:
            if dic[item][ftype] == '':
                print('No '+ftype+' in '+item.strip('\"'))

def make_json(dic, filename):

    with open(filename,'w') as outfile:
        outfile.write('[')
        count = 0
        for item in dic:
            for ftype in dic[item]:
                if dic[item][ftype] != '':
                    if count != 0:
                        outfile.write(',')
                    outfile.write('\n'+dic[item][ftype])
                    count += 1
        outfile.write('\n]')

if __name__ == "__main__":
    main()
