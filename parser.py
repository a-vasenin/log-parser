#!/usr/bin/env python3

import argparse
import csv
from pathlib import Path


argparser = argparse.ArgumentParser()
argparser.add_argument('libraries_path', help='Path to libraries logs.\nExample: ./libraries')
argparser.add_argument('--platform', default='all', choices=['win', 'lin', 'mac'] ,help='can be one of [all, linux, macosx, windows]')
args = argparser.parse_args()


def parser(libraries_path, platform='all'):
    platforms = []
    if platform.lower() == 'all':
        platforms = ['linux', 'macosx', 'windows']
    elif platform.lower() == 'win':
        platforms.append('windows')
    elif platform.lower() == 'lin':
        platforms.append('linux')
    elif platform.lower() == 'mac':
        platforms.append('macosx')

    fieldnames = ['OS', 'Architecture', 'Domain', 'Optimization', 'Pass rate']
    with open('result.csv', 'w') as f:
        writer = csv.DictWriter(f, fieldnames)
        writer.writeheader()

    for platform in platforms:
        path = Path(libraries_path, platform)
        txt_files = [i for i in path.glob('**/*.txt')]
        end_files = [i.stem for i in path.glob('**/*.end')]

        for txt_file in txt_files:
            file_dict = {'OS': platform.capitalize(), 'Architecture': txt_file.parts[3], 'Domain': txt_file.parts[4], }
            if txt_file.stem in end_files:
                file_dict['Optimization'] = txt_file.stem[-2:]

                with open(txt_file) as f:
                    number_of_tests = ''
                    number_of_successes = ''

                    for line in f:
                        if ".Number of tests" in line:
                            line = line.strip('\n| ')
                            number_of_tests = line.lstrip('.Number of tests : ')
                        elif ".Successes" in line:
                            line = line.strip('\n| ')
                            number_of_successes = line.lstrip('.Successes : ')

                    if all([number_of_tests, number_of_successes]):
                        success_percent = 100 * float(number_of_successes)/float(number_of_tests)
                        success_percent = format(success_percent, '.2f')
                    else:
                        success_percent = 'aborted'
                    file_dict['Pass rate'] = success_percent

            with open('result.csv', 'a') as f:
                writer = csv.DictWriter(f, fieldnames, restval='n/a')
                writer.writerow(file_dict)


parser(args.libraries_path, args.platform)
