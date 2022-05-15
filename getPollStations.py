import pandas as pd
import requests

if __name__ == '__main__':
    url = "https://www.dgcs.gov.lb/PollingStations/GetPollingStationExpat"
    id_csv_locaiton = "Valid National ID_backup.csv"

    df_ids = pd.read_csv(id_csv_locaiton)

    # print(df_ids["National ID"])

    # polling_station_df = pd.DataFrame()
    dfs = []
    i=1
    for id in df_ids["National ID"]:
        id_txt = str(id).zfill(12)
        myobj = {'Type': 'IDNumber', 'IDNumber': id_txt}
        x = requests.post(url, data=myobj)

        # df = pd.read_json(x.json()["data"])
        # print(x.text)
        # print(x.json()["data"].keys())
        print(id," ",i,' out of ',len(df_ids["National ID"]))
        i=i+1
        df = pd.DataFrame(x.json()["data"],columns=x.json()["data"].keys(),index=[0])
        dfs.append(df)

    polling_station_df = pd.concat(dfs,ignore_index=True)
    polling_station_df.drop_duplicates(inplace=True)
    polling_station_df.replace("", float("NaN"), inplace=True)
    polling_station_df.dropna(how='all', axis=1, inplace=True)
    polling_station_df.to_csv("PollingStations.csv",
                              index=False, encoding="utf-8")
