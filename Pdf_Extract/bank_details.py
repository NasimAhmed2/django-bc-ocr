import re
from datetime import datetime
from dateutil import parser
import requests

class RowText_to_Dict:
    def __init__(self, lines):
        self.lines = lines
        self.result_dict = {}
        self.Bank_dict = {}

    def exclude_date_pattern(self,word):
        # Define a regular expression pattern to match date formats
        date_pattern = re.compile(r'\b\d{1,2}[-/]\w{3,}[-/]\d{2,4}\b')

        # Check if the word matches the date pattern
        return date_pattern.match(word) is not None

    #Function to find No. key value
    def find_No_Key_Value(self,idx,line):
        key_parts = line.upper().split('NO')
        key = (key_parts[0].strip() + ' No').strip()
        # Extract the next word after 'No' as the value
        value = None
        if len(key_parts) > 1:
            next_words = key_parts[1].split()
            for word in next_words:
                if (any(c.isalpha() for c in word) and any(c.isdigit() for c in word)) or all(c.isdigit() for c in word):
                    value = word.strip()
                    if value:
                        return key,value
        # If value is not found in the same line, look in the next lines
        if value is None and idx + 1 < len(self.lines):
            next_line_idx = idx + 1
            while next_line_idx < len(self.lines):
                next_words = self.lines[next_line_idx].split()
                for word in next_words:
                    if (any(c.isalpha() for c in word) and any(c.isdigit() for c in word)) or all(c.isdigit() for c in word) :
                        # Exclude the pattern "2digit+5alphabet+4digit+1alphabet+1digit+2alphabets"
                        pattern_to_exclude = re.compile(r'\b\d{2}[A-Za-z]{5}\d{4}[A-Za-z]\d[A-Za-z]{2}\b')
                        # Exclude date patterns
                        if not (pattern_to_exclude.match(word) or self.exclude_date_pattern(word)):
                            value = word.strip()
                            if value:
                                return key,value
                next_line_idx += 1
        return key,value

    #function to find account number
    #Function to find ifsc code
    def find_BankAccount_Key_Value(self,idx,line):
        if 'A/C' in line.upper():
            key_parts = line.upper().split('A/C')
        else:
            key_parts = line.upper().split('ACCOUNT')
        key = ('Bank Account No')
        value = None
        if len(key_parts) > 1:
            next_words = key_parts[1].split()
            for word in next_words:
                if all(c.isdigit() for c in word) and len(word) > 8:
                    value = word.strip()
                    if value:
                        return key,value
        # If value is not found in the same line, look in the next lines
        if value is None and idx + 1 < len(self.lines):
            next_line_idx = idx + 1
            while next_line_idx < len(self.lines):
                next_words = self.lines[next_line_idx].split()
                for word in next_words:
                    if all(c.isdigit() for c in word) and len(word) > 8:
                        value = word.strip()
                        if value:
                            return key,value
                    next_line_idx += 1
        return None ,None
    #Function to find ifsc code
    def find_IFSC_Key_Value(self,idx,line):
        key_parts = line.upper().split('IFSC')
        key = ('IFSC' + ' Code')
        value = None
        if len(key_parts) > 1:
            next_words = key_parts[1].split()
            pattern = re.compile(r'\b[A-Za-z]{4}\d{7}\b')
            for word in next_words:
                if (len(word) == 11) and pattern.match(word):
                    value = word.strip()
                    if value:
                        return key,value
        # If value is not found in the same line, look in the next lines
        if value is None and idx + 1 < len(self.lines):
            next_line_idx = idx + 1
            while next_line_idx < len(self.lines):
                next_words = self.lines[next_line_idx].split()
                pattern = re.compile(r'\b[A-Za-z]{4}\d{7}\b')
                for word in next_words:
                    if (len(word) == 11) and pattern.match(word):
                        value = word.strip()
                        if value:
                            return key,value
                next_line_idx += 1
        return None ,None

    #Function to find code key value
    def find_Code_Key_Value(self,idx,line):
        key_parts = line.upper().split('CODE')
        key = (key_parts[0].strip() + ' Code').strip()
        if 'IFSC' in key.upper():
            # Extract the next word after 'No' as the value
            value = None
            if len(key_parts) > 1:
                next_words = key_parts[1].split()
                for word in next_words:

                    if len(word) == 11:
                        value = word.strip()
                        if value:
                            return key,value
            # If value is not found in the same line, look in the next lines
            if value is None and idx + 1 < len(self.lines):
                next_line_idx = idx + 1
                while next_line_idx < len(self.lines):
                    next_words = self.lines[next_line_idx].split()
                    for word in next_words:
                        if all(c.isalpha() for c in word):
                            # Exclude the pattern "2digit+5alphabet+4digit+1alphabet+1digit+2alphabets"
                            pattern_to_exclude = re.compile(r'\b\d{2}[A-Za-z]{5}\d{4}[A-Za-z]\d[A-Za-z]{2}\b')
                            if not pattern_to_exclude.match(word):
                                value = word.strip()
                                if value:
                                    return key,value
                    next_line_idx += 1
        # Extract the next word after 'No' as the value
        value = None
        if len(key_parts) > 1:
            next_words = key_parts[1].split()
            for word in next_words:
                if (any(c.isalpha() for c in word) and any(c.isdigit() for c in word)) or all(c.isdigit() for c in word):
                    value = word.strip()
                    if value:
                        return key,value
        # If value is not found in the same line, look in the next lines
        if value is None and idx + 1 < len(self.lines):
            next_line_idx = idx + 1
            while next_line_idx < len(self.lines):
                next_words = self.lines[next_line_idx].split()
                for word in next_words:
                    if (any(c.isalpha() for c in word) and any(c.isdigit() for c in word)) or all(c.isdigit() for c in word) :
                        # Exclude the pattern "2digit+5alphabet+4digit+1alphabet+1digit+2alphabets"
                        pattern_to_exclude = re.compile(r'\b\d{2}[A-Za-z]{5}\d{4}[A-Za-z]\d[A-Za-z]{2}\b')
                        if not pattern_to_exclude.match(word):
                            value = word.strip()
                            if value:
                                return key,value
                next_line_idx += 1
        return key,value

    #Function to find date key value
    def find_date_key_value(self,idx,line):
        key_parts = line.split('DATE')
        key = (key_parts[0].strip() + ' Date').strip()
        # Extract the next word after 'Date' as the value
        value = None
        if len(key_parts) > 1:
            next_words = key_parts[1].split()
            if next_words:
                for word in next_words:
                    try:
                        # Check if the word matches any date format
                        parsed_date = parser.parse(word)
                        formatted_date = parsed_date.strftime('%d-%b-%y')
                        value = formatted_date
                        if value is not None:
                            return key , value
                    except ValueError:
                        continue
        # If the value is still None, check the next lines
        if value is None:
            next_line_idx = idx + 1
            while next_line_idx < len(self.lines):
                value = self.find_date_in_line(self.lines[next_line_idx])
                next_line_idx = next_line_idx + 1
                if value is not None:
                    return key , value
        return key , value

    def is_valid_date_format(word):
        try:
            parser.parse(word, fuzzy=False)
            return True
        except ValueError:
            return False

    # Function to find a date in a line
    def find_date_in_line(self,line):
        words = line.split()
        for word in words:
            try:
                if not word.isdigit() or not self.is_valid_date_format(word):
                    # Check if the word matches any date format
                    parsed_date = parser.parse(word)
                    formatted_date = parsed_date.strftime('%d-%b-%y')
        #             datetime.strptime(word, '%d-%b-%y')
                    return formatted_date
            except:
                continue
        return None



    #Function to find Number key value
    def find_Number_Key_Value(self,idx,line):
        key_parts = line.upper().split('NUMBER')
        key = (key_parts[0].strip() + ' NUMBER').strip()
        # Extract the next word after 'No' as the value
        value = None
        if len(key_parts) > 1:
            next_words = key_parts[1].split()
            for word in next_words:
                if (any(c.isalpha() for c in word) and any(c.isdigit() for c in word)) or all(c.isdigit() for c in word):
                    value = word.strip()
                    if value:
                        return key,value
        # If value is not found in the same line, look in the next lines
        if value is None and idx + 1 < len(self.lines):
            next_line_idx = idx + 1
            while next_line_idx < len(self.lines):
                next_words = self.lines[next_line_idx].split()
                for word in next_words:
                    if (any(c.isalpha() for c in word) and any(c.isdigit() for c in word)) or all(c.isdigit() for c in word) :
                        # Exclude the pattern "2digit+5alphabet+4digit+1alphabet+1digit+2alphabets"
                        pattern_to_exclude = re.compile(r'\b\d{2}[A-Za-z]{5}\d{4}[A-Za-z]\d[A-Za-z]{2}\b')
                        if not pattern_to_exclude.match(word):
                            value = word.strip()
                            if value:
                                return key,value
                next_line_idx += 1
        return key,value

    # Define a function to process lines based on certain condition to get key value pair
    def process_lines(self):
        #dict to store key value pair
        key_value_mapping = {}
        #Bank Account Number
        for idx, line in enumerate(self.lines):
            if 'A/C' in line.upper() or "ACCOUNT" in line.upper():
                key,value = self.find_BankAccount_Key_Value(idx,line)
                key_value_mapping[key] = value

        #for IFSC code
        for idx, line in enumerate(self.lines):
            if 'IFSC' in line.upper():
                key,value = self.find_IFSC_Key_Value(idx,line)
                key_value_mapping[key] = value 
    #     #for date keys
        for idx, line in enumerate(self.lines):
            if 'DATE' in line.upper():
                key,value = self.find_date_key_value(idx,line)
                key_value_mapping[key] = value

    #     #for keys with No
        for idx, line in enumerate(self.lines):
            if 'NO' in line.upper():
                key,value = self.find_No_Key_Value(idx,line)
                key_value_mapping[key] = value

    #     #for keys with Number
        email_suffix = 1
        for idx, line in enumerate(self.lines):
            #number field
            if 'NUMBER' in line.upper():
                key,value = self.find_Number_Key_Value(idx,line)
                key_value_mapping[key] = value

        for idx, line in enumerate(self.lines):
            if 'CODE' in line.upper():
                key, value = self.find_Code_Key_Value(idx,line)
                key_value_mapping[key] = value

    #     #for keys with EMAIL
        email_suffix = 1
        for idx, line in enumerate(self.lines):
            if '@' in line:
                words = line.split()
                for word in words:
                    if ('@' in word) and ('.' in word):
                        key = 'Email'
                        value = word
                if key in key_value_mapping:
                    # Compare the current value with the existing value
                    existing_value = key_value_mapping[key]
                    if existing_value != value:
                        # Append a numerical suffix to the key
                        key = f"{key}{email_suffix}"
                        email_suffix = email_suffix+1
                key_value_mapping[key] = value



         # for Gst key value pair        
        for idx, line in enumerate(self.lines):
            words = line.split()
            for word in words:
                if re.match(r'\b\d{2}[A-Za-z]{5}\d{4}[A-Za-z]\d[A-Za-z\d]{1,2}\b', word):
                    value = word
                    key = 'GST No'
                    if key in key_value_mapping:
                        # Compare the current value with the existing value
                        existing_value = key_value_mapping[key]
                        if existing_value != value:
                            # Append a numerical suffix to the key
                            key = "GST No1"
                    key_value_mapping[key] = value


        
        for key, value in key_value_mapping.items():
            if key != None:
                if "IFC" in key.upper() or "IFS" in key.upper():
                    print(key,value)
                    IFSC_Code = value
                    response = requests.get(f'https://ifsc.razorpay.com/{IFSC_Code}').json()

                    self.Bank_dict["Bank_Name"] = response['BANK']
                    self.Bank_dict["Bank_Branch"] = response['BRANCH']
                    self.Bank_dict["IFSC_Code"] = value
        self.Bank_dict['Bank_Account_No'] = key_value_mapping.get('Bank Account No')
        self.Bank_dict['Email'] = key_value_mapping.get('Email')
#         Bank_Details['VendorAddress'] = output_dict['VendorAddress']
#         Bank_Details['Account holder name'] = output_dict.get('VendorName')
        
        return self.Bank_dict
    
# text_parser = RowText_to_Dict(lines)

# # Access the result dictionary
# result_dict = text_parser.process_lines()
# result_dict