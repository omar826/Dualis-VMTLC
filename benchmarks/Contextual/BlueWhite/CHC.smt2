(declare-rel inv (Int Int Int))
(declare-rel push (Int Int Int))
(declare-rel fail ())
(declare-var color Int)
(declare-var color1 Int)
(declare-var inserted_blue Int)
(declare-var inserted_blue1 Int)
(declare-var bcount Int)
(declare-var bcount1 Int)


(rule (=> (and (= inserted_blue1 0) (= bcount1 0)) (inv inserted_blue1 bcount1 color)))
(rule (=> (and (inv inserted_blue bcount color) (and (= color 0) (= inserted_blue 0)) (push color bcount bcount1) (= inserted_blue1 1)) (inv inserted_blue1 bcount1 color1)))
(rule (=> (and (inv inserted_blue bcount color) (not (and (= color 0) (= inserted_blue 0))) (= color 1) (push1 color bcount bcount1)) (inv inserted_blue bcount1 color1)))
(rule (=> (and (inv inserted_blue bcount color) (not (and (= color 0) (= inserted_blue 0))) (not (= color 1))) (inv inserted_blue bcount color1)))
(rule (=> (and (inv inserted_blue bcount color) (not (=> (= inserted_blue 1) (= bcount 1)))) fail))

(query fail :print-certificate true)
