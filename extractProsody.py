import os
from multiprocessing.dummy import Pool as ThreadPool

# Set your opensmile Extracter and path here
exe_opensmile = './opensmile/bin/SMILExtract.exe'
path_config = './opensmile/config/prosody/prosodyShs.conf'

# Set your data path and output path here
data_path = "./wav/"
save_path = './features/'  # output folder

# Extractor set-ups
opensmile_options = '-C ' + path_config


def feature_extract(fn):
    infilename = data_path + fn
    outfilename = save_path + fn[:-4] + ".csv"
    opensmile_call = exe_opensmile + ' ' + opensmile_options + \
        ' -I ' + infilename + ' -csvoutput ' + outfilename + \
        ' -start 60 -end 600'
    print(opensmile_call)
    os.system(opensmile_call)


for root, dirs, files in os.walk(data_path):
    for name in files:
        feature_extract(name)
    # print(files)
    # pool = ThreadPool()
    # pool.map(feature_extract, files)
    # pool.close()
    # pool.join()
