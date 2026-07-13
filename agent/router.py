import re


SUMMARY_KEYWORDS = (
    "介绍",
    "总结",
    "概述",
    "主要内容",
    "讲什么",
    "说了什么",
    "摘要",
)
MATH_KEYWORDS = ("积分", "导数", "极限")
OUTLINE_KEYWORDS = ("提纲", "outline")
DOCUMENT_EXPLICIT_TERMS = ("文档", "pdf", "文章", "材料", "论文", "文件")
DOCUMENT_REFERENCE_TERMS = (
    "作者",
    "本文",
    "这篇",
    "这份",
    "其中",
    "章节",
    "结论",
    "实验",
)

CALCULATOR_PREFIX_PATTERN = re.compile(
    r"^(?:(?:请帮我|请|帮我)\s*)?(?:计算|算一下|算一算|总结)\s*"
)
CALCULATOR_SUFFIX_PATTERN = re.compile(
    r"\s*(?:等于多少|是多少|结果是多少|结果|的结果)[？?]?$"
)
ARITHMETIC_EXPRESSION_PATTERN = re.compile(r"[0-9\s.+\-*/^%()]+")
ISO_LIKE_DATE_PATTERN = re.compile(r"\d{4}-\d{1,2}-\d{1,2}")


def normalize_query(query: str) -> str:
    return query.strip().lower()


def contains_any(query: str, terms: tuple[str, ...]) -> bool:
    return any(term in query for term in terms)


def is_summary_query(query: str) -> bool:
    normalized = normalize_query(query)
    return bool(normalized) and contains_any(normalized, SUMMARY_KEYWORDS)


def is_calculator_query(query: str) -> bool:
    candidate = CALCULATOR_PREFIX_PATTERN.sub("", normalize_query(query))
    candidate = CALCULATOR_SUFFIX_PATTERN.sub("", candidate).strip()
    if ISO_LIKE_DATE_PATTERN.fullmatch(candidate):
        return False
    return (
        bool(re.search(r"\d", candidate))
        and bool(re.search(r"[+\-*/^%]", candidate))
        and ARITHMETIC_EXPRESSION_PATTERN.fullmatch(candidate) is not None
    )


def is_math_query(query: str) -> bool:
    return contains_any(normalize_query(query), MATH_KEYWORDS)


def is_outline_query(query: str) -> bool:
    return contains_any(normalize_query(query), OUTLINE_KEYWORDS)


def is_document_query(query: str, has_document: bool) -> bool:
    if not has_document:
        return False

    normalized = normalize_query(query)
    return (
        is_summary_query(normalized)
        or contains_any(normalized, DOCUMENT_EXPLICIT_TERMS)
        or contains_any(normalized, DOCUMENT_REFERENCE_TERMS)
    )


def route_query(query: str, has_document: bool = False) -> str:
    normalized = normalize_query(query)

    if is_math_query(normalized):
        return "math"
    if is_calculator_query(normalized):
        return "calculator"
    if is_document_query(normalized, has_document):
        return "document_qa"
    if is_outline_query(normalized):
        return "outline"
    return "general_qa"
