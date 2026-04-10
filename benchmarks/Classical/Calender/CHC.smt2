(declare-rel inv (Int Int))
(declare-rel insert (Int Int Int Int Int Int))
(declare-rel fail ())
(define-fun absl ((x Int)) Int (ite (>= x 0) x (- x)))
(define-fun INT_MIN () Int -129)
(declare-var len Int)
(declare-var len1 Int)
(declare-var ev1 Int)
(declare-var ev2 Int)
(declare-var maxDiff Int)
(declare-var maxDiff1 Int)


(rule (=> (and (= len1 0) (= INT_MIN maxDiff1)) (inv len1 maxDiff1)))
(rule (=> (and (inv len maxDiff) (>= ev1 0) (<= ev1 3) (>= ev2 0) (<= ev2 3) (< (absl (- ev1 ev2)) 2) (insert len len1 ev1 ev2 maxDiff maxDiff1)) (inv len1 maxDiff1)))
(rule (=> (and (inv len maxDiff) (not (and (>= ev1 0) (<= ev1 3) (>= ev2 0) (<= ev2 3) (< (absl (- ev1 ev2)) 2)))) (inv len maxDiff)))
(rule (=> (and (inv len maxDiff) (not (=> (> len 0)(< maxDiff 2)))) fail))

(query fail :print-certificate true)

//changes made: issue with order of < operation
