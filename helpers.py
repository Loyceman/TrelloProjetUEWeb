def enum_to_readable(enum_value):
    """
    Converts an enum value to a more readable format.
    Example: "PROJECT_MANAGER" -> "Project Manager"
    """
    words = enum_value.split('_')
    capitalized_words = [word.capitalize() for word in words]
    return ' '.join(capitalized_words)
