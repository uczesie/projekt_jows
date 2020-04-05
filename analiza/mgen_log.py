import csv
import argparse

import pandas as pd
import numpy as np



def log_to_csv(filename, outputfile):
    # przetwarzanie logu na csv akceptowalne przez pandas (tylko RECV pozostają)
    with open(filename, 'r', newline='') as f, open(outputfile, 'w', newline='') as output:
        # pandas nie wspiera różnych długości w read_csv
        reader = csv.reader(f, delimiter=' ')
        writer = csv.writer(output, delimiter=',')
        writer.writerow(['recv', 'proto', 'flow', 'seq',
                         'src', 'dst', 'send', 'size'])
        for row in reader:
            if row[1] == 'RECV':
                # print(row)
                row.pop(1)
                row = row[:8]
                for i, element in enumerate(row):
                    if '>' in element:
                        row[i] = element[(element.find('>'))+1:]
                writer.writerow(row)
                # df.append(row)


def load_csv(filename):
    df = pd.read_csv(outputfile, delimiter=',', header=0)

    df['recv'] = pd.to_datetime(df['recv'])
    df['send'] = pd.to_datetime(df['send'])

    df['delay'] = df['recv'] - df['send']

    # da się lepiej, ale nie umiem
    # jitter = pd.DataFrame()
    df['jitter'] = np.nan

    for _, uniq in df[['flow', 'src']].drop_duplicates().iterrows():
        # print(uniq)
        last_delay = pd.Timedelta('nan')
        for index, vals in df.iterrows():
            # print(vals)
            if vals[['flow', 'src']].equals(uniq[['flow', 'src']]):
                try:
                    df.loc[index, 'jitter'] = np.absolute(
                        df.iloc[index]['delay']-last_delay)
                except TypeError:
                    df.loc[index, 'jitter'] = pd.Timedelta('nan')
                last_delay = df.iloc[index]['delay']

    df['jitter'] = pd.to_timedelta(df['jitter'])

    return df


def avg_delay(df):
    return df.groupby(['flow', 'src'])[['delay', 'size']].mean(numeric_only=False)


def avg_jitter(df):
    return df.dropna(subset=['jitter']).groupby(['flow', 'src'])[['jitter']].mean(numeric_only=False)


def throughput(df, interval=None):
    # pierwszy i ostatni w dataframe czas do liczenia przepustowości
    # zwracane są bity danych użytecznych (ponad warstwą transportową)
    # dobrze będzie ucinać ostatni przedział w przypadku podawania interwału
    if interval is None:
        time = df.iloc[-1]['recv'] - df.iloc[0]['recv']
    else:
        time = pd.Timedelta(interval)
    time = time.total_seconds()

    return df.groupby(['flow', 'src'])[['size']].sum()*8/time


def packet_loss(df):
    # zakładam ostatni numer sekwencyjny jako liczbę pakietów

    # new = pd.DataFrame()
    # print(df.groupby(['flow', 'src'], sort=False)['seq'].max())
    temp = df.groupby(['flow', 'src'], sort=False)['seq'].agg(['max', 'count'])
    # new['max_seq'] = temp['seq'].max()
    # new['packets'] = temp.count()
    temp['loss'] = (temp['max']-temp['count'])/temp['max']
    # print(temp)
    # print(temp.dtypes)
    return temp['loss']


def iter_by_timeframe(df, interval, start=None):
    if start is None:
        now = df.iloc[0]['recv']
    else:
        now = start
    end = df.iloc[-1]['recv']
    # yield 1
    while now < end:
        # print(df[(df['recv'] >= now) & (df['recv'] < now+interval)])
        yield now, df[(df['recv'] >= now) & (df['recv'] < now+interval)]
        now += interval


if __name__ == "__main__":
    # filename = 'mgen-h1.txt'
    # outputfile = 'mgen-h1-output.csv'

    parser = argparse.ArgumentParser()
    parser.add_argument('--input', dest='input', help='Plik z logiem mgen')
    parser.add_argument('--processed', dest='output', default='temp.csv',
                        help='Przetworzony plik csv zawierający tylko pakiety (RECV)')
    parser.add_argument('--interval', dest='interval', default='00:00:01',
                        help='Interwał czasowy podziału wyników [hh:mm:ss]')
    parser.add_argument('--fullcsv', dest='fullcsv',
                        help='Plik csv z df (całość)')
    parser.add_argument('--intervalcsv', dest='intervalcsv',
                        help='Plik csv z df (podział na interwały)')

    args = parser.parse_args()
    filename = args.input
    outputfile = args.output
    interval = args.interval
    fullcsv = args.fullcsv
    intervalcsv = args.intervalcsv
    print(args)
    # exit()

    if filename is not None:
        print('Przetwarzanie logu mgen')
        log_to_csv(filename, outputfile)

    print('Wczytywanie danych z przetworzonego pliku')
    df = load_csv(outputfile)
    # print(df)

    if fullcsv is not None:
        print('Zapisywanie df do csv (całość)')
        df.to_csv(fullcsv)

    # print(avg_delay(df))

    # print(packet_loss(df))

    # ---------------------------------------------
    # do całości średnie itp. można odkomentować w razie potrzeby
    df2 = avg_delay(df)
    df2['loss'] = packet_loss(df)
    df2['avg_jitter'] = avg_jitter(df)
    df2['throughput'] = throughput(df)
    print(df2)

    # print(df.dtypes)

    if intervalcsv is not None:
        with open(intervalcsv, 'w') as f:
            f.write('flow,src,delay,avg_size,avg_jitter,throughput,time\n')
            print('Zapisywanie df do csv (fragmentowane)')
    else:
        # reszta zbędna, bo i tak nic się z tym nie robi
        exit()

    for time, x in iter_by_timeframe(df, pd.Timedelta(interval)):
        temp_df = avg_delay(x)
        # straty w ten sposób nie zadziałają
        # temp_df['loss'] = packet_loss(x)
        temp_df['avg_jitter'] = avg_jitter(x)
        temp_df['throughput'] = throughput(x, interval)
        temp_df['time'] = time
        # print(temp_df)
        if intervalcsv is not None:
            temp_df.to_csv(intervalcsv, mode='a', header=False)
