SUMMARY_KEYWORDS = (
    "介绍",
    "总结",
    "概述",
    "主要内容",
    "讲什么",
    "说了什么",
    "摘要",
)


def is_summary_query(query: str) -> bool:
    normalized = query.strip().lower()
    return bool(normalized) and any(
        keyword in normalized for keyword in SUMMARY_KEYWORDS
    )


def route_query(query: str, has_document: bool = False) -> str:
    q = query.lower().strip()

    if any(word in q for word in ["计算", "+", "-", "*", "/", "^"]):
        return "calculator"

    if any(word in q for word in ["积分", "导数", "极限"]):
        return "math"

    if any(word in q for word in ["提纲", "outline"]):
        return "outline"

    if has_document and is_summary_query(q):
        return "document_qa"

    if has_document and any(word in q for word in ["pdf", "文档"]):
        return "document_qa"

    return "general_qa"
