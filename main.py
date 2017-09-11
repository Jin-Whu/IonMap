#!/usr/bin/env python
# coding:utf-8
"""Script entry."""

import argparse
import process


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input', help='IONEX filepath')
    parser.add_argument('output', help='output directory')
    parser.add_argument('-s', '--start', type=str, help='start time HH:MM')
    parser.add_argument('-e', '--end', type=str, help='end time HH:MM')
    parser.add_argument('-i', '--interval', type=int, help='interval', default=3600)
    parser.add_argument('-b', '--bound', type=str, help='bound')
    parser.add_argument('-c', '--colorbar', type=int, help='colorbar range', default=100)
    parser.add_argument('-r', '--ratio', type=float, help='axes ratio', default=10./8)
    args = parser.parse_args()

    bound = args.bound if not args.bound else map(float, args.bound.split(','))
    process.process(args.input, args.output, args.interval, args.start, args.end, bound, args.colorbar, args.ratio)
