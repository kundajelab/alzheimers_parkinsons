#uses the outputs of metadata.json to generate resume.hash.json for each file. 
#these should be used as inputs to resume_pipeline.sh to resume the pipelines from last stopping point 
import argparse 
import os 
import subprocess 
import glob 

def parse_args(): 
    parser=argparse.ArgumentParser(description="generates json files for resuming failed runs") 
    parser.add_argument("--metadata_file_list",default="/oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/metadata_files.txt",help="text file with one metadata.json entry per row")
    parser.add_argument("--resolver_script_path",default="$HOME/atac-seq-pipeline/utils/resumer/resumer.py") 
    parser.add_argument("--outf",default="resumer_files.txt",help="file with resume*json files that were generated")
    return parser.parse_args() 

def main(): 
    args=parse_args() 
    all_resumer_files=[] 
    metadata_file_list=open(args.metadata_file_list,'r').read().strip().split('\n') 
    for mfile in metadata_file_list: 
        #cd into directory where metadata file is located
        mfile_dirname=os.path.dirname(mfile) 
        mfile_basename=os.path.basename(mfile)
        #print(mfile_dirname) 
        os.chdir(mfile_dirname) 
        #run the subprocess to create the resume json 
        subprocess.call(' '.join([args.resolver_script_path,mfile_basename]),shell=True)
        #ls the directory to make sure resume*json was actually generated 
        dirlist = glob.glob(mfile_dirname+"/resume*")
        for f in dirlist: 
            all_resumer_files.append(f) 
        print(dirlist) 
    outf=open(args.outf,'w') 
    outf.write('\n'.join(all_resumer_files)+'\n')
if __name__=="__main__": 
    main() 

