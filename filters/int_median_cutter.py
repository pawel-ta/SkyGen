

def int_median_cutter(lower_bound: int, upper_bound: int, value: int):
    """
    Simple function for cutting values to fit between bounds
    Args:
        lower_bound (int): lower cutting bound
        upper_bound (int): upper cutting bound
        value (int): value to fit between bounds
    Returns:
        value cut to fit into bounds (as integer)
    """
    return int(max(min(value, upper_bound), lower_bound))