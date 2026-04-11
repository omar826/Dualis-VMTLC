#include "../../SeaImpl/AtomicHashMapImpl.h"

extern int nd();

int main(int argc, char* argv[]) {
    HashTable ahm;
    int N = nd();
    int len, min, max, containsk;
    __VERIFIER_assume(N >= 0);

    int i = 0;
    while (i < N) {
        int k = i;
        int v = i;
        
        ahm.insert(k, v);

        len = ahm.len();
        min = ahm.minKey();
        max = ahm.maxKey();
        containsk = ahm.contains(v);

        i++;
    }

    i = 0;
    while (i < N) {
        int k = i;
        int v = i;

        ahm.insert(k, v);

        len = ahm.len();
        min = ahm.minKey();
        max = ahm.maxKey();
        containsk = ahm.contains(v);

        i++;
    }

    // Find operation
    int k = nd();
    __VERIFIER_assume(k != min && k != max && k >= 0 && k < N);
    
    int ret = ahm.find(k);

    printf("ret = %d", ret);

    sassert(ret != MIN && ret1 != MAX);
    return 0;
}
