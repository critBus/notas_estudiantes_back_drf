def strNulo(ci):
    if ci is None:
        return True
    ci = str(ci)
    if len(ci) == 0:
        return True
    if ci.lower() == "null":
        return True
    if ci.lower() == "none":
        return True
    if len(ci) == 0:
        return True
