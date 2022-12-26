#!/usr/bin/python3
import pandas as pd
import sys

if __name__ == '__main__':
    inet = sys.argv[1]
    thr = float(sys.argv[2])
    tmp=pd.read_csv(inet,sep='\t',header=None)
    tmp[tmp[2]>=thr].to_csv(inet,header=False,sep='\t',index=False)


