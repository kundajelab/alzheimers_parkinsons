#/scratch/PI/akundaje/annashch/alzheimers_parkinsons/ryan_peak_overlap/ctr.idr.optimal_set.sorted.merged.bed
#/scratch/PI/akundaje/annashch/alzheimers_parkinsons/ryan_peak_overlap/idr.optimal_set.sorted.merged.bed

#/scratch/PI/akundaje/annashch/alzheimers_parkinsons/ryan_peak_overlap/PeakSets/190104_ControlsOnly_x_Region_reproducible/All_Samples.fwp.filter.non_overlapping.bed
#/scratch/PI/akundaje/annashch/alzheimers_parkinsons/ryan_peak_overlap/PeakSets/190104_ControlsOnly_x_Region_majority/All_Samples.fwp.filter.non_overlapping.bed
#/scratch/PI/akundaje/annashch/alzheimers_parkinsons/ryan_peak_overlap/PeakSets/190104_AllSamples_x_Group-Region_reproducible/All_Samples.fwp.filter.non_overlapping.bed
#/scratch/PI/akundaje/annashch/alzheimers_parkinsons/ryan_peak_overlap/PeakSets/190104_AllSamples_x_Group-Region_majority/All_Samples.fwp.filter.non_overlapping.bed

#CONTROLS, REPRODUCIBLE
#common, from idr 
bedtools intersect -wa -a /scratch/PI/akundaje/annashch/alzheimers_parkinsons/ryan_peak_overlap/ctr.idr.optimal_set.sorted.merged.bed -b /scratch/PI/akundaje/annashch/alzheimers_parkinsons/ryan_peak_overlap/PeakSets/190104_ControlsOnly_x_Region_reproducible/All_Samples.fwp.filter.non_overlapping.bed | sort |uniq > ctr.idr_intersecting_controls.reproducible.a

#common, from Ryan 
bedtools intersect -wa -b /scratch/PI/akundaje/annashch/alzheimers_parkinsons/ryan_peak_overlap/ctr.idr.optimal_set.sorted.merged.bed -a /scratch/PI/akundaje/annashch/alzheimers_parkinsons/ryan_peak_overlap/PeakSets/190104_ControlsOnly_x_Region_reproducible/All_Samples.fwp.filter.non_overlapping.bed | sort |uniq > ctr.idr_intersecting_controls.reproducible.b

#idr - Ryan 
bedtools subtract -A -a /scratch/PI/akundaje/annashch/alzheimers_parkinsons/ryan_peak_overlap/ctr.idr.optimal_set.sorted.merged.bed -b /scratch/PI/akundaje/annashch/alzheimers_parkinsons/ryan_peak_overlap/PeakSets/190104_ControlsOnly_x_Region_reproducible/All_Samples.fwp.filter.non_overlapping.bed | sort |uniq > ctr.idr_minus_controls.reproducible

#Ryan - idr
bedtools subtract -A -b /scratch/PI/akundaje/annashch/alzheimers_parkinsons/ryan_peak_overlap/ctr.idr.optimal_set.sorted.merged.bed -a /scratch/PI/akundaje/annashch/alzheimers_parkinsons/ryan_peak_overlap/PeakSets/190104_ControlsOnly_x_Region_reproducible/All_Samples.fwp.filter.non_overlapping.bed | sort |uniq > controls.reproducible_minus_ctr.idr 

#CONTROLS, majority
#common, from idr 
bedtools intersect -wa -a /scratch/PI/akundaje/annashch/alzheimers_parkinsons/ryan_peak_overlap/ctr.idr.optimal_set.sorted.merged.bed -b /scratch/PI/akundaje/annashch/alzheimers_parkinsons/ryan_peak_overlap/PeakSets/190104_ControlsOnly_x_Region_majority/All_Samples.fwp.filter.non_overlapping.bed  | sort |uniq > ctr.idr_intersecting_controls.majority.a
#common, from Ryan 
bedtools intersect -wa -b /scratch/PI/akundaje/annashch/alzheimers_parkinsons/ryan_peak_overlap/ctr.idr.optimal_set.sorted.merged.bed -a /scratch/PI/akundaje/annashch/alzheimers_parkinsons/ryan_peak_overlap/PeakSets/190104_ControlsOnly_x_Region_majority/All_Samples.fwp.filter.non_overlapping.bed | sort |uniq > ctr.idr_intersecting_controls.majority.b

#idr - Ryan 
bedtools subtract -A -a /scratch/PI/akundaje/annashch/alzheimers_parkinsons/ryan_peak_overlap/ctr.idr.optimal_set.sorted.merged.bed -b /scratch/PI/akundaje/annashch/alzheimers_parkinsons/ryan_peak_overlap/PeakSets/190104_ControlsOnly_x_Region_majority/All_Samples.fwp.filter.non_overlapping.bed | sort |uniq > ctr.idr_minus_controls.majority

#Ryan - idr
bedtools subtract -A -b /scratch/PI/akundaje/annashch/alzheimers_parkinsons/ryan_peak_overlap/ctr.idr.optimal_set.sorted.merged.bed -a /scratch/PI/akundaje/annashch/alzheimers_parkinsons/ryan_peak_overlap/PeakSets/190104_ControlsOnly_x_Region_majority/All_Samples.fwp.filter.non_overlapping.bed | sort |uniq > controls.majority_minus_ctr.idr 

#------------------------------------------------------------------------------------------------------------
#ALL SAMPLES, reproducible
#common, from idr 
bedtools intersect -wa -a /scratch/PI/akundaje/annashch/alzheimers_parkinsons/ryan_peak_overlap/idr.optimal_set.sorted.merged.bed -b /scratch/PI/akundaje/annashch/alzheimers_parkinsons/ryan_peak_overlap/PeakSets/190104_AllSamples_x_Group-Region_reproducible/All_Samples.fwp.filter.non_overlapping.bed | sort |uniq > idr_intersecting_controls.reproducible.a

#common, from Ryan 
bedtools intersect -wa -b /scratch/PI/akundaje/annashch/alzheimers_parkinsons/ryan_peak_overlap/idr.optimal_set.sorted.merged.bed -a /scratch/PI/akundaje/annashch/alzheimers_parkinsons/ryan_peak_overlap/PeakSets/190104_AllSamples_x_Group-Region_reproducible/All_Samples.fwp.filter.non_overlapping.bed | sort |uniq > idr_intersecting_controls.reproducible.b


#idr - Ryan 
bedtools subtract -A -a /scratch/PI/akundaje/annashch/alzheimers_parkinsons/ryan_peak_overlap/idr.optimal_set.sorted.merged.bed -b /scratch/PI/akundaje/annashch/alzheimers_parkinsons/ryan_peak_overlap/PeakSets/190104_AllSamples_x_Group-Region_reproducible/All_Samples.fwp.filter.non_overlapping.bed  | sort |uniq > all.idr_minus_all.reproducible

#Ryan - idr 
bedtools subtract -A -b /scratch/PI/akundaje/annashch/alzheimers_parkinsons/ryan_peak_overlap/idr.optimal_set.sorted.merged.bed -a /scratch/PI/akundaje/annashch/alzheimers_parkinsons/ryan_peak_overlap/PeakSets/190104_AllSamples_x_Group-Region_reproducible/All_Samples.fwp.filter.non_overlapping.bed  | sort |uniq > all.reproducible_minus_all.idr


#ALL SAMPLES,  majority 
#common, from idr 
bedtools intersect -wa -a /scratch/PI/akundaje/annashch/alzheimers_parkinsons/ryan_peak_overlap/idr.optimal_set.sorted.merged.bed -b /scratch/PI/akundaje/annashch/alzheimers_parkinsons/ryan_peak_overlap/PeakSets/190104_AllSamples_x_Group-Region_majority/All_Samples.fwp.filter.non_overlapping.bed  | sort |uniq > idr_intersecting_controls.majority.a

#common, from Ryan 
bedtools intersect -wa -b /scratch/PI/akundaje/annashch/alzheimers_parkinsons/ryan_peak_overlap/idr.optimal_set.sorted.merged.bed -a /scratch/PI/akundaje/annashch/alzheimers_parkinsons/ryan_peak_overlap/PeakSets/190104_AllSamples_x_Group-Region_majority/All_Samples.fwp.filter.non_overlapping.bed | sort |uniq > idr_intersecting_controls.majority.b


#idr - Ryan 
bedtools subtract -A -a /scratch/PI/akundaje/annashch/alzheimers_parkinsons/ryan_peak_overlap/idr.optimal_set.sorted.merged.bed -b /scratch/PI/akundaje/annashch/alzheimers_parkinsons/ryan_peak_overlap/PeakSets/190104_AllSamples_x_Group-Region_majority/All_Samples.fwp.filter.non_overlapping.bed | sort |uniq > all.dir_minus_all.majority

#Ryan - idr 
bedtools subtract -A -a /scratch/PI/akundaje/annashch/alzheimers_parkinsons/ryan_peak_overlap/PeakSets/190104_AllSamples_x_Group-Region_majority/All_Samples.fwp.filter.non_overlapping.bed -b /scratch/PI/akundaje/annashch/alzheimers_parkinsons/ryan_peak_overlap/idr.optimal_set.sorted.merged.bed | sort |uniq > all.majority_minus_all.idr 
