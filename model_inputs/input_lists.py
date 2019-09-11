
with open('/users/soumyak/alzheimers_parkinsons/model_inputs/sc.idr.peaks','w') as idr_peaks, \
     open('/users/soumyak/alzheimers_parkinsons/model_inputs/sc.ambig.peaks','w') as ambig_peaks:
    for cluster in range(1,25):
        idr_peaks.write('/mnt/lab_data3/soumyak/adpd/peaks/idr_peaks/Cluster'+str(cluster)+'.idr.optimal.narrowPeak'+'\t'+'Cluster'+str(cluster)+'\n')
        ambig_peaks.write('/mnt/lab_data3/soumyak/adpd/peaks/ambiguous/Cluster'+str(cluster)+'.ambiguous.bed'+'\t'+'Cluster'+str(cluster)+'\n')

