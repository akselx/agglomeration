import os, json, sys, time
from synthicity.utils import misc
import dataset
from synthicity.urbansim import networks

args = sys.argv[1:]

dset = dataset.BayAreaDataset(os.path.join(misc.data_dir(),'bayarea.h5'))
num = misc.get_run_number()

if __name__ == '__main__':
  print time.ctime()
  for arg in args: misc.run_model(arg,dset,estimate=1)
  print time.ctime()
  t1 = time.time()
  numyears = 1
  #for i in range(numyears):
  #  t2 = time.time()
  #  for arg in args: misc.run_model(arg,dset,show=False,estimate=0,year=2010+i)
  #  print "Time to simulate year %d = %.3f" % (i+1,time.time()-t2)
  print "Actual time to simulate per year = %.3f" % ((time.time()-t1)/float(numyears))
  dset.nodes.set_index(networks.NETWORKS.external_nodeids[0]).to_csv('accvars.csv',index_label="node_id",float_format="%.2f")
  print time.ctime()
