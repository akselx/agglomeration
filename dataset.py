import numpy as np, pandas as pd
import time, os
from synthicity.utils import misc
from synthicity.urbansim import dataset, networks
import warnings

warnings.filterwarnings('ignore',category=pd.io.pytables.PerformanceWarning)

# this is the central location to do all the little data format issues that will be needed by all models

class BayAreaDataset(dataset.Dataset):

  def __init__(self,filename):
    super(BayAreaDataset,self).__init__(filename)
  
  def fetch_nets(self):

    nets = self.store['nets']
    nets = self.join_for_field(nets,'buildings','building_id','_node_id0')
    return nets

  def fetch_factual(self):
    return pd.read_csv(os.path.join(misc.data_dir(),'factual_places.csv'))
  
  def filter_pois(self,filt,field="category",sub=1):
    df = self.fetch('factual')
    if sub: df = df[df[field].str.contains(filt,na=False)]
    else: df = df[df[field].str.equals(filt,na=False)]
    return df
