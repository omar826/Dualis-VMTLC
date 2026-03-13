(declare-rel inv (Int Int))
(declare-rel append (Int Int Int))
(declare-rel fail ())
(declare-var v Int)
(declare-var v1 Int)
(declare-var lmin Int)
(declare-var lmin1 Int)
(declare-var gmin Int)
(declare-var gmin1 Int)
(define-fun INT_MAX () Int 10)


(rule (=> (and (= gmin1 INT_MAX) (= lmin1 INT_MAX)) (inv lmin1 gmin1)))
(rule (=> (and (inv lmin gmin) (append v lmin lmin1) (= gmin1 (ite (< v gmin) v gmin))) (inv lmin1 gmin1)))
(rule (=> (and (inv lmin gmin) (not (= gmin lmin))) fail))

(query fail :print-certificate true)
