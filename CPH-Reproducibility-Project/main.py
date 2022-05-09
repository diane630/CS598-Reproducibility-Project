'''
Main function for CPH.
'''
# Necessary packages
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import argparse
import numpy as np
import pandas as pd
from data_loader import data_loader
from CPH import cph
from utils import rmse_loss
from math import *
import random

def test_loss(ori_data_x,imputed_data_x,ward_nor_list):
    df = pd.read_csv("./data/Chronic_Diseases_Prevalence_Dataset.csv")
    ward_code_list=list(df['Ward Code'])
    n=0
    y=0
    y_mae=0
    no, dim = ori_data_x.shape
    dim2 = int(dim)
    print(dim,dim2)
    R_original=ori_data_x[:,dim2-1]
    R_result = imputed_data_x[:,dim2-1]
    yy_mae = []
    for id in ward_nor_list:
        result=R_result[id]
        origial=R_original[id]
        # print
        # print(id,origial,result)
        if str(origial)!="nan" and origial!=0:
            y=y+pow((origial-result),2)
            n+=1
            y_mae = y_mae + abs(origial - result)
            yy_mae.append(abs(origial - result))
    RMSE=sqrt(y/n)
    MAE=y_mae/n
    # print("RMSE:",RMSE)
    # print("MAE:",MAE)
    # print()
    return RMSE, MAE

def main (args,yy,disease, learning_rate):
  '''
  Args:
    - miss_rate: probability of missing components
    - batch:size: batch size
    - hint_rate: hint rate
    - alpha: hyperparameter
    - iterations: iterations
    
  Returns:
    - imputed_data_x: imputed data
    - rmse, mae
  '''

  miss_rate = args.miss_rate
  
  cph_parameters = {'batch_size': args.batch_size,
                     'hint_rate': args.hint_rate,
                     'alpha': args.alpha,
                     'iterations': args.iterations}

  # Load data and introduce missingness
  ori_data_x, miss_data_x, data_m, ward_nor_list, data_image = data_loader(miss_rate, yy, disease)
  # print(ori_data_x, miss_data_x, data_m, ward_nor_list, data_image)

  # Impute missing data
  imputed_data_x = cph(miss_data_x, cph_parameters,data_image, learning_rate)
  ###
  # print(imputed_data_x)

  RMSE, MAE = test_loss(ori_data_x,imputed_data_x,ward_nor_list)

  return RMSE, MAE

def get_error(disease = "obesity", missing_rate = 90, hint_rate = 0.9, learning_rate = 1e-5, epoch = 10):
  # original CPH repo suggests using disease = "obesity", missing_rate = 90, hint_rate = 0.9, learning_rate = unknown
    
  missing_rate = missing_rate

  for yy in range(2008,2009):
      mmin = 100
      print(disease, ", year:" + str(yy) + "-2017")
      for i in range(epoch):
          # Inputs for the main function
          parser = argparse.ArgumentParser()
          parser.add_argument(
            '--miss_rate',
            help='missing data probability',
            default=missing_rate/100,
            type=float)
          parser.add_argument(
            '--batch_size',
            help='the number of samples in mini-batch',
            default=483,
            type=int)
          parser.add_argument(
            '--hint_rate',
            help='hint probability',
            default=hint_rate,
            type=float)
          parser.add_argument(
            '--alpha',
            help='hyperparameter',
            default=100,
            type=float)
          parser.add_argument(
            '--iterations',
            help='number of training interations',
            default=10000,
            type=int)

          args = parser.parse_args()

          # Calls main function
          RMSE, MAE = main(args,yy, disease, learning_rate)
          if RMSE+MAE < mmin:
              RMSE2= RMSE
              MAE2 = MAE
              mmin = RMSE+MAE
          if i >0 and i%10 == 0:
            print(f"epoch: {i}, RMSE: {RMSE2}, MAE: {MAE2}")
      print("target disease: ", disease)
      try:
        print("RMSE:", RMSE2)
        print("MAE:", MAE2)
        return RMSE2, MAE2
      except:
        print("RMSE1:", RMSE)
        print("MAE1:", MAE)
        return RMSE, MAE

def grid_search(disease = "obesity", missing_rate = 90, hint_rate = 0.9, learning_rate = 1e-5, epoch = 10):
    lr = 3e-05
    disease = "obesity"
    epoch = 10
    step = 1.02
    for i in range(50):
      RMSE2, MAE2 = get_error(disease = disease, missing_rate = 50, hint_rate = 0.9, learning_rate = lr, epoch = epoch)
      print("done searching learning rate: ", float(lr))
      with open(f"./result/learning_rate_err_{disease}.txt", "a") as f:
        f.write(f"l_r: {float(lr)}, RMSE: {RMSE2}, MAE: {MAE2}\n")
      lr /= step

if __name__ == '__main__':
    learning_rate = 2.9411764705882354e-05
    disease = "obesity"
    epoch = 20
    hint_rate = 0.9
    RMSE, MAE = get_error(disease = disease, missing_rate = 50, hint_rate = hint_rate, learning_rate = learning_rate, epoch = epoch)
    print(disease, RMSE, MAE)