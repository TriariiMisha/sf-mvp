import argparse

parser = argparse.ArgumentParser(description="Data collector")

parser.add_argument("-t", "--tickers_file", type=str, help="path to file with tickers")
parser.add_argument("-d", "--duration", type=str, help="process duration in [int|float][d|h|m|s] format")
parser.add_argument("-b", "--batch_size", type=int, help="batch size when to write data")
