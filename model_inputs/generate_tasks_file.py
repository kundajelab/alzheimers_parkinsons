bigwigs = open('/oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/merged_tagAligns_outputs/fc.signal.unique.bigwig','r').read().strip().split('\n') 
idr_peaks = open('/oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/merged_tagAligns_outputs/idr.optimal.narrowPeaks.txt','r').read().strip().split('\n') 
ambig_peaks = open('/oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/merged_tagAligns_outputs/ambig.optimal.narrowPeaks.2.txt','r').read().strip().split('\n') 
samples=open('/oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/merged_tagAligns_outputs/samples.txt','r').read().strip().split('\n')
adpd_tasks = 'adpd.tasks.tsv'
sample_dict=dict()
#build the tasks file 
for sample in samples:
    sample_dict[sample]=[]
    for idr_peaks_file in idr_peaks:
        if idr_peaks_file.__contains__(sample):
            sample_dict[sample].append(idr_peaks_file)
            break
    for bigwig_file in bigwigs:
        if bigwig_file.__contains__(sample):
            sample_dict[sample].append(bigwig_file)
            break 
    for ambig_peaks_file in ambig_peaks:
        if ambig_peaks_file.__contains__(sample):
            sample_dict[sample].append(ambig_peaks_file)
            break
outf=open(adpd_tasks,'w')
for sample in sample_dict:
    outf.write(sample+'\t'+'\t'.join(sample_dict[sample])+'\n')
    
