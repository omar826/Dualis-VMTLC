#!/bin/bash
set -e

PARAM=${1:-20}

> evaluation_summary.txt # deleting contents
> implication_report.txt
> seahorn_summary.txt
> cvc5_summary.txt

rm -rf ../logs/ClassicalHornICEPipeline_Logs \
    ../logs/ClassicalLLMHornICEFUZZPipeline_Logs \
    ../logs/ClassicalLLMHornICEPipeline_Logs \
    ../logs/ContextualHornICEPipeline_Logs \
    ../logs/ContextualLLMHornICEFUZZPipeline_Logs \
    ../logs/ContextualLLMHornICEPipeline_Logs

rm -rf ../benchmarks/ClassicalHornICE_working_temp \
    ../benchmarks/ContextualHornICE_working_temp \
    ../benchmarks/ClassicalLLMHornICE_working_temp \
    ../benchmarks/ContextualLLMHornICE_working_temp \
    ../benchmarks/ContextualLLMHornICEFUZZ_working_temp \
    ../benchmarks/ClassicalLLMHornICEFUZZ_working_temp

echo "Running pipelines with parameter: $PARAM"

python3 contextualllmpipeline.py all
python3 classicalllmpipeline.py all

python3 run_all.py -m \
    ClassicalHornICE \
    ContextualHornICE \
    ClassicalLLMHornICE \
    ContextualLLMHornICE \
    -b all -p "$PARAM"
