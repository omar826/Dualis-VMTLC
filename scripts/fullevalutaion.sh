#!/bin/bash
set -e

BENCHMARKS="BinaryTree Stack"

python3 classicalllmpipeline.py $BENCHMARKS
python3 contextualllmpipeline.py $BENCHMARKS

python3 run_all.py -m \
    ClassicalHornICE \
    ContextualHornICE \
    ClassicalLLMHornICE \
    ContextualLLMHornICE \
    -b $BENCHMARKS -p 8
