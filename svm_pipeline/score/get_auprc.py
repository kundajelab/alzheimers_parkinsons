import pandas as pd
from sklearn.metrics import average_precision_score
prefix="/srv/scratch/annashch/gecco/SVM"
import sys
task=sys.argv[1]
fold=sys.argv[2]

labels=pd.read_csv(prefix+"/"+"svm_predictions_svmtrainset_genometestset"+"/"+task+"/"+"labels."+fold+".sorted.bed",header=None,sep='\t',index_col=[0,1,2])
preds=pd.read_csv(prefix+"/"+"svm_predictions_svmtrainset_genometestset"+"/"+task+"/"+"genomewidepredictions."+task+"."+fold+".sorted.bed",header=None,sep='\t',index_col=[0,1,2])
labels_rows=labels.shape[0]
preds_rows=preds.shape[0]
assert labels_rows==preds_rows
#make sure the indices are properly ordered!
cur_index=preds.index
labels=labels.loc[cur_index]
assert sum(preds.index==labels.index)==preds_rows 
merged=pd.concat([labels,preds],axis=1)[3].dropna()
merged.columns=['labels','preds']
#print(merged.shape)
#print(preds.shape)
#print(labels.shape)
#print(merged.head())
cur_auprc=average_precision_score(merged['labels'],merged['preds'])
total=merged.shape[0]
pos=sum(merged['labels'])
neg=total-pos
print(task+'\t'+fold+'\t'+str(cur_auprc)+'\t'+str(pos)+'\t'+str(neg))
