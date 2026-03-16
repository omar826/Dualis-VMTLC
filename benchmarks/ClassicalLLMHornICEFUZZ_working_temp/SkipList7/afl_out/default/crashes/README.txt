Command line used to find this crash:

afl-fuzz -i /home/omarmuhammad/Dualis/scripts/../benchmarks/ClassicalLLMHornICEFUZZ_working_temp/SkipList7/afl_in -o /home/omarmuhammad/Dualis/scripts/../benchmarks/ClassicalLLMHornICEFUZZ_working_temp/SkipList7/afl_out -t 2000 -p exploit -V 20 /home/omarmuhammad/Dualis/scripts/../benchmarks/ClassicalLLMHornICEFUZZ_working_temp/SkipList7/lower_bound_fuzz /home/omarmuhammad/Dualis/scripts/../benchmarks/ClassicalLLMHornICEFUZZ_working_temp/SkipList7/lower_boundCE.txt

If you can't reproduce a bug outside of afl-fuzz, be sure to set the same
memory limit. The limit used for this fuzzing session was 0 B.

Need a tool to minimize test cases before investigating the crashes or sending
them to a vendor? Check out the afl-tmin that comes with the fuzzer!

Found any cool bugs in open-source tools using afl-fuzz? If yes, please post
to https://github.com/AFLplusplus/AFLplusplus/issues/286 once the issues
 are fixed :)

