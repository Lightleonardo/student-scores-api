subjects: dict[int, dict] = {}
assessments: dict[int, dict] = {}
scores: dict[int, dict] = {}

_next_subject_id = 1
_next_assessment_id = 1
_next_score_id = 1


def next_subject_id() -> int:
    global _next_subject_id
    value = _next_subject_id
    _next_subject_id += 1
    return value


def next_assessment_id() -> int:
    global _next_assessment_id
    value = _next_assessment_id
    _next_assessment_id += 1
    return value


def next_score_id() -> int:
    global _next_score_id
    value = _next_score_id
    _next_score_id += 1
    return value