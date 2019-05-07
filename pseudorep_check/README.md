Generates pseudo-replicates for the ADPD cohort to control for variation in the biological replicates.

All tagAlign files for a particular region/condition are pooled, randomly split into even sized chunks equal to the number of original replicates. 
limma analysis is performed on the pseudo-rep count file and the number of differential peaks are compared to the number of differential peaks for the biological replicates. 
