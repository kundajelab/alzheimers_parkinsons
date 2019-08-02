num_samples=`cat idr.optimal.narrowPeaks.txt| wc -l`  
echo $num_samples 
for i in `seq 1 $num_samples`
do
    echo $i
    a_file=`head -n $i overlap.optimal.narrowPeaks.txt | tail -n1`
    b_file=`head -n $i idr.optimal.narrowPeaks.txt | tail -n1`
    cur_sample=`head -n $i samples.txt | tail -n1`
    echo "a_file:$a_file"
    echo "b_file:$b_file" 
    bedtools intersect -v -a $a_file -b $b_file > $cur_sample.ambiguous.bed
    gzip $cur_sample.ambiguous.bed
    echo $cur_sample.ambiguous.bed.gz 
done



