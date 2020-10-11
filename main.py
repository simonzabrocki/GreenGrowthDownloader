from ggdata.scripts import download_all
import argparse

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Download and preprocess data.')
    parser.add_argument('API', metavar='API', type=str, help='A supported API name.')
    parser.add_argument('--path', metavar='path', type=str, default="data/", help='Where the downloaded file goes.')
    parser.add_argument('--raw', metavar='raw', type=lambda x: (str(x).lower() == 'true'), default=False, help='Save raw ouput')
    parser.add_argument('--restart', metavar='restart', type=lambda x: (str(x).lower() == 'true'), default=True, help='Redownload existing files')

    args = parser.parse_args()

    API_name, raw, path, restart = args.API, args.raw, args.path, args.restart

    download_all(API_name, path=path, raw=raw, restart=restart)
