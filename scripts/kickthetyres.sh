#!/bin/bash
set -e

BENCHMARKS="BinaryTree"

> evaluation_summary.txt # deleting contents
> implication_report.txt
> seahorn_summary.txt
> cvc5_summary.txt

python3 classicalllmpipeline.py $BENCHMARKS
python3 contextualllmpipeline.py $BENCHMARKS

python3 run_all.py -m \
    ClassicalHornICE \
    ContextualHornICE \
    ClassicalLLMHornICE \
    ContextualLLMHornICE \
    -b $BENCHMARKS -p 8
