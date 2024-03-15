The meaning of the various observations, labels and problem constraints are given below.4

O : Observation
L : Label
C : Content

Y : Yellow
W : White
B : Both 

Implications of observations:
• OnY => CnY ∨ CnB ∀ n, n = 1,2,3
• OnW => CnW ∨ CnB ∀ n, n = 1,2,3
Implications of labelling:
• LnY => ¬ CnY ∀ n, n = 1,2,3
• LnW => ¬ CnW ∀ n, n = 1,2,3
• LnB => ¬ CnB ∀ n, n = 1,2,3
Implication of the constraint that there is only one box of each color:
• C1Y ∨ C1W ∨ C1B
• C2Y ∨ C2W ∨ C2B
• C3Y ∨ C3W ∨ C3B
Implication of the constraint that there are no two boxes of the same color:
• C1p => (¬ C2p) ∧ (¬ C3p) ∀ p, p = Y,W,B
• C2p => (¬ C3p) ∧ (¬ C1p) ∀ p, p = Y,W,B
• C3p => (¬ C1p) ∧ (¬ C2p) ∀ p, p = Y,W,B
Proof that box 2 must contain white balls:
• from O3Y derive C3Y ∨ C3B by Modus Ponens . . . (I)
• from L3B derive ¬ C3B by Modus Ponens . . . (II)
• from (I) and (II), derive C3Y by Resolution . . . (III)
• from (III), derive (¬ C1Y) ∧ (¬ C2Y) by Modus Ponens . . . (IV)
• from O1Y, derive CnY ∨ CnB by Modus Ponens . . . (V)
• from (IV), derive (¬ C1Y) by Conjunction Elimination . . . (VI)
• from (V) and (VI), derive C1B by Resolution . . . (VII)
• from O2W, derive C2W ∨ C2B by Modus Ponens . . . (VIII)
• from (VII), derive (¬ C2B) ∧ (¬ C3B) by Modus Ponens . . . (IX)
• from (IX), derive (¬ C2B) by Conjunction Elimination . . . (X)
• from (VIII) and (X), derive C2W by Resolution . . . [Proved]