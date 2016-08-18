import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='Film Umbrella cli tool')
    parser.add_argument('--name', '-n', help='Name of film')
    parser.add_argument('--release-date', '-rd', help='Release date of film')
    parser.add_argument('--genre', '-g', help='Genre of film')
    args = parser.parse_args()

