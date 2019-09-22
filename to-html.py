from os import listdir
from os.path import isfile, join
import os
import argparse
import sys

def clean(line):
    s = line.strip()
    if s.startswith('<title>') and s.endswith('</title>'):
        s = ''
    s = s.replace('&#182;', '')
    return s

def minify(file_path):
    with open(file_path, 'r') as fi:
        lines = [clean(line) for line in fi.readlines() if len(line.strip()) > 0]
        s = '\n'.join(lines)
        return s

def get_files(dir_path):
    return [f for f in listdir(dir_path) if isfile(join(dir_path, f)) and f.endswith('.ipynb')]

def parse_args(args):
    parser = argparse.ArgumentParser(
        'IPYNB to HTML', 
        epilog='One-Off Coder http://www.oneoffcoder.com')
    parser.add_argument('-d', '--dir', help='directory', required=True)
    return parser.parse_args(args)

def do_it(args):
    dir_path = args.dir[0:len(args.dir) -1] if args.dir.endswith('/') else args.dir
    for f in get_files(dir_path):
        file_path = f'{dir_path}/{f}'
        cmd = f'jupyter nbconvert --to html --template full {file_path}'
        resp = os.popen(cmd).read()
        print(resp)
        html_path = file_path.replace('.ipynb', '.html')
        minified_text = minify(html_path)
        with open(html_path, 'w') as f:
            f.write(minified_text)

if __name__ == '__main__':
    args = parse_args(sys.argv[1:])
    do_it(args)