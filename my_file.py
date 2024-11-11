import argparse

from consts import RPS_LIMIT

parser = argparse.ArgumentParser(description="My First Argument Parser")

parser.add_argument("-n", "--name", type=str, help="name of person")
parser.add_argument("-a", "--age", type=int, help="age of person")

args = parser.parse_args()

name = args.name
age = args.age

print(f'Hello, {name} of age {age}')
print(RPS_LIMIT)
