def find_max(numbers):
    """Should return the largest number in the list."""
    max_num = 0
    for n in numbers:
        if n > max_num:
            max_num = n
    return max_num