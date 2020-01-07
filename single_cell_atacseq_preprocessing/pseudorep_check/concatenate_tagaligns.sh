#concatenates tagAlign files from the same region/group 
for f in t.*
do
    echo $f 
    for sample in `cat $f`
    do
	echo $sample 
	cat $sample >> grouped.$f 
    done
done

