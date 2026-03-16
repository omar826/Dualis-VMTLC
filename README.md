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

## step-by-Step instructions for evaluations
