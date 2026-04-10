# Table of Contents
* [Getting Started Guide](#getting-started-guide)
  * [Prerequisites](#prerequisites)
  * [Environment Setup](#environment-setup)
  * [LLM Configuration](#llm-configuration)
  * [VMTLC Proofs for BinaryTree](#vmtl-proofs-for-binarytree)
    * [BinaryTree Description](#binarytree-description)
	  * [Synthesizing VMTLC Proof](#synthesizing-vmtlc-proof)
* [Complete Evaluation](#complete-evaluation)
  * [Benchmarks & Parallel Execution](#benchmarks--parallel-execution)
  * [Running Full Evaluation Script](#running-full-evaluation-script)
  * [Learner: LLM](#learner-llm)
	* [Available Modes](#available-modes)  
    * [Log Contents (LLM)](#log-contents-llm)
  * [Learner: HornICELLM](#learner-hornicellm)
	* [Available Modes](#available-modes)
    * [Log Contents (HornICELLM)](#log-contents-hornicellm)
  * [Learner: HornICE](#learner-hornice)
    * [Available Modes](#available-modes)
    * [Log Contents (HornICE)](#log-contents-hornice)
  * [Using Fuzzer to test specific benchmarks of
    interest](#Using-Fuzzer-to-test-specific-benchmarks-of-interest)
  * [Old Logs](#old-logs)
  * [Comparing with CVC5 and SeaHorn](#comparing-with-CVC5-and-SeaHorn)
* [Use alternative tools in VMTLC framework](#using-alternativ-tools-in-vmtlc-framework)
  * [Tester](#tester)
  * [Learner](#learner)

## Getting Started Guide

This guide walks you through setting up the Docker environment and
performing a basic "kick-the-tyre" test to verify that the artifact
functions correctly. This phase takes approximately 30 minutes.

### Prerequisites
* **Docker:** Ensure Docker is installed and running on your host
  machine.
* **OS Compatibility:** Compatible with Linux.

### Environment Setup
Navigate to the artifact root directory (```/Dualis```), where the
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

It also contains prebuilt docker image as ``Dualis.tgz`` in the main
directory.

Dualis image can be loaded using,

```bash
docker load < Dualis.tar.gz
```

and can run it using the earlier run instruction.

### LLM Configuration
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

### VMTLC Proofs for Binarytree

In this phase all three learners, **LLM**, **HornICELLM** and,
**HornICE** on **BinaryTree** are executed on the benchmarks.

Before executing the VMTLC pipelines with these learners, we first
describe the BinaryTree benchmark executed by all the pipelines.

#### BinaryTree Description

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

#### Synthesizing VMTLC Proof

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
functions and loop invariants which were _adequate_ to prove the client
and were also passed _correct_ by the tester.

## Complete Evaluation

To reproduce the results from the paper, execute the
```fullevaluation.sh`` script. This step generates VMTLC proofs 43
benchmarks using prviously mentioned learners and takes approximately
__10-12 hours__.

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

while the Contextual BinaryTree directory has a client test harness as

```
BinaryTree_fuzz.cpp
```
, verification harness for Seahorn as,
```
BinaryTree_sea.cpp
```

and other files.

The evaluation is configured to run all pipelines on the benchmarks
that did not timeout in Table 1 of the paper.

With **LLM** as the learner, each benchmark is executed sequentially
for each pipeline (classical and contextual). In contrast, for
**HornICE** and **HornICELLM**, multiple benchmarks are executed in
parallel (configured to run 20 benchmarks simultaneously).

### Running Full Evaluation Script

In this section we undertake steps to back our claims in the paper.

1. This step reproduces Table 1 in the paper by:

	[-] Running all learners, HornICE, HornICELLM and LLM for
    contextual and modular (classical) pipelines on benchmarks that did
    not __timeout__.
2. Also the numbers used in RQs to present our case.
   
   [-] Comparing with CVC5.
   
   [-] Comparing with SeaHorn.
   
3. Note that we claim our manually vetted specifications are
   correct. We do not provide any additional guarantees; however, for
   the LLM pipelines, we perform an equivalence check between the
   previously obtained specifications and the newly generated ones.
   
__Note : These steps take approximately 10-12 hrs to complete.__

### Running full evaluation script

Run the following bash script

```
./fullevaluation.sh #processors (default is 20)
```

__Note : Evaluation is carried by running learners on 20 benchmarks in
parallel. Ensure that sufficient CPU resources (≈20 cores) are
available to obtain results within the expected time.__

After 10-12 hrs you will see that the evaluation has ended.

After the evaluation run, the compiled concise results are captured in
```evaluation_summary.txt```.

```
cat evaluation_summary.txt
```
to view results.

Run the script ```summary_table.py``` which builds a summary table
using ```evaluation_summary.txt```.

```
python3 summary_table.py
```

This provides an overview of all the learners across all the
benchmarks. The evaluation_summary.txt file will contain results from
table 1 in the paper (without the time measurement).

During evaluation, intermediate files for each pipeline are stored in
the `pipeline_working_temp` directory. For example, one such directory
is `ContextualHornICE_working_temp`.

Each pipeline working directory contains benchmark-specific
subdirectories. These subdirectories include fuzzer results, seeds,
compiled fuzzer harness executables, and generated specifications
produced during and after the learning process.

These directories are deleted before every full evaluation run.

You can monitor the progress of the evaluation by opening another
terminal in the Docker container and running:

```
docker exec -it Dualis /bin/bash
```
Then, execute:

```cat evaluation_summary.txt```

to view the current status of the run.

To provide better visibility into the accumulated results, we list a
set of useful commands for each learner below. You can execute these
commands to obtain detailed results as described in the following
sections.

### Learner:LLM

To run specific benchmarks of interest for modular (classical)
specifications, execute (Pass the exact names of the benchmarks you want to test as space-separated arguments):

```
python3 classicalllmpipeline.py BinaryTree Stack
```


Similarly, for contextual specifications, execute:

```
python3 contextualllmpipeline.py BinaryTree Stack
```
The results are printed to standard output (STDOUT).

Since LLM outputs may vary across runs, we verify that the generated
specifications are equivalent to previously vetted ones. To perform
this equivalence check, run the following script (from the
`/Dualis/scripts` directory):

```
python check_implications.py
```
The report is generated at: ```/Dualis/scripts/implication_report.txt```.

You can view the contents using:
```
cat /Dualis/scripts/implication_report.txt
```

#### Log Contents

The logs for these runs are located in:

- `/Dualis/logs/ClassicalLLMPipeline_logs` (modular/classical), and
- `/Dualis/logs/ContextualLLMPipeline_logs` (contextual)

Each directory contains a subdirectory for each benchmark. For example:

```
BinaryTree
  --> conversation_history.json
  --> final_cpp_specs.txt
```

- `conversation_history.json` contains the full interaction with the LLM.
- `final_cpp_specs.txt` contains the final learned specifications for
  functions and loop invariants.

An example:

```
insert
((isEmpty1 == 0) && (min1 == (isEmpty == 1 ? n : (n < min ? n : min))))

search
((!(isEmpty == 1) || (ret1 == 0)) && (!((isEmpty == 0) && (ret1 == 1)) || (v >= min)))
```

#### LLM Prompt Templates

The prompt templates used for synthesizing contextual and modular
specifications are located in:

- `template_contextual.txt` is used for `ContextualLLMPipeline`
- `Template.txt` is used for `ClassicalLLMPipeline`

### Learner:HornICELLM
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

The logs for these runs are located in:

- `/Dualis/logs/ClassicalLLMHornICEPipeline_logs` (modular/classical), and
- `/Dualis/logs/ContextualLLMHornICEPipeline_logs` (contextual)

Within each pipeline log directory, navigate to the subdirectory
corresponding to the benchmark of interest (e.g., `BinaryTree`). The
following files can be found:

```
  --> BinaryTree_pipeline.log - contains all the external iterations
  --> internal_BinaryTree, this is a directory that hosts logs of internal iterations.
```
- **External (E) iterations** capture the interaction between the
  tester and the learner.
- **Internal (I) iterations** capture the interaction between the
  learner and the verifier.

#### LLM Prompt Templates

The prompt templates used to construct the initial set of
expressions—over which contextual and modular specifications are
synthesized—are located in:

`/Dualis/script/templates`

- `template_express_contextual.txt` is used for `ContextualLLMHornICEPipeline`
- `Template_expression.txt` is used for `ClassicalLLMHornICEPipeline`

### Learner: HornICE

To run specific benchmarks of interest for modular (classical)
specifications, use:

```
python3 run_all.py -m ClassicalHornICE -b Stack BinaryTree -p 2
```
Similarly, for contextual specifications:

```
python3 run_all.py -m ContextualMHornICE -b Stack BinaryTree -p 2
```

Results will be available in:

- `/Dualis/logs/ClassicalHornICEPipeline_Logs`
- `/Dualis/logs/ContextualHornICEPipeline_Logs`

respectively.

#### Available Modes
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
The logs for these runs are located in:

- `/Dualis/logs/ClassicalHornICEPipeline_logs` (modular/classical), and
- `/Dualis/logs/ContextualHornICEPipeline_logs` (contextual)

Within each pipeline log directory, navigate to the subdirectory for
the benchmark of interest (e.g., `BinaryTree`). The following files
can be found:

```
  --> BinaryTree_pipeline.log - contains all the external iterations
  --> internal_BinaryTree, this is a directory that hosts logs of internal iterations.
```
- **External (E) iterations** capture the interaction between the tester and the learner.
- **Internal (I) iterations** capture the interaction between the learner and the verifier.

### Using Fuzzer to test specific benchmarks of interest

If you want to manually interact with the fuzzer, you can invoke AFL++
directly on the compiled C++ harnesses.

This should be done only after running one of the pipelines on a
benchmark, for example:

```
python3 run_all.py -m ContextualLLMHornICE -b Stack BinaryTree -p 2
```

The compiled binaries and fuzzing artifacts are stored in the
temporary working directory corresponding to the selected mode and
benchmark. For example:

```
cd /Dualis/benchmarks/ContextualLLMHornICE_working_temp/BinaryTree
```
Run the following commands to start AFL++:

```
export AFL_SKIP_CPUFREQ=1
export AFL_I_DONT_CARE_ABOUT_MISSING_CRASHES=1
export AFL_LLVM_CMPLOG=1

afl-fuzz -i afl_in -o afl_out -t 2000 -p exploit ./BinaryTree_fuzz cex.txt
```

This uses the same parameters as the pipeline (a 2000 ms execution
timeout per run ), but enables the interactive AFL++ UI in the
terminal.

While the fuzzer is running, the standard AFL++ status screen is
displayed. Monitor the **"saved crashes"** metric in the top-right
corner.

After terminating the fuzzer, you can inspect any discovered
counterexamples (crashes) by navigating to:

```
ls -l afl_out/default/crashes/
```

### Old Logs

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

## Using alternative tools in VMTLC framework

We could use other alternative tools for tester and learner.

### Tester

Dualis currently uses AFL++. However, other fuzzers such as
**libfuzzer** can be integrated with minimal changes to the fuzz
harnesses and the script file, ``chcverifynfuzz.py``.

**Changes to harnesses** : Navigate to the ``benchmarks`` directory
  which contains two sub-directories: ``Contextual`` and
  ``Classical``. Each contains benchmark-specific directories.
  
- In ``Classical``, each benchmark directory includes files of the
  form ``<function_name>_fuzz.cpp``, which serve as per-function
  fuzz harnesses for testing modular contracts. These can be adapted
  to work with alternative fuzzers.

- In ``Contextual``, each benchmark directory contains a file of the
  form ``<benchmark_name>_fuzz.cpp``, which should be modified
  similarly.

Both harnesses rely on a shared implementation under
``benchmarks/FuzzImpl``, which provides utilities to construct data
structure states (in a context-insensitive manner) for testing
synthesized modular contracts.

**Changes to the script file** The compilation and fuzzing is
implemented in ``Dualis/scripts/chcverifynfuzz.py``. The base class
``BasePipeline`` defines a method ``run_fuzz`` that handles harness
compilation and fuzzing using AFL++.

To integrate another fuzzer, extend this class by adding a new method
that invokes the desired fuzzer and generates counterexamples in the
expected format at the following files:
- ``<benchmark_name>_CE.txt`` for contextual pipelines
- ``<function_name>_CE.txt`` for modular pipelines

### Learner

The interactions with the LLM are heavily abstracted. Dualis does not
rely on model-specific features, it relies purely on text-in/text-out
prompting.

**How to switch**: Navigate to the pipeline scripts
(classicalllmpipeline.py or contextualllmpipeline.py). Locate the
get_gemini_definitions() function call in get_llm_response and
replace it with an equivalent function for any other LLM provider
SDK.

**Prompts**: The prompt templates located in scripts/templates/ are
model agnostic and will work out-of-the-box with any modern model.


## Adding a New Benchmark

## Scripts

## Artifact Availability
