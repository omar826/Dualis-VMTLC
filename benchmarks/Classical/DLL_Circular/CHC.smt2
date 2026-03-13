(declare-rel push (Int Int Int))
(declare-rel inv (Int Int))
(declare-rel fail ())
(declare-var val Int)
(declare-var val1 Int)
(declare-var max Int)
(declare-var max1 Int)


(rule (=> (and (= val1 0) (= max1 0)) (inv val1 max1)))
(rule (=> (and (inv val max) (< val 3) (= val1 (+ val 1)) (push val1 max max1)) (inv val1 max1)))
(rule (=> (and (inv val max) (>= val 3) (push val max max1)) (inv val max1)))
(rule (=> (and (inv val max) (push val max max1)) (inv val max1)))
(rule (=> (and (inv val max) (not (and (>= max 0) (<= max 3)))) fail))

(query fail :print-certificate true)
