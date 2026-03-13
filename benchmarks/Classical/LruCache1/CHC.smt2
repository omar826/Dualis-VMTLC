(declare-var N Int)
(declare-var size Int)
(declare-var len Int)
(declare-var len1 Int)
(declare-var i Int)
(declare-var i1 Int)
(declare-var containsmru Int)
(declare-var containsmru1 Int)
(declare-var containsk Int)
(declare-var mru Int)
(declare-var mru1 Int)
(declare-var k Int)
(declare-var v Int)
(declare-var ret1 Int)
(declare-rel insert_or_assign (Int Int Int Int Int Int Int Int Int Int))
(declare-rel find (Int Int Int))
(declare-rel inv1 (Int Int Int Int Int Int Int))
(declare-rel fail ())
(define-fun is_valid ((x Int)) Bool (or (= x 1) (= x 0)))
(define-fun MAX () Int 128)

(rule (=> (and (>= N 3) (= size N) (= len 0) (= i 0) (= containsmru 0) (= containsk 0) (= mru MAX) ) (inv1 i N len  mru size containsmru containsk)))
(rule (=> (and (inv1 i N len  mru size containsmru containsk) (is_valid containsmru) (< i N) (= k i) (= v i) (insert_or_assign k v len mru size containsmru len1 mru1 containsmru1 ret1) (= i1 (+ i 1))) (inv1 i1 N len1  mru1 size containsmru1 containsk)))
(rule (=> (and (inv1 i N len  mru size containsmru containsk) (is_valid containsmru) (is_valid containsk) (not (< i N)) (<= 0 k) (< k N) (find k containsk  mru1) (= mru1 MAX)) fail))

(query fail :print-certificate true)



((((containsmru <= 0) && ((N - i) > 0) && ((mru - i) > 8) && (size <= 3)) 
|| 
((i <= 0) && (containsmru <= 0) && ((i - len) <= 3) && (size > 3))) && ((size - N) <= 0) && (containsk <= 0) && (size > 2))


(((((((size <= 1) && (len <= 0)) || ((size <= 1) && (len > 0))) && (containsmru1 <= 0)) || ((((size <= 1) && (k <= (-3))) || ((size <= 1) && (k > (-3)))) && (containsmru1 > 0))) && (containsmru <= 0)) || (containsmru > 0))