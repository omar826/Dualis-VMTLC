(declare-var flag Int)
(declare-var flag1 Int)
(declare-var top Int)
(declare-var top1 Int)
(declare-var len Int)
(declare-var len1 Int)
(declare-var val Int)
(declare-rel push (Int Int Int Int Int))
(declare-rel inv (Int Int Int))
(declare-rel fail ())
(define-fun MAX () Int 128)


(rule (=> (and (= flag 1) (= len 0) (= top MAX) ) (inv top len flag)))
(rule (=> (and (inv top len flag) (= flag 1) (= val 1) (push val top len top1 len1) (= flag1 0)) (inv top1 len1 flag1)))
(rule (=> (and (inv top len flag) (not (= flag 1)) (= val 2) (push1 val top len top1 len1) (= flag1 1)) (inv top1 len1 flag1)))
(rule (=> (and (inv top len flag) (not (or (= len 0) (and (=> (= flag 0) (= top 1)) (=> (= flag 1) (= top 2)))))) fail))

(query fail :print-certificate true)