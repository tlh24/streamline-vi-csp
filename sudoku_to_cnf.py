import sys

def var_id(r, c, v):
	"""
	Maps 0-indexed row (0-8), col (0-8), and val (0-8)
	to a 1-indexed SAT variable (1 to 729).
	"""
	return r * 81 + c * 9 + v + 1

def generate_sudoku_cnf(puzzle_string):
	if len(puzzle_string) != 81:
		raise ValueError("Puzzle string must be exactly 81 characters long.")

	clauses = []

	# 1. CELL CONSTRAINTS: Each cell must have exactly one value.
	for r in range(9):
		for c in range(9):
			# At least one value in this cell
			clauses.append([var_id(r, c, v) for v in range(9)])
			# At most one value in this cell (mutually exclusive)
			for v1 in range(9):
				for v2 in range(v1 + 1, 9):
					clauses.append([-var_id(r, c, v1), -var_id(r, c, v2)])

	# 2. ROW CONSTRAINTS: Each row must contain each value exactly once.
	for r in range(9):
		for v in range(9):
			# At least one cell in the row has the value
			clauses.append([var_id(r, c, v) for c in range(9)])
			# At most one cell in the row has the value
			for c1 in range(9):
				for c2 in range(c1 + 1, 9):
					clauses.append([-var_id(r, c1, v), -var_id(r, c2, v)])

	# 3. COLUMN CONSTRAINTS: Each column must contain each value exactly once.
	for c in range(9):
		for v in range(9):
			# At least one cell in the column has the value
			clauses.append([var_id(r, c, v) for r in range(9)])
			# At most one cell in the column has the value
			for r1 in range(9):
				for r2 in range(r1 + 1, 9):
					clauses.append([-var_id(r1, c, v), -var_id(r2, c, v)])

	# 4. BOX CONSTRAINTS: Each 3x3 box must contain each value exactly once.
	for br in range(3):
		for bc in range(3):
			for v in range(9):
				cells = [(br * 3 + i, bc * 3 + j) for i in range(3) for j in range(3)]
				# At least one cell in the box has the value
				clauses.append([var_id(r, c, v) for r, c in cells])
				# At most one cell in the box has the value
				for i in range(len(cells)):
					for j in range(i + 1, len(cells)):
						r1, c1 = cells[i]
						r2, c2 = cells[j]
						clauses.append([-var_id(r1, c1, v), -var_id(r2, c2, v)])

	# 5. CLUES: Add a unit clause (length 1) for each known clue.
	for i, char in enumerate(puzzle_string):
		if char not in ['0', '.']:
			r = i // 9
			c = i % 9
			v = int(char) - 1 # 0-indexed value
			clauses.append([var_id(r, c, v)])

	return clauses

def write_dimacs(clauses, filename="sudoku.cnf"):
	with open(filename, 'w') as f:
		# DIMACS header: p cnf <vars> <clauses>
		f.write(f"p cnf 729 {len(clauses)}\n")
		for clause in clauses:
			f.write(" ".join(map(str, clause)) + " 0\n")

if __name__ == "__main__":
	import sys
	# Arto Inkala's 2012 "World's Hardest Sudoku"
	# 0s represent blank spaces.
	default_puzzle = "800000000003600000070090200050007000000045700000100030001000068008500010090000400"
	puzzle = sys.argv[1] if len(sys.argv) > 1 else default_puzzle

	print(f"Translating puzzle: {puzzle}")
	cnf_clauses = generate_sudoku_cnf(puzzle)

	out_file = "hard_sudoku.cnf"
	write_dimacs(cnf_clauses, out_file)
	print(f"Successfully wrote {len(cnf_clauses)} clauses to {out_file}")
