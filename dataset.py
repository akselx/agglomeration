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
  
  def tester(dataset,year):
    """
    toy example to test visibility (Nov 12 2013)
    """
    costar = dataset.costar.merge(dataset.parcels[['zone_id']],right_index=True,left_on='parcel_id')
    costar = costar.groupby('zone_id')['averageweightedrent','rentable_building_area'].median()
    costar.head()

    zone_to_node = dataset.parcels[['_node_id0','zone_id']]
    nodes = dataset.nodes.reset_index(level=0,drop=True).join(zone_to_node.join(costar))
    #nodes = dataset.nodes.reset_index(level=0,drop=True)
    print pd.Series(nodes.index).describe()

    return nodes

  def compute_nonres_building_proportions(dataset,year):

    buildings = dataset.fetch('buildings')
    buildings = buildings[buildings['general_type'] <> 'Residential']
    buildings['rent'] = dataset.load_attr('nonresidential_rent',year)

    tmp = buildings[['_node_id0','building_sqft','general_type']]
    tmp['weightedrent'] = tmp['building_sqft']*buildings['rent']

    totsum = tmp.groupby('_node_id0').sum().rename(columns={"building_sqft":"totsum"})
    totsum["weightedrent"] /= totsum["totsum"]
    del tmp["weightedrent"]

    offsum = tmp[tmp['general_type']=='Office'].groupby('_node_id0').sum().rename(columns={"building_sqft":"offsum"})
    indsum = tmp[tmp['general_type']=='Industrial'].groupby('_node_id0').sum().rename(columns={"building_sqft":"indsum"})
    retsum = tmp[tmp['general_type']=='Retail'].groupby('_node_id0').sum().rename(columns={"building_sqft":"retsum"})

    nodesums = totsum.join(offsum).join(indsum).join(retsum)
    for fname in ["offsum","retsum","indsum"]: nodesums[fname] = nodesums[fname].fillna(0)
    for fname in ["off","ret","ind"]: nodesums[fname+"pct"] = nodesums[fname+"sum"]/nodesums["totsum"]
    print pd.Series(nodesums.index).describe()
    
    return nodesums



  def tester3(dataset,year):
    """
    toy example to test visibility (Nov 12 2013)
    """
    #costar = dataset.costar.merge(dataset.parcels[['zone_id']],right_index=True,left_on='parcel_id')
    costar = dataset.costar.groupby('City')['averageweightedrent','rentable_building_area'].median()
    costar.head()

    city_to_node = dataset.parcels[['_node_id0','zone_id']]
    nodes = dataset.nodes.reset_index(level=0,drop=True).join(zone_to_node.join(costar))
    #nodes = dataset.nodes.reset_index(level=0,drop=True)
    return nodes

  def tester2(dataset,year):
      """
      toy example to test visibility (Nov 12 2013)
      """
      return dataset.nodes.reset_index(level=0,drop=True).join(dataset.buildings.groupby('_node_id0')['building_sqft','residential_units','stories'].agg(['mean','median','sum']))

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

  def fetch_costar(self):
    costar = self.store['costar']
    costar = costar[costar['averageweightedrent']>0]
    costar['stories'] = costar['number_of_stories']
    costar['general_type'] = costar['PropertyType']
    costar = costar[costar.general_type.isin(["Office","Retail","Industrial","Flex"])]
    return costar


  # the norental and noowner leave buildings with unassigned tenure
  def building_filter(self,norental=0,noowner=0,residential=1,nofilter=0):
    buildings = self.fetch('buildings')
    if nofilter: return buildings
    if residential: buildings = buildings[(buildings['general_type'] == 'Residential')]
    else:           buildings = buildings[(buildings['general_type'] <> 'Residential')]
    if norental:    buildings = buildings[buildings['tenure'] <> 1]
    if noowner:     buildings = buildings[buildings['tenure'] <> 2]
    return buildings
