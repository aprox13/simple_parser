Add edge between 1 and 2: ___'1' > '2'___ or ___'1' {PARAMS} '2'___ where:
__'?'__ -  name of vertex
**PARAMS**:
___l(min, max)___ - length of path from min to max, default ___l(1, 1)___
___g(name)___ - genome name, default ___Graph.name_var + graphbuilder.Graph.var_index___
___w(min, max)___ - weight of path from min to max, default ___w(1, -1)___
___u(min, max)___ - count of uniq paths from min to max, default ___u(0, -1)___
___n(ids...)___ - vertices that must contain the path  ___n([])___

Parameters separator ___':'___
F.e.: ___'-1' > '0' {w(0,100):g(X_0)} '1' {u(20, 100):l(0, 100)} '2' {u(20, 100):n(1, 2, 3, 4, 5, 6, 7)}___

___Graph.parse(str)___ return all edges in this fromat: ___[from, to, genome, weights, lengths, n, uniq]___, split by lenght ( is this edge shows path or simple edge)


***Some format***:
___'1'>'2'; '2' > '3';___ -> ___[[["'1'", "'2'", 'X_0', (1, -1), (1, 1), [], (0, -1)], ["'2'", "'3'", 'X_1', (1, -1), (1, 1), [], (0, -1)]], []]___
___
___'-1' > '0' {w(0,100):g(X_0)} '1' {u(20, 100):l(0, 100)} '2' {u(20, 100):n(1, 2, 3, 4, 5, 6, 7)}; '1' > '2'___ -> ___[[["'-1'", "'0'", 'X_1', (1, -1), (1, 1), [], (0, -1)], ["'0'", "'1'", 'X_0', (0, 100), (1, 1), [], (0, -1)], ["'2'", None, 'X_3', (1, -1), (1, 1), (20, 100), [1, 2, 3, 4, 5, 6, 7]], ["'1'", "'2'", 'X_4', (1, -1), (1, 1), [], (0, -1)]], [["'1'", "'2'", 'X_2', (1, -1), (0, 100), (20, 100), (0, -1)]]]___

___
___{l(100, 2000)}___ -> ___[[], [[None, None, 'X_0', (1, -1), (100, 2000), [], (0, -1)]]]___ ]