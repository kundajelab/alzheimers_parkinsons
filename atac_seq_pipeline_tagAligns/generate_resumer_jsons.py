#uses the outputs of metadata.json to generate resume.hash.json for each file. 
#these should be used as inputs to resume_pipeline.sh to resume the pipelines from last stopping point 
import argparse 
import os 
import subprocess 
import glob 
import pdb 
import json 

def parse_args(): 
    parser=argparse.ArgumentParser(description="generates json files for resuming failed runs") 
    parser.add_argument("--metadata_file_list",default="/oak/stanford/groups/akundaje/projects/alzheimers_parkinsons/metadata_files.txt",help="text file with one metadata.json entry per row")
    parser.add_argument("--resolver_script_path",default="$HOME/atac-seq-pipeline/utils/resumer/resumer.py") 
    parser.add_argument("--outf",default="resumer_files.txt",help="file with resume*json files that were generated")
    return parser.parse_args() 

def main(): 
    args=parse_args() 
    print("generating output files") 
    print(args.outf) 
    outf=open(args.outf,'w') 
    outf_noresume=open(args.outf+".nometadata",'w') 

    all_resumer_files=[] 
    no_resumer_files=[] 
    metadata_file_list=open(args.metadata_file_list,'r').read().strip().split('\n') 
    for mfile in metadata_file_list: 
        # read metdata JSON file
        with open(mfile, 'r') as f:
            m_json_obj = json.load(f)
        # get pipeline version
        if 'atac.pipeline_ver' in m_json_obj['inputs'] and \
            m_json_obj['inputs']['atac.pipeline_ver'] == 'v1.1.6':
            resolver_script_dirname = os.path.dirname(args.resolver_script_path)
            output_def_json_file = os.path.join(resolver_script_dirname, 'atac.v1.1.6.json')
        else:
            output_def_json_file = None

        #cd into directory where metadata file is located
        mfile_dirname=os.path.dirname(mfile) 
        mfile_basename=os.path.basename(mfile)
        #print(mfile_dirname) 
        os.chdir(mfile_dirname) 
        #run the subprocess to create the resume json 

        if output_def_json_file:
            extra_param = ' '.join(['--output-def-json-file', output_def_json_file])
        else:
            extra_param = ''
        cmd = ' '.join([args.resolver_script_path, mfile_basename, extra_param])
        subprocess.call(cmd, shell=True)
        #ls the directory to make sure resume*json was actually generated 
        dirlist = glob.glob(mfile_dirname+"/resume*")
        if len(dirlist)==0: 
            no_resumer_files.append(mfile) 
        else:
            #use the most recent file 
            most_recent_time=None
            most_recent_file=None
            for f in dirlist: 
                cur_timestamp=os.path.getmtime(f)
                if most_recent_time==None: 
                    most_recent_time=cur_timestamp
                    most_recent_file=f
                elif cur_timestamp > most_recent_time: 
                    most_recent_time=cur_timestamp 
                    most_recent_file=f 
            all_resumer_files.append(most_recent_file) 
            print(most_recent_file) 
    outf.write('\n'.join(all_resumer_files)+'\n')
    outf.close() 
    outf_noresume.write('\n'.join(no_resumer_files)+'\n')
    outf_noresume.close() 

if __name__=="__main__": 
    main() 

