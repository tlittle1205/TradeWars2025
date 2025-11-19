def clearscr():
    """Clear terminal screen universally."""
    print("\033[2J\033[H", end="")
    