def is_linearly_independent(vectors):
    num_vectors = len(vectors)
    dimension = len(vectors[0])
    matrix = [row[:] for row in vectors]  

    # Gaussian elimination
    for i in range(min(num_vectors, dimension)):
        pivot = None
        for row in range(i, num_vectors):
            if matrix[row][i] != 0:
                pivot = row
                break

        if pivot is None:
            continue        
        if pivot != i:
            matrix[i], matrix[pivot] = matrix[pivot], matrix[i]
        
        pivot_value = matrix[i][i]
        matrix[i] = [value / pivot_value for value in matrix[i]]
        
        for row in range(i + 1, num_vectors):
            factor = matrix[row][i]
            matrix[row] = [matrix[row][col] - factor * matrix[i][col] for col in range(dimension)]
    
    rank = 0
    for row in matrix:
        if any(val != 0 for val in row):
            rank += 1
    
    return rank == num_vectors


vectors = [[1, 0, 1, 0, 1, 0, 1, 1, 0, 0], [0, 1, 0, 0, 0, 1, 0, 0, 0, 1], [0, 0, 1, 1, 1, 1, 1, 0, 0, 0], [0, 0, 0, 1, 1, 1, 1, 1, 1, 1], [0, 0, 0, 0, 1, 0, 0, 0, 1, 0], [0, 0, 0, 0, 0, 1, 1, 1, 0, 0], [0, 0, 0, 0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 1]]

result = is_linearly_independent(vectors)
print(result)
