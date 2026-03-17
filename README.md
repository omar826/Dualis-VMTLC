## Getting Started Guide

This guide walks you through setting up the Docker environment and
performing a basic "kick-the-tires" test to verify the artifact
functions correctly. This initial phase is designed to take approx.
30 minutes to complete.

### 1. Prerequisites
* **Docker:** Ensure Docker is installed and running on your host
  machine.
* **OS Compatibility:** Compatible with Linux.

### 2. Environment Setup
Navigate to the directory (Dualis) of the artifact (where the `Dockerfile`
is located) and build the image:

```bash
docker image build \
  --build-arg USER_ID=$(id -u) \
  --build-arg GROUP_ID=$(id -g) \
  -t dualis:latest .
```
and run the image :

```bash
docker run -u $(id -u):$(id -g) -it --rm \
  -v $(pwd)/logs:/Dualis/logs \
  -v $(pwd)/benchmarks:/Dualis/benchmarks \
  --name Dualis \
  dualis:latest
```

### 3. Running Basic Tests

In this phase we run all the three learners, **LLM**, **HornICELLM**
and, **HornICE** on **BinaryTree** benchmark.

Before we proceed to execute the proof pipeline, following are the
details on the benchmark:

#### BinaryTree

The client uses an implementation of **BinaryTree** (library). It
executes a loop for `N` iterations (where `N` is chosen
nondeterministically), in which it inserts a value `n` (also chosen
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

### Synthesizing VMTLC proofs

Run the command
```
bash ./kickthetyres.sh
```
in the ``Dualis/scripts
directory`` to synthesize the specifications (Modular and Contextual)
with LLM, HornICELLM and HornICE as the learners for BinaryTree.

The output of the run is present in ``evaluation_summary.txt``.

Run
```
cat /Dualis/scripts/evaluation_summary.txt
```

to view the status of the run and the final specifications for
functions and loop invariants.

## Step-by-Step instructions for evaluations

In this section,

1. We try to reproduce Table 1 in the paper by 

	[-] Running all the learners, HornICE, HornICELLM and LLM for
    contextual and modular (classical) modes on benchmarks that did
    not __timeout__.
2. Also the numbers used in RQs to present our case.
   
   [-] Comparing with CVC5 as a learner.
   
   [-] Comparing with SeaHorn as automated verifier of library +
   client.
   
__Note : These steps take approximately 4-5 hrs to complete.__

### Running full evaluation script

Get in to ``/Dualis/scripts`` directory (ignore if already) using

```
cd /Dualis/scripts
```

Now, you are required to create a ```.env``` file using

```
touch /Dualis/.env
```
and enter the API-KEY that will be used by LLM (Gemini) and the format is,

```
API-KEY = "<alphanumric-string>"
```

and run the bash script

```
./full_evaluation.sh
```

__Note : We are running learners for 20 benchmarks at once. Please
make sure to give similar/more resources to get results in time. These
resources will be used by HornICE and HornICELLM learners__

After 4-5 hrs you will see that all the evaluation has ended.

After the evaluation run,

```
cat evaluation_.txt
```

to get an overview of the evaluation for all the learners across all
the benchmarks. This .txt file will contain results from table 1 in
the paper.

To add more **visibility** to the results that we have accumulated, we
 give th following set of useful commands for each learner. You could
 run them to get results as explained below.

### LLM

To run specific benchmarks of your interest for modular (classical)
specifications, run the following command.

```
```

Similarly for contextual specifications, run the following command.
```
```

Results of both the commands will be on the standard output (STDOUT).

We also show that the results that we manually whetted for LLM during
our runs are __equivalent__ to the ones produced in this run. To see that
run the following script (in ```/Dualis/scripts``` folder).

```
python check_implications.py
```


### HornICELLM

### HornICE



Note : We have run all the learner only on benchmarks that passed (did
not time out). But if you wish to run on all of them


Note : We have run all the learner only on benchmarks that passed (did
not time out). But if you wish to run on all of them 
