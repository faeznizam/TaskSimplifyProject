def count_rows(file, original_df, updated_df):
    ori_row = len(original_df) - 1
    updated_row = len(updated_df) - 1

    print(f'{file} - Original Row: {ori_row} - Updated Row: {updated_row}')