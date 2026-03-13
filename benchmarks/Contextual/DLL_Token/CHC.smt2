(declare-rel push (Int Int Int Int Int))
(declare-rel inv (Int Int Int))
(declare-rel fail ())
(declare-var val1 Int)
(declare-var val Int)
(declare-var min Int)
(declare-var min1 Int)
(declare-var max Int)
(declare-var max1 Int)


(rule (=> (and (= val1 0) (= min1 0) (= max1 0)) (inv val1 min1 max1)))

(rule (=> (and (inv val min max) (push val min min1 max max1)) (inv val min1 max1)))

(rule (=> (and (inv val min max) (not (and (= min 0) (= max 0)))) fail))

(query fail :print-certificate true)
