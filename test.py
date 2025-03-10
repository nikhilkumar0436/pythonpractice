import pandas as pd

print("enter filepath for STATIC AMOUNT:")
filePath1 = input()
book1 = pd.read_excel(filePath1)

print("enter filepath for DYNAMIC AMOUNT:")
filePath2 = input()
book2 = pd.read_excel(filePath2)

file1_columns = ['INPUT_CASE_NUMBER', 'MRCH_NM']
file2_columns = ['case-idnumber', 'merchant-name']

book1['combined_key'] = book1[file1_columns].astype(str).apply(lambda row: '.join(row), axis=1)
book2['combined_key'] = book2[file2_columns].astype(str).apply(lambda row: '.join(row), axis=1)

merged_df = pd.merge(book1, book2, on='combined_key', how='inner', suffixes=('_file1', '_file2'))
merged_df.drop(labels='combined_key', axis=1, inplace=True)

print(merged_df.columns)

filtered_row = []

for index, row in merged_df.iterrows():
    tAmount = row['TRANSACTION AMOUNT']
    if row['amount-of-charge'] == 'multiple-amount':
        if (tAmount == row['amount1'] or tAmount == row['amount2'] or tAmount == row['amount3'] or tAmount == row['amount4'] or tAmount == row['amount5'] or tAmount == row['amount6'] or tAmount == row['amount7']):
            filtered_row.append(row)
    elif row['amount-of-charge'] == 'specific-amount' and tAmount == row['amount']:
        filtered_row.append(row)
    elif row['amount-of-charge'] == 'amount-range' and row['from-amount'] <= tAmount <= row['to-amount']:
        filtered_row.append(row)

final = pd.DataFrame(filtered_row)
final.to_excel(excel_writer='test.xlsx', index=False)