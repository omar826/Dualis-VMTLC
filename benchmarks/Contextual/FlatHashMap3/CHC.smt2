(declare-var N Int)
(declare-var i Int)
(declare-var i1 Int)
(declare-var i_old Int)
(declare-var containsk Int)
(declare-var containsk1 Int)
(declare-var len Int)
(declare-var len1 Int)
(declare-var flag Int)
(declare-var flag1 Int)
(declare-var ret Int)
(declare-var ret1 Int)
(declare-var k Int)
(declare-var v Int)
(declare-rel insert (Int Int Int Int Int Int))
(declare-rel erase (Int Int Int Int Int))
(declare-rel inv1 (Int Int Int Int))
(declare-rel inv2 (Int Int Int Int Int Int))
(declare-rel fail ())
(define-fun is_valid ((x Int)) Bool (or (= x 1) (= x 0)))


(rule (=> (and (> N 0) (= i 0) (= containsk 0) (= len 0)) (inv1 i N len containsk)))

(rule (=> (and (inv1 i N len containsk) (is_valid containsk) (< i N) (= k i) (= v i) (insert k v len containsk len1 containsk1) (= i1 (+ i 1))) (inv1 i1 N len1 containsk1)))

(rule (=> (and (inv1 i_old N len containsk) (is_valid containsk) (not (< i_old N)) (= i 0) (= flag 1)) (inv2 i N len containsk flag ret)))

(rule (=> (and (inv2 i N len containsk flag ret) (is_valid containsk) (< i N) (= flag 1) (= k i) (erase k len flag len1 ret1) (= i1 (+ i 1)) (= flag1 (- 1 flag))) (inv2 i1 N len1 containsk flag1 ret1)))

(rule (=> (and (inv2 i N len containsk flag ret) (is_valid containsk) (< i N) (= flag 0) (= i1 (+ i 1)) (= flag1 (- 1 flag))) (inv2 i1 N len containsk flag1 ret)))

(rule (=> (and (inv2 i N len containsk flag ret) (is_valid containsk) (not (< i N)) (not (=>(flag == 0)(= ret (- N 1))))) fail))

(query fail :print-certificate true)