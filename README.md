# Table of Contents
* [Getting Started Guide](#getting-started-guide)
  * [Prerequisites](#prerequisites)
  * [Environment Setup](#environment-setup)
  * [Running Basic Tests](#running-basic-tests)
    * [BinaryTree](#binarytree)
  * [Learning specifications for a VMTLC Proof](#synthesizing-vmtlc-proof)
* [Step-by-Step Instructions for Evaluations](#step-by-step-instructions-for-evaluations)
  * [Benchmarks & Parallel Execution](#benchmarks--parallel-execution)
  * [Running Full Evaluation Script](#running-full-evaluation-script)
  * [Learner: LLM](#learner-llm)
    * [Log Contents (LLM)](#log-contents-llm)
  * [Learner: HornICELLM](#learner-hornicellm)
    * [Log Contents (HornICELLM)](#log-contents-hornicellm)
  * [Learner: HornICE](#learner-hornice)
    * [Log Contents (HornICE)](#log-contents-hornice)
  * [Comparing with CVC5 and SeaHorn](#comparing-with-CVC5-and-SeaHorn)

## Getting Started Guide

This guide walks you through setting up the Docker environment and
performing a basic "kick-the-tyre" test to verify that the artifact
functions correctly. This phase takes approximately 30 minutes.

### Prerequisites
* **Docker:** Ensure Docker is installed and running on your host
  machine.
* **OS Compatibility:** Compatible with Linux.

### Environment Setup
Navigate to the artifact root directory (```/Dualis``), where the
`Dockerfile` is located. Then build the image:

```bash
docker image build \
  --build-arg USER_ID=$(id -u) \
  --build-arg GROUP_ID=$(id -g) \
  -t dualis:latest .
```
and run the container :

```bash
docker run -u $(id -u):$(id -g) -it --rm \
  -v $(pwd)/logs:/Dualis/logs \
  -v $(pwd)/benchmarks:/Dualis/benchmarks \
  --name Dualis \
  dualis:latest
```

### LLM Configuration (.env)
Before running the evaluation pipeline with the LLM learner, you must
provide a Gemini API key.

Navigate to the ``/Dualis/scripts`` directory (skip if already there):

```
cd /Dualis/scripts
```


Add your GEMINI API_KEY to the .env file by replacing the string
"alphanumeric-string-here" with the actual key.

```
API_KEY = "alphanumeric-string-here"
```

**Note : API_KEY will be shared with the Artifact Reviewers via the AEC
chairs.**

### Running Basic Tests (kick the tyres)

In this phase all three learners, **LLM**, **HornICELLM** and,
**HornICE** on **BinaryTree** are executed on the benchmarks.

Before we proceed to execute the proof pipeline, following are the
details on the benchmark:

#### BinaryTree

The client uses an implementation of **BinaryTree** (library). It
executes a loop for `N` iterations, where `N` is chosen
nondeterministically, in which it inserts a value `n` (also chosen
nondeterministically) only if it is non-negative (`n >= 0`). After the
loop, it searches for a value `v` (chosen nondeterministically) and
asserts that the returned value `ret` is always `false`. The abstract
program is shown below.

```
BinaryTree bt;

while(*) {
    int n;
    if (n >= 0) {
        bt.insert(n);
    }
}

int v = *;
assume(v < 0);
ret = bt.search(v)
assert (ret == false);
```

#### Synthesizing VMTLC proofs

Run the following command
```
bash ./kickthetyres.sh
```

in the ``Dualis/scripts``` directory to synthesize the specifications
(Modular and Contextual) with LLM, HornICELLM and HornICE as the
learners for BinaryTree.

The output of the run is located in ``evaluation_summary.txt``.

Run
```
cat /Dualis/scripts/evaluation_summary.txt
```

to view the status of the run and the final specifications for
functions and loop invariants.

## Full Evaluation

To reproduce the results from the paper, execute the full evaluation
script. This process covers 43 benchmarks and takes approximately __7-8
hours__.

### Benchmarks & Parallel Execution

We have a set of 43 benchmarks for which we give VMTLC proofs using
Modular (Classical) and Contextual Specifications.

Here are the list of benchmarks
```
        "AlternatingList", "AtomicHashMap1", "AtomicHashMap2", "AtomicHashMap3",
        "AtomicHashMap4", "AtomicHashMap5", "AtomicLinkedList1", "AtomicLinkedList2",
        "BinaryHeap1", "BinaryHeap2", "BinaryTree", "BlueWhite", "Calender",
        "DLL_Circular", "DLL_Token", "FlatHashMap1", "FlatHashMap2", "FlatHashMap3",
        "FlatHashMap4", "FlatHashSet", "LruCache1", "Max", "Min", "Multimap1",
        "Multimap2", "Multiset1", "Multiset2", "NormalFilterQueue",
        "PriorityFilterQueue", "ProcessQueue", "RedBlackTree", "SkipList1",
        "SkipList2", "SkipList3", "SkipList4", "SkipList5", "SkipList6",
        "SkipList7", "Stack", "StockOrder", "TokenBucket1", "TokenBucket2", "TokenBucket3"
```

Benchmarks are located in ```/Dualis/benchmarks``` under
```Contextual``` and ```Classical``` directories.

Under these directories, each benchmark has a sub-directory. For
example, BinaryTree directory (under Classical) has following files :

```
Abstract.txt    - abstract client program
Attributes.txt  - derived and primary attributes for HornICELLM learner
BinaryTree.smt2 - CHC file for HornICE, HornICELLM and LLM 
BinaryTree.sy   - Constraint file for CVC5.
in              - fuzzer seeds
insert_fuzz.cpp - fuzzer harness (for each function called in the client)
llm_definitions.py - LLM specifications for verifier
validity_check_gen_ds.py - verifier (z3 based) for LLM.
```

while the Contextual BinaryTree directory has a single client test harness as

```
BinaryTree_fuzz.cpp
```
and verification harness for Seahorn as,
```
BinaryTree_sea.cpp
```

along with other files.

We have configured the evaluation for all the pipelines to run on the
benchmarks that did not timeout as per Table1 in the paper.

With LLM as the learner each benchmark for each pipeline (classical
and contextual) is executed sequentially, while for HornICE and
HornICELLM several applications are executed in parallel (configured to run 20
applications in parallel).

### Running the Full Evaluation Script

In this section,

1. This step reproduces Table 1 in the paper by:

	[-] Running all learners, HornICE, HornICELLM and LLM for
    contextual and modular (classical) pipelines on benchmarks that did
    not __timeout__.
2. Also the numbers used in RQs to present our case.
   
   [-] Comparing with CVC5.
   
   [-] Comparing with SeaHorn.
   
__Note : These steps take approximately 8-10 hrs to complete.__

### Running full evaluation script

and run the bash script

```
./fullevaluation.sh #processors (default is 20)
```

__Note : Evaluation is carried by running learners on 20 benchmarks in
parallel. Ensure that sufficient CPU resources (≈20 cores) are
available to obtain results within the expected time.__

After 8-10 hrs you will see that the evaluation has ended.

After the evaluation run,

```
cat evaluation_summary.txt
```

This provides an overview of all the learners across all the
benchmarks. The evaluate_summary.txt file will contain results from
table 1 in the paper.

During the evaluation for each pipeline, the intermediate temporary
files are located in ```pipeline_working_temp```. For example, one
such folder can be ```ContextualHornICE_working_temp```. These
benchmark-specific directories in each pipeline working temp folder will
have fuzzer results, seeds, executables of fuzzer harness and
generated specs when learning is in progress and when it ends. These
directories are deleted before every full evaluation.

Also you can view the status of the run by spawning another terminal
in docker like,

```
docker exec -it Dualis /bin/bash
```
and checking the ```evaluation_summary.txt```.

To add more **visibility** to the results we have accumulated, we provide
 the following set of useful commands for each learner. You could run
 them to get results as explained below.

### LLM

To run specific benchmarks of your interest for modular (classical)
specifications, run the following command.

```
python3 classicalllmpipeline.py BinaryTree Stack
```

Similarly for contextual specifications, run the following command.
```
python3 contextualllmpipeline.py BinaryTree Stack
```

Results are printed to standard output (STDOUT).

Since LLM outputs may vary across runs, we verify that the generated
specifications are equivalent to previously vetted ones. To check the
equivalence execute the following script (in ```/Dualis/scripts```
folder)

```
python check_implications.py
```
to see a report at ```/Dualis/scripts/implication_report.txt```.

```
cat /Dualis/scripts/implication_report.txt
```
to see the contents.

#### Log Contents
The logs for this run are located in 

```/Dualis/logs/ClassicalLLMPipeline_logs``` for modular (classical) and,

```/Dualis/logs/ContextualLLMPipeline_logs``` for contextual.

Each directory contains a dedicated sub-directory for each benchmark. For example,

```
BinaryTree
  --> conversation_history.json
  --> final_cpp_specs.txt
```

the ```conversation_history.json``` file full conversation with the
LLM and the ```final_cpp_specs.txt``` contains the final learned
specifications for loop invariants and functions for example,

```
insert
((isEmpty1 == 0) && (min1 == (isEmpty == 1 ? n : (n < min ? n : min))))

search
((!(isEmpty == 1) || (ret1 == 0)) && (!((isEmpty == 0) && (ret1 == 1)) || (v >= min)))
```

#### LLM Prompt Templates

The prompt templates used for synthesizing contextual and modular
specifications are given in ```/Dualis/script/templates```.

1. ```template_contextual.txt``` is used for
   ```ContextualLLMPipeline``` and

2.```Template.txt``` is used for ```ClassicalLLMPipeline```.


### HornICELLM
To run specific benchmarks of your interest for modular (classical)
specifications, run the following command.

```
python3 run_all.py -m ClassicalLLMHornICE -b Stack BinaryTree -p 2
```

Similarly for contextual specifications, run the following command.
```
python3 run_all.py -m ContextualLLMHornICE -b Stack BinaryTree -p 2
```

Results will be available in
```/Dualis/logs/ClassicalLLMHornICEPipeline_Logs``` and
```/Dualis/logs/ContextualLLMHornICEPipeline_Logs``` respectively.

Following are all possible modes,

```
'ClassicalHornICE',
'ClassicalLLMHornICE',
'ContextualHornICE',
'ContextualLLMHornICE',
'ClassicalCVC5',
'ContextualCVC5',
'ContextualSeaHorn'
```

#### Log Contents
The logs for this run are located in 

```/Dualis/logs/ClassicalLLMHornICEPipeline_logs``` for modular (classical) and,

```/Dualis/logs/ContextualLLMHornICEPipeline_logs``` for contextual.

Under those pipeline log folder for an application of interest look
for the following files for BinaryTree.

```
  --> BinaryTree_pipeline.log - contains all the external iterations
  --> internal_BinaryTree, this is a directory that hosts logs of internal iterations.
```

External (E) iterations capture the interaction of tester, learner
while Internal (I) iterations capture the interaction between learner
and verifier.

#### LLM Prompt Templates

The prompt templates used for building initial set of expressions over
which contextual and modular specifications are synthesized are given
in ```/Dualis/script/templates```.

1. ```template_express_contextual.txt``` is used for
   ```ContextualLLMHornicePipeline``` and

2.```Template_expression.txt``` is used for
```ClassicalLLMHornICEPipeline```.


### HornICE

To run specific benchmarks of your interest for modular (classical)
specifications, run the following command.

```
python3 run_all.py -m ClassicalHornICE -b Stack BinaryTree -p 2
```

Similarly for contextual specifications, run the following command.
```
python3 run_all.py -m ContextualMHornICE -b Stack BinaryTree -p 2
```

Results will be available in
```/Dualis/logs/ClassicalHornICEPipeline_Logs``` and
```/Dualis/logs/ContextualHornICEPipeline_Logs``` respectively.

Following are all possible modes,

```
'ClassicalHornICE',
'ClassicalLLMHornICE',
'ContextualHornICE',
'ContextualLLMHornICE',
'ClassicalCVC5',
'ContextualCVC5',
'ContextualSeaHorn'
```

#### Log Contents
The logs for this run are located in 

```/Dualis/logs/ClassicalHornICEPipeline_logs``` for modular (classical) and,

```/Dualis/logs/ContextualHornICEPipeline_logs``` for contextual.

Under those pipeline log folder for an application of interest look
for the following files for BinaryTree.

```
  --> BinaryTree_pipeline.log - contains all the external iterations
  --> internal_BinaryTree, this is a directory that hosts logs of internal iterations.
```

External (E) iterations capture the interaction of tester, learner
while Internal (I) iterations capture the interaction between learner
and verifier.

### Using Fuzzer to test specific benchmarks of interest

If you want to manually interact with the fuzzer, you can invoke AFL++
directly on the compiled C++ harnesses.

This should be done only after running any of the pipelines on any of
the benchmarks like for example,

```
python3 run_all.py -m ContextualLLMHornICE -b Stack BinaryTree -p 2
```

The compiled binaries and fuzzing artifacts are stored in the
temporary working directory for the specific mode and benchmark.

```
cd /Dualis/benchmarks/ContextualLLMHornICE_working_temp/BinaryTree
```

Run the following command to start AFL++ directly. This command uses
the same parameters our pipeline uses (a 2000ms execution timeout per
run and the exploit power schedule), but allows the interactive UI to
render in your terminal:

```
export AFL_SKIP_CPUFREQ=1
export AFL_I_DONT_CARE_ABOUT_MISSING_CRASHES=1
export AFL_LLVM_CMPLOG=1

afl-fuzz -i afl_in -o afl_out -t 2000 -p exploit ./BinaryTree_fuzz cex.txt
```

While the fuzzer is running, you will see the standard AFL++ status
screen. Monitor the "saved crashes" metric in the top right.

Once you terminate the fuzzer, you can manually inspect any
counterexamples (crashes) it found by navigating to the output
directory:

```
ls -l afl_out/default/crashes/
```

### Old Logs (Precomputed Results)

To compare your fresh runs against our original results,
you can review the pre-computed logs. 

These are located in:

```
/Dualis/logs_old
```
and the folders are

```
ClassicalLLMPipeline_logs
ClassicalLLMHornICEPipeline_Logs 
ClassicalLLMHornICEFUZZPipeline_Logs 
ClassicalHornICEPipeline_Logs 
ClassicalCVC5Pipeline_Logs 
ContextualCVC5Pipeline_Logs 
ContextualHornICEPipeline_Logs 
ContextualLLMHornICEFUZZPipeline_Logs 
ContextualLLMHornICEPipeline_Logs 
ContextualSeaHorn 
ContextualLLMPipeline_logs 
ContextualSeaHornPipeline_Logs 
kick_the_tyres_old_logs - kick the tyres logs
Vetted_Specs - log contains vetted specs due LLM
```

### Comparing with CVC5 and SeaHorn

In this section we evaluate the benchmarks to evaluate whether,

1. CVC5 can successfully synthesize specs and produce a VMTLC proof.
2. SeaHorn can successfully prove client+library for the assertion.

To run these, execute the following command from within the ```/Dualis/scripts``` directory
```
 python3 run_all.py -m \
     ContextualSeaHorn \
     ContextualCVC5 \
     ClassicalCVC5 \
     -b all -p 20
```

#### Locating the results

Once the execution finishes, the script generates quick-read text
files in ```/Dualis/scripts```. These files contain a list of the
benchmarks run and a simple Yes or No regarding whether the tool
succeeded.

For CVC5: Open cvc5_summary.txt to see if the specifications were
successfully generated.

For SeaHorn: Open seahorn_summary.txt to see if the proofs were
successfully generated Result: UNSAT (proof successful) or SAT
(counterexample found).

If you wish to inspect the exact stdout/stderr, tracebacks, or the
precise timeout points for any individual run, detailed logs are saved
in the logs directory located one level up from the script.

The logs are organized by mode. Navigate to the following directories:
```
 ../logs/ClassicalCVC5Pipeline_Logs/
 ../logs/ContextualCVC5Pipeline_Logs/
 ../logs/ContextualSeaHornPipeline_Logs/
```

Inside these folders, you will find an individual text file for each
benchmark (e.g., Stack_pipeline.log). These files contain the exact
command executed, the raw terminal output from the solver, and the
total pipeline duration.
