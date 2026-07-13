from agent.router import route_query


def test_routes_arithmetic_to_calculator():
    assert route_query("2 + 3") == "calculator"


def test_routes_outline_request_to_outline():
    assert route_query("generate an outline") == "outline"


def test_routes_explicit_document_question_when_document_exists():
    assert route_query("这个文档讲了什么", has_document=True) == "document_qa"


def test_routes_plain_question_to_general_qa():
    assert route_query("What is machine learning?") == "general_qa"
