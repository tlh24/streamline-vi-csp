def decode_solution(filename):
	with open(filename, 'r') as f:
		lines = f.readlines()

	if lines[0].strip() != "SAT":
		print("The solver did not find a solution (UNSAT).")
		return

	# Read the second line, split by space, and convert to integers
	# We ignore the last '0' character
	variables = [int(x) for x in lines[1].split()[:-1]]

	# Filter out only the True (positive) assignments
	true_vars = [v for v in variables if v > 0]

	# Create an empty 9x9 grid
	grid = [[0 for _ in range(9)] for _ in range(9)]

	# Reverse the math: var_id = r * 81 + c * 9 + v + 1
	for var in true_vars:
		var -= 1           # shift back to 0-indexed
		v = var % 9        # value (0-8)
		c = (var // 9) % 9 # column (0-8)
		r = var // 81      # row (0-8)

		grid[r][c] = v + 1 # Store actual digit (1-9)

	# Print the grid nicely
	print("-" * 25)
	for r in range(9):
		row_str = "| "
		for c in range(9):
			row_str += str(grid[r][c]) + " "
			if c % 3 == 2:
				row_str += "| "
		print(row_str)
		if r % 3 == 2:
			print("-" * 25)

	# print the grid as a standard 81-string
	for r in range(9):
		for c in range(9):
			print(grid[r][c], end='')
	print("")

if __name__ == "__main__":
	decode_solution("solution.txt")
