numgroups=`cat groups.txt | wc -l`
echo $numgroups
for i in $(seq 1 $numgroups)
do
    cur_group=`head -n $i groups.txt | tail -n1 | cut -f1`
    echo "cur_group:$cur_group" 
    cur_group_num_reps=`head -n $i groups.txt | tail -n1 | cut -f2` 
    echo "cur_group_num_reps:$cur_group_num_reps"
    sbatch --partition akundaje,euan,owners,normal --mem=5G -o logs/$cur_group.o -e logs/$cur_group.e -n 1 --job-name $cur_group --time=04:00:00 generate_pseudoreps.sh $cur_group $cur_group_num_reps 
done

