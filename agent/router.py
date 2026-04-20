def route_query(query: str, has_document: bool = False) -> str:
    q = query.lower().strip()

    if any(word in q for word in ["计算", "+", "-", "*", "/", "^"]):
        return "calculator"

    if any(word in q for word in ["积分", "导数", "极限"]):
        return "math"

    if any(word in q for word in ["提纲", "outline"]):
        return "outline"

    if has_document and any(word in q for word in ["pdf", "文档"]):
        return "document_qa"

    return "general_qa"