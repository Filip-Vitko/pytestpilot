def add_item(item, items=[]):
    """Should return a new list with item appended, starting fresh each call."""
    items.append(item)  # bug: mutable default arg persists across calls
    return items

def find_max(numbers):
    """Should return the largest number in the list."""
    max_num = 0  # bug: fails if all numbers are negative
    for n in numbers:
        if n > max_num:
            max_num = n
    return max_num

def is_palindrome(s):
    """Should return True if the string reads the same forwards and backwards."""
    s = s.lower()
    return s == s[::-1] and len(s) > 0  # bug: empty string should count as palindrome

def safe_divide(a, b):
    """Should return a / b, or None if b is zero."""
    return a / b  # bug: crashes on b=0 instead of returning None

def sum_range(start, end):
    """Should return the sum of all integers from start to end, inclusive."""
    total = 0
    for i in range(start, end):  # bug: excludes 'end', should be end + 1
        total += i
    return total