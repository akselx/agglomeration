import os, json, sys, time
from synthicity.utils import misc
import dataset
from synthicity.urbansim import networks
import variables

args = sys.argv[1:]

dset = dataset.BayAreaDataset(os.path.join(misc.data_dir(),'bayarea.h5'))
#print "ADD A TEST FROM %s TO MAKE SURE  'dataset.compute_nonres_building_proportions(dset,2010)' IS VISIBLE" %__name__
#print dset.tester(2010)

num = misc.get_run_number()

if __name__ == '__main__':
  print time.ctime()
  for arg in args: misc.run_model(arg,dset,estimate=1,simulate=1)
  print time.ctime()
  t1 = time.time()
  numyears = 1
  num = misc.get_run_number()
  for i in range(numyears):
    t2 = time.time()
    for arg in args: misc.run_model(arg,dset,show=False,estimate=0,simulate=1,year=2010+i)
    print "Time to simulate year %d = %.3f" % (i+1,time.time()-t2)
  print "Actual time to simulate per year = %.3f" % ((time.time()-t1)/float(numyears))
  #dset.nodes.set_index(networks.NETWORKS.external_nodeids[0]).to_csv('accvars.csv',index_label="node_id",float_format="%.2f")
  print time.ctime()
  dset.save_coeffs(os.path.join(misc.runs_dir(),'run_drive_%d.h5'%num))
  dset.save_output(os.path.join(misc.runs_dir(),'run_drive_%d.h5'%num))
