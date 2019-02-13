import pandas as pd
import numpy as np
import pathlib
from scipy import stats

currentDirectory = pathlib.Path(".")
print(currentDirectory)
currentPattern = "*.exe_*"
train = pd.DataFrame()
count = 0
names = ['Time', 'Steps', 'TPS']
dver = 0.999
dintp = 0.05
t = stats.norm.ppf(dver)
print(t)
for currentFile in currentDirectory.glob(currentPattern):
    with open(currentFile) as inp:
        for line in inp:
            if 'Statistics:' in line:
                df = pd.read_csv(inp, names = names)
                pars = str(currentFile).replace("Biggs_EXP6_Function", "BiggsEXP6").replace("Cluster2D2_function", "Cluster2D2").replace("Hartman_6_function", "Hartman6").split("_")
                #df['file'] = str(currentFile)
                df['prog'] = pars[0]
                df['func'] = pars[2]
                df['knrec'] = pars[3]
                #print(df)
                train = train.append(df)

grtrain = train.groupby(by=["prog", "func", "knrec"]).agg(["mean","std"]).reset_index(col_level=0)
for col in ["Time", "Steps", "TPS"]:
    grtrain["n_"+col] = t*grtrain[col]["std"]/(dintp*grtrain[col]["mean"])
    grtrain["n_"+col] = grtrain["n_"+col].apply(lambda x: int(x*x) if int(x*x) > 20 else 20)
    #if int(x*x) > 20 else 20
    #print(grtrain[col]["std"])
#print(grtrain.shape)
#print(grtrain.columns)
#print(grtrain.index)
grtrain.to_csv("n_exp.csv", index=False)
print(grtrain[grtrain["func"]=="BiggsEXP6"])
