import re

def match_condition(path, conditions):
    for cond in conditions:
        if cond.lower() in path.lower():
            return cond
    return "Unknown"


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
                s = match.group(0)
    elif subj_list:
        for subj in subj_list:
           s = [subj for subj in subj_list if subj in f]
    else:
        s = "Unknown"

    return s
