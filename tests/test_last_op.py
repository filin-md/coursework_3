from utils.last_op import encode_from, encode_to, last_five, DATA


def test_encode_from():
    assert encode_from("Счет 38611439522855669794") == "Счет 3861 14** **** **** 9794"

def test_encode_to():
    assert encode_to("Visa Platinum 8990922113665229") == "Visa Platinum **5229"

def test_last_five():
    assert type(last_five(DATA)) == list
    assert len(last_five(DATA)) == 5