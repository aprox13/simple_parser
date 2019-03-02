from graphbuilder import Graph

print(Graph.parse("'-1' > '0' {w(0,100):g(X_0)} '1' {u(20, 100):l(0, 100)} '2' {u(20, 100):n(1, 2, 3, 4, 5, 6, 7)}"))