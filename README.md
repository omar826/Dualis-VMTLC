## Getting Started Guide

This guide walks you through setting up the Docker environment and
performing a basic "kick-the-tires" test to verify the artifact
functions correctly. This initial phase is designed to take less than
30 minutes to complete.

### 1. Prerequisites
* **Docker:** Ensure Docker is installed and running on your host
  machine.
* **OS Compatibility:** Compatible with Linux.

### 2. Environment Setup
Navigate to the directory (Dualis) of the artifact (where the `Dockerfile`
is located) and build the image:

```bash
docker image build -t dualis:latest .
```
and run the image :

```bash
docker run -it \
  -v $(pwd)/../logs:/Dualis/logs \
  -v $(pwd)/../benchmarks:/Dualis/benchmarks \
  --name Dualis \
  dualis:latest
```

### 3. Running Basic Tests

In this phase we run all the three learners, **LLM**, **HornICELLM**
and, **HornICE** on **BinaryTree** and **Stack** benchmarks.

Before we proceed to execute the proof pipeline, following are the
details on the Benchmarks:

>> BinaryTree

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

>> Stack

The client uses an implementation of **Stack** (library). It first
chooses a nondeterministic value `N` such that `N > 0`. In the first
loop, the client pushes the value `N` onto the stack `N` times while
incrementing the counter `c`. After this, the client repeatedly pops
elements from the stack until the stack becomes empty, incrementing
another counter `d` for every pop operation. Finally, the client
asserts that the number of pop operations performed is equal to `N`.

The abstract program is shown below.

'''
Stack st;
int c = 0, d = 0, N = *;

assume(N > 0)
while (c < n)
{
	st.push(n);
    c = c+1;
}

while (sl != 0) {
    st.pop();
    d = d+1;
}

assert (d == n)
'''

### Synthesizing VMTLC proofs

Run the command
```
python3 run_all.py -m \
ClassicalLLM \
ContextualLLM \
ClassicalHornICE \
ContextualHornICE \
ClassicalLLMHornICE \
ContextualLLMHornICE \
-b Stack BinaryTree -p 8
```
in the ``Dualis/scripts
directory`` to synthesize the specifications (Modular and Contextual)
with LLM, HornICELLM and HornICE as the learners for BinaryTree and
Stack.

```
```
the output of the run, showing the specifications is present in <>.

Following are the specifications synthesized for BinaryTree client
using LLM as the learner.

### LLM
## BinaryTree

**Modular**

```
insert(n) :=
search(v) :=
inv := 
```

## Contextual

```
insert(n) :=
search(v) :=
inv := 
```
Using HornICELLM,

### HornICELLM
## BinaryTree

**Modular**
```
insert(n) :=
search(v) :=
inv := 
```
**Contextual**
```
insert(n) :=
search(v) :=
inv := 
```
 and, finally using HornICE.
### HornICE
## BinaryTree

**Modular**
```
insert(n) :=
search(v) :=
inv := 
```

**Contextual**
```
insert(n) :=
search(v) :=
inv := 
```

And similarly for the Stack client.
### LLM
## Stack

**Modular**
```
insert(n) :=
search(v) :=
inv1 :=
inv2 :=
```

**Contextual**

```
push(n) := 
pop() :=
inv1 :=
inv2 :=
```

### HornICELLM
## Stack

**Modular**
```
push(n): (((sl1 - sl) <= 1) && ((sl1 - sl) > 0))
po(): ((((sl > (-1)) && (sl1 <= 0) && ((sl - sl1) <= 0)) || ((sl - sl1) > 0)) && ((sl - sl1) <= 1))
inv1: (((N - c) > (-1)) && ((sl - c) <= 0) && ((sl - c) > (-1)) && (d > (-1)) && (d <= 0))
inv2: ((((N - sl) - d) <= 0) && (((sl + d) - N) <= 0) && (d > (-1)))
```

**Contextual**

```
push(n) : (((sl1 - sl) <= 1) && ((sl1 - sl) > 0))
pop : (((sl - sl1) <= 1) && ((sl - sl1) > 0))
inv1 : (((d <= 0) && (d > (-1)) && (c <= 1) && ((c - sl) <= 0) && ((sl - c) <= 0) && (N > 0) && (N <= 1)) || (((N - c) > (-1)) && ((sl - c) <= 0) && ((c - sl) <= 0) && (d <= 0) && (d > (-1)) && (N > 1)))
inv2 : ((((N - sl) - d) <= 0) && (((sl + d) - N) <= 0) && (d > (-1)))
```

### HornICE
## Stack

**Modular**
```
push(n): (((sl - sl1) <= (-1)) && ((sl - sl1) > (-2)))
pop(): ((((sl > (-1)) && (sl <= 0) && ((sl - sl1) <= 0)) || ((sl - sl1) > 0)) && ((sl - sl1) <= 1))
inv1: (((((d - N) + sl) <= 0) && (((d - c) + sl) <= 0) && (((c - d) - sl) <= 0) && (d <= 0) && (N > 0) && (N <= 1)) || ((((d - c) + sl) <= 0) && (((d - N) + sl) <= 0) && (((c - d) - sl) <= 0) && (N > 1)))
inv2: ((((N - d) - sl) <= 0) && (((d - N) + sl) <= 0) && (((N - d) - sl) <= 1))
```

**Contextual**

```
push(n): (((sl1 - sl) <= 1) && ((sl1 - sl) > 0))
pop(): (((sl - sl1) <= 1) && ((sl - sl1) > 0))
inv1: (((N - c) > (-1)) && (d > (-1)) && (d <= 0) && ((sl - c) <= 0) && ((c - sl) <= 0) && (N > 0))
inv2: ((((N - sl) - d) <= 0) && (((sl + d) - N) <= 0) && (((N - sl) - d) <= 1) && (N > 0))
```

## Step-by-Step instructions for evaluations
