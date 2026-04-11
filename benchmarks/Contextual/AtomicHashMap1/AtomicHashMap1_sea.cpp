#include "../../SeaImpl/AtomicHashMapImpl.h"

extern int nd();

int main(int argc, char* argv[]) {
    HashTable ahm;
    int N = nd();
    int len = 0;
    int min = 0;
    int max = 0;
    int containsk = 0;

    __VERIFIER_assume(N > 0);

    int i = 0;
    while (i < N) {
        int k = i;
        int v = i;
        
        ahm.insert(k, v);

        len = ahm.len();
        min = ahm.minKey();
        max = ahm.maxKey();
        containsk = ahm.contains(k);

        v = i + 1;

        ahm.insert(k, v);

        len = ahm.len();
        min = ahm.minKey();
        max = ahm.maxKey();
        containsk = ahm.contains(k);

        i++;
    }

    int k = nd();
    __VERIFIER_assume(k >= 0 && k < N);
    
    int ret1 = ahm.find(k);

    sassert(ret1 != MIN and ret1 != MAX);

    return 0;
}
