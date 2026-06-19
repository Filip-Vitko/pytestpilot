def sum_range(start, end):
    """Should return the sum of all integers from start to end, inclusive."""
    total = 0
    for i in range(start, end):
        total += i
    return total