from dataset import PISToN_dataset
import os
import numpy as np


def get_processed(ppi_list, GRID_DIR):
    """
    Output processed protein complexes.
    For a small number of the models, interaction maps failed to preprocess, possibly due to clashes.
    The PIsToN scores for those models will be assigned to "incorrect"
    """
    processed_ppis = []
    for ppi in ppi_list:
        pid, ch1, ch2 = ppi.split('_')
        if os.path.exists(GRID_DIR + '/' + ppi + '.npy'):
            processed_ppis.append(ppi)
    return processed_ppis


import PyPluMA
import PyIO
import pickle
class CAPRIPlugin:
 def input(self, inputfile):
  self.parameters = PyIO.readParameters(inputfile)
 def run(self):
     pass
 def output(self, outputfile):
  CAPRI_DIR = PyPluMA.prefix()+"/"+self.parameters["CAPRI_DIR"]
  GRID_DIR = CAPRI_DIR+"/"+self.parameters["GRID_DIR"]
  CAPRI_LIST_FILE = CAPRI_DIR + "/" + self.parameters["CAPRI_LIST_FILE"]

  capri_list = [x.strip('\n') for x in open(CAPRI_LIST_FILE, 'r').readlines()]
  test_list_updated = get_processed(capri_list, GRID_DIR)

  print(f"{len(test_list_updated)}/{len(capri_list)} complexes were processed.")
  unprocessed_complexes = set(capri_list) - set(test_list_updated)

  print(f"Unprocessed complexes: {unprocessed_complexes}")
  print("The PISToN score for those complexes will be assigned to 2 (because smaller number is a better complex).")

  unique_pids = list(set([x.split('-')[0] for x in capri_list]))

  print(f"Unique targets: {unique_pids}")

  capri_dataset = PISToN_dataset(GRID_DIR, test_list_updated)
  outfile = open(outputfile+".dataset.pkl", "wb")
  pickle.dump(capri_dataset, outfile)
  outfile2 = open(outputfile+".uniquepid.pkl", "wb")
  pickle.dump(unique_pids, outfile2)
  outfile3 = open(outputfile+".testlist.pkl", "wb")
  pickle.dump(test_list_updated, outfile3)
  outfile4 = open(outputfile+".unprocessed.pkl", "wb")
  pickle.dump(unprocessed_complexes, outfile4)
