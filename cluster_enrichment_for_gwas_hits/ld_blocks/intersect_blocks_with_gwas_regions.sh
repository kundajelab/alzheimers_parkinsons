for i in `seq 1 10`
do
    bedtools intersect -u -a fourier_ls-all.bed -b ../Kunkle.-$i.bed > blocks.Kunkle.overlap.-$i.bed
    bedtools intersect -u -a fourier_ls-all.bed -b ../23andme.-$i.bed > blocks.23andme.overlap.-$i.bed
done
