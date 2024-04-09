\ Model Gallos
\ LP format - for model browsing. Use MPS format to capture full model detail.
Minimize
  0.5 x[0] + 0.75 x[1] + x[2]
Subject To
 R0: 0.1 x[0] + 0.25 x[1] + 0.4 x[2] >= 0.15
 R1: 0.1 x[0] + 0.25 x[1] + 0.4 x[2] <= 0.4
 R2: 0.5 x[0] + 0.2 x[1] + 0.1 x[2] >= 0.2
 R3: 0.5 x[0] + 0.2 x[1] + 0.1 x[2] <= 0.5
 R4: 0.3 x[0] + 0.5 x[1] + 0.1 x[2] >= 0.1
 R5: 0.3 x[0] + 0.5 x[1] + 0.1 x[2] <= 0.6
Bounds
End
