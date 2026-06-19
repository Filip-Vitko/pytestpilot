def is_palindrome(s):
    """Should return True if the string reads the same forwards and backwards."""
    s = s.lower()
    return s == s[::-1] and len(s) > 0