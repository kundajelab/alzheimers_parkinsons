prefix="/oak/stanford/groups/akundaje/projects/alzheimers_parkinsons" 
json_list=prefix+"/jsons" 
narrowPeak_list=prefix+"/narrowPeakFiles.2.txt"
processed_samples=set() 
samples=set() 
for entry in open(narrowPeak_list,'r').read().strip().split('\n'): 
    tokens=entry.split('/')
    processed_sample='/'.join(tokens[7:11]).lstrip("outputs_")
    print(processed_sample) 
    processed_samples.add(processed_sample)
for entry in open(json_list,'r').read().strip().split('\n'): 
    sample=entry.split('.')[0] 
    samples.add(sample) 
    print(sample) 
failed=samples-processed_samples 
outf=open("to_rerun.txt",'w') 
for f in failed: 
    outf.write(f+'\n')
