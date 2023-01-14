import helper


def test_host_arg_decode_1():
    assert helper.decode_host_list(["1-4"]) == ['1', '2', '3', '4']


def test_host_arg_decode_2():
    assert helper.decode_host_list(["1-4","6", "10,9"]) == ['1', '2', '3', '4', '6', '10', '9']


def test_host_arg_decode_3():
    assert helper.decode_host_list(["1-4,6,7", "9"]) == ['1', '2', '3', '4', '6', '7', '9']