import re
import numpy as np
from typing import NamedTuple
from enum import Enum
from dataclasses import dataclass
from scipy.stats import iqr

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


class ZooEvent(NamedTuple):
    x: float   # frame / time / % gait cycle
    y: float   # amplitude value


def extract_events(ch_data, event_name):
    """Extracts the named event scalers (value and frame) from a zoo file."""
    try:
        x = ch_data["event"][event_name][0]
        y = ch_data["event"][event_name][1]
        if y == 999:
            return None
        return ZooEvent(x=x, y=y)
    except (KeyError, TypeError, ValueError):
        return None

def compute_ensemble(arrays):
    """Compute time normalized mean and standard deviation for a list of arrays.

    Parameters
    ----------
    arrays : list[np.ndarray]

    Returns
    -------
    mean : array
    upper : array
        mean + std
    lower : array
        mean - std
    """

    stack = np.vstack(arrays)
    mean = np.nanmean(stack, axis=0)
    std = np.nanstd(stack, axis=0)

    return mean, mean+std, mean-std

class ConditionSource(Enum):
    """Enum defining condition sources."""
    FOLDER = "folder" # Condition encoded in folder/filepath
    CHANNEL = "channel" # Conditions encoded in channel name suffix/prefix


@dataclass
class ConditionSpec:
    """Describes how the conditions are encoded in the data"""

    source: ConditionSource
    conditions: list[str]
    channel_map: dict[str, str] | None = None

def _compute_bandwidth(values: list[float]) -> float:
    """Silverman's rule of thumb — bandwidth scaled to data spread.
    More robust than Scott's rule when outliers are present."""

    arr = np.asarray(values)
    n=len(arr)
    std = np.std(arr, ddof=1)
    spread = min(std, iqr(arr) / 1.34)
    return 0.9 * spread * n ** (-1 / 5)


def _align_by_subject(vals_a:list[float], subjects_a:list[str], vals_b:list[float], subjects_b:list[str]):
    map_b = dict(zip(subjects_b, vals_b))
    aligned_a, aligned_b, aligned_s = [], [], []

    for val_a, subj in zip(vals_a, subjects_a):
        if subj in map_b:
            aligned_a.append(val_a)
            aligned_b.append(map_b[subj])
            aligned_s.append(subj)

    return aligned_a, aligned_b, aligned_s