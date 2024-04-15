from script.onhold_hrsr import process_startek_file
from script.onhold_hrsr import startek_format
from script.onhold_hrsr import process_uts
from script.onhold_hrsr import process_ds

import pandas as pd
import os
import warnings

def startek_process(file_path, file, folder_path):
   df = pd.read_excel(file_path, dtype={'Post Code': str})
   df_strtk = startek_format.initialize_startek_format()
   df_strtk = startek_format.copy_data(df_strtk, df)
   df_strtk = startek_format.populate_pkg_column(file, df_strtk)
   df_strtk = process_startek_file.remove_duplicates(df_strtk)
   new_filename = process_startek_file.rename_startek_file(file)
   process_startek_file.save_file(df_strtk, new_filename, folder_path)

def uts_process(file_path, file, folder_path):
   df = process_uts.read_file(file_path)
   df = process_uts.populate_campaign(df, file)
   df = process_uts.remove_duplicates(df)
   new_filename = process_uts.rename_uts_file(file)
   process_uts.save_file(df, new_filename, folder_path)

def ds_process(file_path, file):
   df = process_ds.read_file(file_path)
   df = process_ds.populate_campaign(df, file)
   df = process_ds.remove_duplicates(df)
   process_ds.save_file(df, file_path, file)

def main():
   warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl.styles.stylesheet')

   current_month = 'Apr'
   base_folder = r'C:\Users\mfmohammad\OneDrive - UNICEF\Desktop\TM Schedule Files\Hard and Soft Reject\2024'
   month_folder = os.path.join(base_folder, current_month)

   
   
   # startek
   agency = 'Startek'
   agency_folder = os.path.join(month_folder, agency)
   for folder in os.listdir(agency_folder):
      if folder == 'HR':
         folder_path = os.path.join(agency_folder, folder)
         file_list = os.listdir(folder_path)
         for file in file_list:
            if 'New Onhold' in file:
               file_path = os.path.join(folder_path, file)
               startek_process(file_path, file, folder_path)
            else:
               pass
            
      elif folder == 'SR':
         folder_path = os.path.join(agency_folder, folder)
         file_list = os.listdir(folder_path)
         for file in file_list:
            if 'New Onhold' in file:
               file_path = os.path.join(folder_path, file)
               startek_process(file_path, file, folder_path)
            else:
               pass
      
      else:
         pass
 
    
         
   # UTS 
   agency2 = 'UTS'
   agency_folder2 = os.path.join(month_folder, agency2)
   for folder in os.listdir(agency_folder2):
      if folder == 'HR':
         folder_path2 = os.path.join(agency_folder2, folder)
         file_list2 = os.listdir(folder_path2)
         for file in file_list2:
            if 'New Onhold' in file:
               file_path = os.path.join(folder_path2, file)
               uts_process(file_path, file, folder_path2)
            else:
               pass
            
      elif folder == 'SR':
         folder_path2 = os.path.join(agency_folder2, folder)
         file_list2 = os.listdir(folder_path2)
         for file in file_list2:
            if 'New Onhold' in file:
               file_path = os.path.join(folder_path2, file)
               uts_process(file_path, file, folder_path2)
            else:
               pass
         
      else:
         pass


   # DS
   agency3 = 'DS'
   ds_folder = os.path.join(month_folder, agency3)
   file_list = os.listdir(ds_folder)
   for file in file_list:
      file_path = os.path.join(ds_folder, file)

      ds_process(file_path, file)

   # combine cc and debit file
   file1 = 'DS - CC 1 Month Prior to Card Expiry.xlsx'
   file2 = 'DS - Debit Card Expiry Date.xlsx'
   file_path1 = os.path.join(ds_folder, file1)
   file_path2 = os.path.join(ds_folder, file2)
   df1 = pd.read_excel(file_path1)
   df2 = pd.read_excel(file_path2)
   combine_df = pd.concat([df1,df2], ignore_index=True)
   output_filename = 'Card Pre Expiry Campaign.xlsx'
   output_filepath = os.path.join(ds_folder, output_filename)
   combine_df.to_excel(output_filepath, index=False)
   print(f'{output_filename} has been save to folder')

   # rename 
   file3 = 'New Onhold HR Report - DS.xlsx'
   file_path3 = os.path.join(ds_folder, file3)
   df3 = pd.read_excel(file_path3, dtype={'Post Code' : str})
   output_filename2 = 'OnHold DS HR Month 1.xlsx'
   output_filepath2 = os.path.join(ds_folder, output_filename2)
   df3.to_excel(output_filepath2, index=False)
   print(f'{output_filename2} has been save to folder')

if __name__ == '__main__':
   main()