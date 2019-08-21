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

    make_json(ad_files, 'ADAD', 'fc_bigwig', 'AD_ADAD_fc_browser_tracks.json')
    make_json(ad_files, 'ADAD', 'pval_bigwig', 'AD_ADAD_pval_browser_tracks.json')

    make_json(ad_files, 'CTRH', 'fc_bigwig', 'AD_CTRH_fc_browser_tracks.json')
    make_json(ad_files, 'CTRH', 'pval_bigwig', 'AD_CTRH_pval_browser_tracks.json')

    make_json(ad_files, 'CTRL', 'fc_bigwig', 'AD_CTRL_fc_browser_tracks.json')
    make_json(ad_files, 'CTRL', 'pval_bigwig', 'AD_CTRL_pval_browser_tracks.json')

    make_json(ad_files, 'LOAD', 'fc_bigwig', 'AD_LOAD_fc_browser_tracks.json')
    make_json(ad_files, 'LOAD', 'pval_bigwig', 'AD_LOAD_pval_browser_tracks.json')

    make_json(pd_files, 'CTRL', 'fc_bigwig', 'PD_CTRL_fc_browser_tracks.json')
    make_json(pd_files, 'CTRL', 'pval_bigwig', 'PD_CTRL_pval_browser_tracks.json')

    make_json(pd_files, 'GBA1', 'fc_bigwig', 'PD_GBA1_fc_browser_tracks.json')
    make_json(pd_files, 'GBA1', 'pval_bigwig', 'PD_GBA1_pval_browser_tracks.json')

    make_json(pd_files, 'LOPD', 'fc_bigwig', 'PD_LOPD_fc_browser_tracks.json')
    make_json(pd_files, 'LOPD', 'pval_bigwig', 'PD_LOPD_pval_browser_tracks.json')

    make_json(pd_files, 'LRRK', 'fc_bigwig', 'PD_LRRK_fc_browser_tracks.json')
    make_json(pd_files, 'LRRK', 'pval_bigwig', 'PD_LRRK_pval_browser_tracks.json')

def make_dict(adpd, dic):

    outputs = adpd.split('/')[-1] + '/'

    for h in os.listdir(adpd):
        if h != 'logs':
            for i in os.listdir(adpd + '/' + h):
                for j in os.listdir(adpd + '/' + h + '/' + i):
                    name = '\"'+j+'\"'
                    qtc = '{\"anglescale\":1,\"pr\":255,\"pg\":71,\"pb\":20,\"nr\":255,\"ng\":0,\"nb\":0,\"pth\":\"rgb(0,0,178)\",\"nth\":\"#800000\",\"thtype\":1,\"thmin\":0,\"thmax\":25,\"thpercentile\":90,\"height\":50,\"summeth\":1}'
                    for k in os.listdir(adpd + '/' + h + '/' + i + '/' + j + '/cromwell-executions/atac'):
                        macs2 = ''
                        for call_macs2 in ['/call-macs2_signal_track/shard-0','/call-macs2/shard-0','/call-macs2_signal_track_pooled','/call-macs2_pooled']:
                            if os.path.isdir(adpd + '/' + h + '/' + i + '/' + j + '/cromwell-executions/atac/' + k + call_macs2 + '/execution/'):
                                for l in os.listdir(adpd + '/' + h + '/' + i + '/' + j + '/cromwell-executions/atac/' + k + call_macs2 + '/execution/'):
                                    if l.endswith('fc.signal.bigwig'):
                                        ftype = '\"bigwig\"'
                                        tname = '\"'+j+'_fc_bigwig\"'
                                        url = '\"http://mitra.stanford.edu/kundaje/projects/alzheimers_parkinsons/'+ outputs + h + '/' + i + '/' + j + '/cromwell-executions/atac/' + k + call_macs2 + '/execution/' + l + '\"'
                                        mode = '1'
                                        json_item = '{\"type\": '+ftype+',\"url\": '+url+',\"mode\": '+mode+',\"name\": '+tname+',\"qtc\": '+qtc+'}'
                                        if name not in dic:
                                            dic[name] = {'fc_bigwig': json_item, 'pval_bigwig': '', 'hammock': ''}
                                        else:
                                            dic[name]['fc_bigwig'] = json_item
                                    if l.endswith('pval.signal.bigwig'):
                                        ftype = '\"bigwig\"'
                                        tname = '\"'+j+'_pval_bigwig\"'
                                        url = '\"http://mitra.stanford.edu/kundaje/projects/alzheimers_parkinsons/'+ outputs + h + '/' + i + '/' + j + '/cromwell-executions/atac/' + k + call_macs2 + '/execution/' + l + '\"'
                                        mode = '1'
                                        json_item = '{\"type\": '+ftype+',\"url\": '+url+',\"mode\": '+mode+',\"name\": '+tname+',\"qtc\": '+qtc+'}'
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
                                    url = '\"http://mitra.stanford.edu/kundaje/projects/alzheimers_parkinsons/' + outputs + h + '/' + i + '/' + j + '/cromwell-executions/atac/' + k + '/call-reproducibility_overlap/execution/' + m + '\"'
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

def make_json(dic, group, track, filename):

    with open(filename,'w') as outfile:
        outfile.write('[')
        count = 0
        for item in dic:
            if item.strip('\"').split('_')[0] == group:
                for ftype in [track,'hammock']:
                    if dic[item][ftype] != '':
                        if count != 0:
                            outfile.write(',')
                        outfile.write('\n'+dic[item][ftype])
                        count += 1
        outfile.write('\n]')

if __name__ == "__main__":
    main()
