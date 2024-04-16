import pandas as pd
import numpy as np
import re
sizes = {
    'PSL':
        '0.115	0.125	0.135	0.15	0.165	0.185	0.21	0.25	0.35	0.475	0.575	0.855	1.22	1.53	1.99	2.585	3.37',
    'water':
        '0.119552706	0.140894644	0.169068337	0.204226949	0.227523895	0.253291842	0.279285719	0.35426882	0.604151175	0.705102841	0.785877189	1.100686925	1.117622254	1.765832382	2.690129739	3.014558062 4.392791391'}


def read_pop(path, size='water'):
    # calculate size dlog_bin
    print(size)
    binedges = np.fromstring(sizes[size], dtype=float, sep="\t")
    midbin = (binedges[1:] + binedges[:-1])/2
    dlog_bin = np.log10(binedges[1:]) - np.log10(binedges[:-1])
    r = re.compile('b[0-9]')

    # Load file
    df = pd.read_csv(path)
    df = df.dropna(axis=0)
    df = df.reset_index(drop=True)
    df['datetime'] = pd.to_datetime(df['timestamp'], format="%Y%m%d%H%M%S")

    binlab = list(filter(r.search, df.columns))
    for particle_size, each_dlog_bin in zip(binlab, dlog_bin):
        df[particle_size] = df[particle_size]/(df[' POPS_flow(ccm/s)']) / each_dlog_bin

    return df, midbin
