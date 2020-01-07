buddies_nn=set(open('buddies_nn.txt','r').read().strip().split('\n'))
sig_svm=set(open('sig_svm.txt','r').read().strip().split('\n'))
nn_unique=buddies_nn-sig_svm
outf=open('nn_unique.txt','w')
outf.write('\n'.join(nn_unique)+'\n')

