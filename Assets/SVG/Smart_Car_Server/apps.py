def Color(red, green, blue, white=0):
    """_summary_

    Args:
        red (_int_): _description_ RGB color value between 0 and 255
        green (_int_): _description_ RGB color value between 0 and 255
        blue (_int_): _description_. RGB color value between 0 and 255
        white (int, optional): _description_. Defaults to 0.

    Returns:
        _type_: _description_
    """
    return (white << 24) | (red << 16) | (green << 8) | blue

index = Color(255,255,255,10)
print(type(index))
print(index)