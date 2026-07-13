import pytest

from agent.router import (
    is_calculator_query,
    is_document_query,
    is_math_query,
    normalize_query,
    route_query,
)


@pytest.mark.parametrize(
    "query",
    [
        "2 + 3",
        "计算 2^10 + 24",
        "算一下 (12.5 - 2.5) / 2",
        "请帮我计算 -4 * (3 + 2)",
        "2 + 3 等于多少？",
        "10 % 3",
    ],
)
def test_recognizes_calculator_queries(query):
    assert is_calculator_query(query)


@pytest.mark.parametrize(
    "query",
    [
        "https://example.com/docs",
        "解释 client/server 架构",
        "什么是 A/B 测试",
        "state-of-the-art 是什么意思",
        "版本 2.0",
        "2026-07-13",
        "42",
        "",
    ],
)
def test_rejects_non_calculator_queries(query):
    assert not is_calculator_query(query)


def test_normalizes_query_once():
    assert normalize_query("  Generate AN OUTLINE  ") == "generate an outline"


@pytest.mark.parametrize(
    "query",
    ["求 x 的导数", "计算 x 的导数", "解释这个积分", "这个极限是多少"],
)
def test_recognizes_math_queries(query):
    assert is_math_query(query)


@pytest.mark.parametrize(
    "query",
    [
        "这个文档讲了什么",
        "总结主要内容",
        "作者的主要观点是什么",
        "本文的结论是什么",
        "这篇文章有哪些限制",
        "这份材料讲了什么",
        "第二章节讨论什么",
        "实验使用了什么数据",
    ],
)
def test_recognizes_document_queries_when_document_exists(query):
    assert is_document_query(query, has_document=True)


@pytest.mark.parametrize("query", ["作者是谁", "结论是什么", "这篇文章讲什么"])
def test_does_not_route_document_references_without_document(query):
    assert not is_document_query(query, has_document=False)


@pytest.mark.parametrize(
    ("query", "has_document", "expected"),
    [
        ("2 + 3", False, "calculator"),
        ("计算 2^10 + 24", False, "calculator"),
        ("解释 client/server 架构", False, "general_qa"),
        ("什么是 A/B 测试", False, "general_qa"),
        ("state-of-the-art 是什么意思", False, "general_qa"),
        ("计算 x 的导数", False, "math"),
        ("解释这个积分", False, "math"),
        ("generate an outline", False, "outline"),
        ("生成深度学习提纲", False, "outline"),
        ("给这份文档生成提纲", True, "document_qa"),
        ("给这份文档生成提纲", False, "outline"),
        ("作者的主要结论是什么", True, "document_qa"),
        ("作者的主要结论是什么", False, "general_qa"),
        ("这个文档讲了什么", True, "document_qa"),
        ("总结主要内容", True, "document_qa"),
        ("总结 2 + 2", True, "calculator"),
        ("What is machine learning?", False, "general_qa"),
        ("", False, "general_qa"),
    ],
)
def test_routes_queries(query, has_document, expected):
    assert route_query(query, has_document=has_document) == expected
