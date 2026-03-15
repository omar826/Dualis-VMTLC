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
docker run --rm -it dualis:latest
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

Run this script ``kickthetyres.py`` in the ``Dualis/scripts
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

### HornICE
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

## Step-by-Step instructions for evaluations
