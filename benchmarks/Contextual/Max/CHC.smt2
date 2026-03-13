(declare-rel inv (Int Int))
(declare-rel append (Int Int Int))
(declare-rel fail ())
(declare-var v Int)
(declare-var lmax Int)
(declare-var lmax1 Int)
(declare-var gmax Int)
(declare-var gmax1 Int)
(define-fun INT_MAX () Int 10)
(define-fun INT_MIN () Int (- 10))


(rule (=> (and (= gmax1 INT_MIN) (= lmax1 INT_MIN)) (inv lmax1 gmax1)))
(rule (=> (and (inv lmax gmax) (append v lmax lmax1) (= gmax1 (ite (> v gmax) v gmax))) (inv lmax1 gmax1)))
(rule (=> (and (inv lmax gmax) (not (= gmax lmax))) fail))

(query fail :print-certificate true)
