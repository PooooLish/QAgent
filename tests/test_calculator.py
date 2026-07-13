from utils.calculator import calculator


def test_calculates_documented_exponent_syntax():
    assert calculator("计算 2^10 + 24") == "1048"


def test_rejects_function_calls():
    assert calculator("计算 __import__('os').getcwd()") == "计算失败，请检查表达式"
