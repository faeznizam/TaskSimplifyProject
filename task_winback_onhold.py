from script import remove_duplicate
from script import clean_phone_number


import pandas as pd
import os
import warnings

def main():
    # filter warning 
    warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl.styles.stylesheet')

    current_month = 'Apr - Copy'
    base_folder_path = r'C:\Users\mfmohammad\OneDrive - UNICEF\Desktop\TM Schedule Files\TM BSN Winback\2024\TM Winback Onhold'

    current_month_folder_path = os.path.join(base_folder_path, current_month)

    for subfolder in os.listdir(current_month_folder_path):
        subfolder_path = os.path.join(current_month_folder_path, subfolder)

        for file in os.listdir(subfolder_path):
            file_path = os.path.join(subfolder_path, file)

            df = pd.read_excel(file_path, dtype={'Post Code' : str})

            cleaned_df = clean_phone_number.process_mobile_numbers(df)

            cleaned_df = remove_duplicate.remove_duplicates(df)

            cleaned_df.to_excel(file_path, index=False)

            print(f'{file} has been save in the folder')


    for subfolder in os.listdir(current_month_folder_path):
        subfolder_path = os.path.join(current_month_folder_path, subfolder)

        for file in os.listdir(subfolder_path):
            file_path = os.path.join(subfolder_path, file)
            
            df = pd.read_excel(file_path)

            print(f'File: {file} , Number of Rows: {len(df)} , Inv no count: {clean_phone_number.count_invalid_number(df)}')
    
    





if __name__ == '__main__':
    main()