import pandas as pd
import uuid


class SpreadSheetData:

    def generate_spreadsheet():
        companies_data_sheet = '_docs/data/Companies.xlsx'
        companies_sheet_data = pd.read_excel(companies_data_sheet, sheet_name=0)

        legal_rep_data = pd.DataFrame({
            'Name': companies_sheet_data['Legal Representative Name'],
            'Identification': companies_sheet_data['Legal Representative Identification'],
            'Tax ID': companies_sheet_data['Legal Representative Tax ID'],
            'Phone': companies_sheet_data['Legal Representative Phone'],
            'Address': companies_sheet_data['Legal Representative Address'],
        })

        legal_rep_data['private_uuid'] = [
            str(uuid.uuid4()) for _ in range(len(legal_rep_data))]
        legal_rep_data['Username'] = legal_rep_data['Name'].str.split(
        ).str[0] + '_' + legal_rep_data['Name'].str.split().str[-1]
        legal_rep_data['First Name'] = legal_rep_data['Name'].str.split().str[0]
        legal_rep_data['Last Name'] = legal_rep_data['Name'].str.split().str[-1]
        legal_rep_data['Email'] = legal_rep_data['Name'] + '@riyuu.net'
        legal_rep_data.to_excel(
            '_docs/data/Representatives.xlsx', index=False)
