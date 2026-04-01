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
        self._fl = engine(self.fld)
        self.subjects = self._resolve_subjects()


        # lazy caches — populated on first access
        self._extracted: set[tuple[str, str]] = set()
        self._lines: dict[tuple[str, str], list[np.ndarray]] = {}
        self._events: dict[tuple[str, str], list[float]] = {}
        self._subj_index: dict[tuple[str, str], list[str]] = {}


    def _ensure_extracted(self, channel: str, condition: str) -> None:
        key = (channel, condition)
        if key not in self._extracted:
            self._extract(channel, condition)
            self._extracted.add(key)

    def get_lines(self, channel, condition):
        self._ensure_extracted(channel, condition)
        return self._lines.get((channel, condition), [])

    def get_events(self, channel, condition):
        self._ensure_extracted(channel, condition)
        return self._events.get((channel, condition), [])

    def get_subject_ids(self, channel, condition):
        self._ensure_extracted(channel, condition)
        return self._subj_index.get((channel, condition), [])



    def _extract(self, channel, condition, ):
        """Parse all zoo files for on (channel, condition) pair."""
        key = (channel,condition)
        self._lines[key] = []
        self._events[key] = []
        self._subj_index[key] = []

        for f in self._fl:
            data = zload(f)
            matched = match_condition(f, self.conditions)

            # fall save: condition needs to be all or match the condition currently in favour
            if matched != "__all__":
                if matched != condition:
                    continue

            # fail save: key must be in data.
            if channel not in data.keys():
                continue

            ch_data = data[channel]
            raw = ch_data.get("line")
            if raw is not None:
                arr = np.asarray(raw, dtype=float).squeeze()
                self._lines[key].append(arr)
                self._subj_index[key].append(extract_subject_id(f, subj_list=self.subj_list, str_pattern=self.str_match))


    def _resolve_subjects(self):
        seen, result = set(), []
        for f in self._fl:
            matched = match_condition(f, self.conditions)
            if matched is None:
                continue

            s =  extract_subject_id(f, subj_list=self.subj_list, str_pattern=self.str_match)
            if s not in seen:
                seen.add(s)
                result.append(s)

        return result