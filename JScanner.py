#!/usr/bin/python3

from traceback import print_exc
from termcolor import colored
from argparse import ArgumentParser
from concurrent.futures import ThreadPoolExecutor

from lib.JSExtract import JSExtract
from lib.Functions import starter, output_writer

parser = ArgumentParser(description=colored('Javascript Scanner', color='yellow'), epilog=colored("Enjoy bug hunting", color='yellow'))
input_group = parser.add_mutually_exclusive_group()
output_group = parser.add_mutually_exclusive_group()
input_group.add_argument('---', '---', action="store_true", dest="stdin", help="Stdin")
input_group.add_argument('-w', '--wordlist', type=str, help='Absolute path of wordlist')
input_group.add_argument('-u', '--url', type=str, help="URL to scan (-d not necessary when -u specified)")
parser.add_argument('-d', '--domain', type=str, help="Domain")
output_group.add_argument('-oD', '--output-directory', type=str, help="Output directory")
output_group.add_argument('-o', '--output', type=str, help="Output file")
parser.add_argument('-e', '--enable-entropy', action="store_true", help="Enable entropy search")
parser.add_argument('-t', '--threads', type=int, help="Number of threads")
parser.add_argument('-b', '--banner', action="store_true", help="Print banner and exit")
argv = parser.parse_args()

input_wordlist = starter(argv)
JSExtractor = JSExtract(argv)
    
def main():
    with ThreadPoolExecutor(max_workers=argv.threads) as submitter:
        future_objects = [submitter.submit(JSExtractor.extract_from_url, input_word) for input_word in input_wordlist]
        if argv.output_directory:
            output_writer(argv.domain, future_objects, filepath=argv.output_directory)
        elif argv.output:
            output_writer(argv.output, future_objects, filepath=None)

if __name__ == "__main__":
    main()
