# Model Checker
To run, install the requirements and execute main.py. 
This file takes a positional argument which should point to the directory containing the models (.aut files) and queries (.mcf files).
With parameter '-g' you can specify a specific .aut file on which to evaluate the queries. Without specifying an .aut file the model checker will evaluate all queries in the given directory on all labelled transition systems in the directory.
If you add parameter '-e' the model checker will use the Emerson-Lei algorithm, otherwise it will use the Naive Algorithm.

To give an example, if you want to evaluate the queries on the dining philophers problem set for n=2, with the Emerson-Lei algorithm, you might use a command like: 
python -m main "Experiments/dining" -g "dining_2.aut" -e
