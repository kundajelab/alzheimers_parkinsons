for f in `cut -f1 groups.txt`
do
    echo "field:"$f
    grep $f tagAlign.files.txt | cut -f2 >> t.$f
done
