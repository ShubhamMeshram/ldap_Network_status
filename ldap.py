import re
import time
import subprocess
import pandas as pd

d={}
user_list = ["raos", "liy206", "meshrams", "gallanik", "hsuc11" ,"kauns", "hasijay", "muiz","hannab2"]
ldap_str = "ldapsearch -LLL -h smusdir.bms.com  -x -b o=bms.com uid=$$user_id bmsentaccountstatus mail"
#ldap_mail = "ldapsearch -LLL -h smusdir.bms.com -x -b o=bms.com uid=$$user_id bmsentaccountstatus mail | grep "mail:" | cut -d " " -f 2"
df = pd.DataFrame([])

for user in user_list:
        final_ldap_str = ""
        final_ldap_str = ldap_str.replace("$$user_id", user)
        output = str(subprocess.check_output(final_ldap_str, shell=True))
        if re.findall("[\w\.-]+@[\w\.-]+",output):
                email = re.findall("[\w\.-]+@[\w\.-]+",output)
        else:
                email = "NA"

        print("Fetching data for {}".format(user))
        time.sleep(1)

        if "Enabled" in output:
            df=df.append(pd.DataFrame({'BMSID': user,'Status':"Employee/Consultant", 'Email': email},index=[0]),ignore_index=True)
        elif "Disabled" in output:
            df=df.append(pd.DataFrame({'BMSID':user, 'Status':"E/C who left BMS in the last 6 months", 'Email': email}, index=[0]), ignore_index=True)
        elif output == "b''":
            df=df.append(pd.DataFrame({'BMSID': user, 'Status': "Partner/Resigned", 'Email': email}, index=[0]), ignore_index=True)
        else:
            df=df.append(pd.DataFrame({'BMSID': user, 'Status': "Unknown", 'Email': email}, index=[0]), ignore_index=True)
print("\nGenerating result...")
time.sleep(2)
print("\n")
print(df)
print("\n")
