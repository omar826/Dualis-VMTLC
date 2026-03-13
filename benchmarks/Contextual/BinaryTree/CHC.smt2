(declare-rel inv    (Int Bool Int))
(declare-rel insert (Int Int Int Bool Bool))
(declare-rel search (Int Int Bool Bool))
(declare-rel fail   ())

(define-fun True  () Bool true)
(define-fun False () Bool false)
(define-fun INT_MAX () Int 2147483647)

(declare-var isEmpty  Bool)
(declare-var isEmpty1 Bool)
(declare-var min      Int)
(declare-var min1     Int)
(declare-var n        Int)
(declare-var n1       Int)
(declare-var v        Int)
(declare-var ret1     Bool)

;;— initialization rule: if isEmpty1 is true, then inv(min1, isEmpty1, n) must hold
(rule
  (=> 
    isEmpty1
    (inv min1 isEmpty1 n)
  )
)

;;— loop‐body when n1 ≥ 0
(rule
  (=> 
    (and 
      (inv min isEmpty n)
      (>= n1 0)
      (insert n1 min min1 isEmpty isEmpty1)
    )
    (inv min1 isEmpty1 n1)
  )
)

;;— loop‐body when n1 < 0
(rule
  (=> 
    (and 
      (inv min isEmpty n)
      (< n1 0)
    )
    (inv min isEmpty n1)
  )
)

;;— post‐condition: if v<0 and search(...) yields ret1=true, then fail
(rule
  (=> 
    (and 
      (inv min isEmpty n)
      (< v 0)
      (search v min isEmpty ret1)
      ret1         ;; means (ret1 == true)
    )
    fail
  )
)

(query fail :print-certificate true)
