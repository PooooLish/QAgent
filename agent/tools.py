from rag.retrieve import retrieve_chunks
from utils.calculator import calculator as safe_calculator
from utils.text_utils import truncate_text


SUMMARY_KEYWORDS = [
    "介绍",
    "总结",
    "概述",
    "主要内容",
    "讲什么",
    "说了什么",
    "摘要",
]


def is_summary_query(query: str) -> bool:
    query = query.strip().lower()
    if not query:
        return False

    return any(keyword in query for keyword in SUMMARY_KEYWORDS)


def calculator(expr: str) -> str:
    """
    包一层统一接口，内部调用安全计算器
    """
    return safe_calculator(expr)


def generate_outline(topic: str) -> str:
    topic = topic.strip()
    if not topic:
        topic = "未指定主题"

    return f"""以下是一个简要提纲：

1. 引言
2. 背景与问题定义
3. 核心方法
4. 实验或应用
5. 结论与未来工作

主题：{topic}
"""


def build_document_context(
    query: str,
    chunks: list[str],
    summary_top_k: int = 8,
    retrieval_top_k: int = 4,
    fallback_top_k: int = 3,
    max_context_len: int = 4000,
) -> tuple[str, str, list[str]]:
    """
    返回:
    - context: 给模型的上下文
    - retrieval_mode: 检索模式
    - retrieved_chunks: 实际取到的chunk列表
    """
    query = query.strip()

    if not chunks:
        return "", "no_document", []

    # 1. 总结类问题：优先取文档前几段
    if is_summary_query(query):
        retrieved = chunks[:summary_top_k]
        context = "\n\n".join(retrieved)
        context = truncate_text(context, max_context_len)
        return context, "document_summary", retrieved

    # 2. 正常检索
    retrieved = retrieve_chunks(query, chunks, top_k=retrieval_top_k)

    # 3. 检索失败时回退
    if not retrieved:
        retrieved = chunks[:fallback_top_k]
        context = "\n\n".join(retrieved)
        context = truncate_text(context, max_context_len)
        return context, "fallback", retrieved

    # 4. 正常返回
    context = "\n\n".join(retrieved)
    context = truncate_text(context, max_context_len)
    return context, "retrieval", retrieved