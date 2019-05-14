module load ucsc_tools 
for f in expanded*bed
do
    liftOver $f hg38ToHg19.over.chain.gz hg19.$f unmapped.$f
    echo $f
done
