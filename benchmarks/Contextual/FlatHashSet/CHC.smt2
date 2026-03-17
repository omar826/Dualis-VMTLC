(declare-var N Int)
(declare-var size Int)
(declare-var len Int)
(declare-var len1 Int)
(declare-var i Int)
(declare-var i1 Int)
(declare-var min Int)
(declare-var min1 Int)
(declare-var max Int)
(declare-var max1 Int)
(declare-var containsv Int)
(declare-var containsv1 Int)
(declare-var v Int)
(declare-rel insert (Int Int Int Int Int Int Int Int Int))
(declare-rel erase (Int Int Int Int Int Int Int Int Int))
(declare-rel reserve (Int Int Int))
(declare-rel inv1 (Int Int Int Int Int Int))
(declare-rel inv2 (Int Int Int Int Int Int))
(declare-rel inv3 (Int Int Int Int Int Int))
(declare-rel fail ())
(define-fun MAX () Int -129)
(define-fun MIN () Int 128)
(define-fun is_valid ((x Int)) Bool (or (= x 1) (= x 0)))

(rule (=> (and (> N 0) (= len 0) (= i 0) (= min MIN) (= max MAX) (= containsv 0)) (inv1 i N len containsv min max)))

(rule (=> (and (inv1 i N len containsv min max) (is_valid containsv) (< i N) (= v i) (insert v len containsv min max len1 containsv1 min1 max1) (= i1 (+ i 1))) (inv1 i1 N len1 containsv1 min1 max1)))

(rule (=> (and (inv1 i N len containsv min max) (is_valid containsv) (not (< i N)) (= i1 0)) (inv2 i1 N len containsv min max)))

(rule (=> (and (inv2 i N len containsv min max) (is_valid containsv) (< i N) (= v i) (erase v len containsv min max len1 containsv1 min1 max1) (= i1 (+ i 1))) (inv2 i1 N len1 containsv1 min1 max1)))

(rule (=> (and (inv2 i N len containsv min max) (is_valid containsv) (not (< i N)) (reserve len N len1) (= i1 0)) (inv3 i1 N len containsv min max)))

(rule (=> (and (inv3 i N len containsv min max) (is_valid containsv) (< i N) (= v (+ i N)) (insert v len containsv min max len1 containsv1 min1 max1) (= i1 (+ i 1))) (inv3 i1 N len1 containsv1 min1 max1)))

(rule (=> (and (inv3 i N len containsv min max) (is_valid containsv) (not (< i N)) (not (= len N))) fail))

(query fail :print-certificate true)