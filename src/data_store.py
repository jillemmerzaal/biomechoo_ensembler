import numpy as np
import re

from biomechzoo.utils.engine import engine
from biomechzoo.utils.zload import zload

from src.helpers import match_condition, extract_subject_id
class DataStore:
    """
    Loads, indexes and extracts relevant data and information from the zoo files.
    """
    def __init__(self, fld, conditions, subj_list=None, str_match=None):
        self.fld = fld
        self.conditions = conditions
        self.subj_list = subj_list
        self.str_match = str_match
        self.subjects = self._resolve_subjects()

        # lazy caches — populated on first access
        self._lines: dict[tuple[str, str], list[np.ndarray]] = {}
        self._events: dict[tuple[str, str], list[float]] = {}
        self._subj_index: dict[tuple[str, str], list[str]] = {}

    def get_lines(self, channel, condition):
        key = (channel, condition)
        if key not in self._lines:
            self._extract(channel, condition)

        return self._lines.get(key, [])

    def get_events(self, channel, condition):
        key = (channel, condition)
        if key not in self._events:
            self._extract(channel, condition)

        return self._events.get(key, [])

    def get_subject_ids(self, channel, condition):
        key = (channel, condition)
        if key not in self._subj_index:
            self._extract(channel, condition)
        return self._subj_index.get(key, [])



    def _extract(self, channel, condition, ):
        """Parse all zoo files for on (channel, condition) pair."""
        key = (channel,condition)
        self._lines[key] = []
        self._events[key] = []
        self._subj_index[key] = []

        fl = engine(self.fld)
        for f in fl:
            data = zload(f)
            matched = match_condition(f, self.conditions)
            if matched != condition or channel not in data.keys():
                continue

            ch_data = data[channel]
            raw = ch_data.get("line")
            if raw is not None:
                arr = np.asarray(raw, dtype=float).squeeze()
                self._lines[key].append(arr)
                self._subj_index[key].append(extract_subject_id(f, subj_list=self.subj_list, str_pattern=self.str_match))


    def _resolve_subjects(self):
        seen, result = set(), []
        fl = engine(self.fld)
        for f in fl:
            for cond in self.conditions:
                if match_condition(f, self.conditions) == cond:
                    s =  extract_subject_id(f, subj_list=self.subj_list, str_pattern=self.str_match)
                    if s not in seen:
                        seen.add(s)
                        result.append(s)

        return result