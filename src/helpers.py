import re

_NO_CONDITIONS = "__all__"

def match_condition(path, conditions):
    if not conditions:
        return _NO_CONDITIONS

    for cond in conditions:
        if cond.lower() in path.lower():
            return cond
    return None


def extract_subject_id(f, subj_list, str_pattern):
    """
    Extracts the subject ID from the zoo file path and a string match using a regular expression of a known list of subject IDs.
    Parameters
    ----------
    f : str
        File path to the zoo file.
    subj_list : list[str]
        List of subject IDs.
    str_pattern : list[reg]
        String pattern to match the subject IDs.

    Returns
    -------
    s : str
        Subject ID.
    """
    if str_pattern:
        for pattern in str_pattern:
            match = re.search(pattern, f)
            if match:
                return match.group(0)
    if subj_list:
        matched = [subj for subj in subj_list if subj in f]
        return matched[0] if matched else "Unknown"

    return "unknown"
