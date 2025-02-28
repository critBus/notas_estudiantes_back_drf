EXTENSION_TYPE_UNKNOWN = "DESCONOCIDO"  # "UNKNOWN"


def get_extension(file_name):
    # Split the file name into parts using the dot as a separator
    parts = file_name.split(".")

    # Check if there is at least one extension
    if len(parts) > 1:
        # Get the last part, which is considered the extension
        extension = parts[-1]

        # Check if the extension has more than 6 characters
        if len(extension) > 6:
            return EXTENSION_TYPE_UNKNOWN

        # Return the extension in uppercase
        return extension.upper()

    # If there is no extension, return "UNKNOWN"
    return EXTENSION_TYPE_UNKNOWN
