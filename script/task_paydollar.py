# import
import pandas as pd
import re
import os
import numpy as np

# function 
def clean_and_reformat(df):
    column_to_clean = ['Card Issuing Bank (System)', 'Card Type']  # list column to clean
    df[column_to_clean] = df[column_to_clean].replace('--', '')    # replace blank row with --
    df = df.drop('Status', axis=1)                                 # delete Status column 

    # replace 'CREDIT' to Credit Card and 'Debit' to Debit Card
    df['Card Type'] = df['Card Type'].apply(lambda x : 'Credit Card' if x == 'CREDIT' else ('Debit Card' if x == 'DEBIT' else x ))
    
    # get 2 digit from year and create dummy column
    df['Exp Year 2'] = df['Exp Year'].str[2:]

    # reformat exp month and exp year
    df['Exp Date'] = np.where((df['Exp Month'] != '') & (df['Exp Year 2'] != ''),
                                df['Exp Month'] + '/' + df['Exp Year 2'], 
                                '')
    # drop dummy column
    df = df.drop('Exp Year 2', axis=1)

    # create list with new column order
    new_column_order = ['Merchant Ref.', 'Payment Mtd.', 'Card/Account', 'Exp Month', 'Exp Year',
                        'Exp Date', 'Bank Ref.', 'Holder Name', 'Card Issuing Bank (System)',
                        'Card Type', 'Channel Type', 'Payer IP']
    # rearrange 
    df = df[new_column_order]

    # rename the column
    df.rename(
        columns={
        'Merchant Ref.':'sescore__External_Donation_Reference_Id__c',
        'Payment Mtd.' : 'sescore__Payment_Submethod__c',
        'Card/Account' : 'sescore__Card_Number_Masked__c', 
        'Exp Month' : 'Exp Month',
        'Exp Year' : 'Exp Year',
        'Bank Ref.' : 'sescore__Secondary_Token__c',
        'Holder Name' : 'sescore__Cardholder_Name__c',
        'Card Issuing Bank (System)' : 'sescore__Card_Issuer__c',
        'Payer IP' : 'Payer IP',
        'Card Type' : 'sescore__Payment_Method__c',
        'Channel Type' : 'Channel Type',
        'Exp Date' : 'sescore__Card_Expiry__c'
        }, 
        inplace=True)
    
    return df

# function for date format
def get_date_input(prompt):
    while True:
        try:
            date_input = input(prompt)
            day, month, year = map(int, date_input.split('/'))
            formatted_date = f'{day:02d}{month:02d}{year:02d}'
            return formatted_date
        except ValueError:
            print('Invalid input. Please enter valid date in format dd/mm/yy')

# get start and end date from user
def get_user_date_input():
    print('Enter start date:')
    start_date = get_date_input('Enter date in dd/mm/yy format: ')

    print('\nEnter end date:')
    end_date = get_date_input('Enter date in dd/mm/yy format: ')

    return start_date, end_date

# main function
def main():
    # input folder path. Edit path accordingly.
    folder_path = r'C:\Users\mfmohammad\OneDrive - UNICEF\Desktop\Paydollar vs SF Task\2024\Jan'
    file_name = 'order.xlsx'

    # combine folder path and file name
    file_path = os.path.join(folder_path, file_name)

    # read file
    df = pd.read_excel(file_path)

    # apply function
    df = clean_and_reformat(df)

    # rename the file:
    start_date, end_date = get_user_date_input()
    new_file_name = f'Online Donation - {start_date}-{end_date} - Paydollar.xlsx'
    
    # build output file path
    new_file_path = os.path.join(folder_path, new_file_name)
    
    # save file in the folder
    df.to_excel(new_file_path, index=False)

    # successfull attempt prompt
    print(f'File {new_file_name} been saved in the folder')

if __name__ == "__main__":
    main()
    