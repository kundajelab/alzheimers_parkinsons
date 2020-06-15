#!/users/soumyak/miniconda3/bin/python

import nbformat
from nbconvert.preprocessors import *
from nbparameterise import extract_parameters, parameter_values, replace_definitions
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor


def main():
    clusters = [i for i in range(1, 25)]
    nb_pool = []
    for cluster in clusters:
        #create_new_notebook(cluster)
        nb_pool.append(cluster)
    with ProcessPoolExecutor(max_workers=24) as pool:
        merge=pool.map(create_new_notebook, nb_pool)


def create_new_notebook(cluster):

    with open("template.ipynb") as f:
        nb = nbformat.read(f, as_version=4)
    orig_parameters = extract_parameters(nb)

    print("Cluster", cluster)

    # Update the parameters and run the notebook
    params = parameter_values(orig_parameters, cluster_input=cluster)
    new_nb = replace_definitions(nb, params, execute=False)
    new_nb, resources = ClearOutputPreprocessor().preprocess(new_nb, resources={})
    new_nb, resources = ExecutePreprocessor(timeout=1440).preprocess(new_nb, resources={})

    # Save
    with open("../Cluster%s.ipynb" % str(cluster), 'w') as f:
        nbformat.write(new_nb, f)


if __name__ == "__main__":
    main()
