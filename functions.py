import time
from typing import Union

Number = Union[int, float]


class Functions:
    """
    Class containing methods for the test 
    """

    @staticmethod
    def functionMultiply(f0_arg0: Number, f0_arg1: Number):
        # print("Start functionMultiply")
        time.sleep(1)
        print(f"Result: {f0_arg0} * {f0_arg1} = {f0_arg0 * f0_arg1}")
        # print("End functionMultiply")
        return f0_arg0 * f0_arg1

    @staticmethod
    def function1Summ(f1_arg0: Number, f1_arg1: Number, f1_arg2: Number):
        # print("Start function1Summ")
        time.sleep(3)
        print(f"Result: {f1_arg0} + {f1_arg1} + {f1_arg2} = {f1_arg0 + f1_arg1 + f1_arg2}")
        # print("End function1Summ")
        return f1_arg0 + f1_arg1 + f1_arg2

    @staticmethod
    def functionOne(f1_arg0: Number):
        # print("Start functionOne")
        time.sleep(1)
        print(f"Result: {f1_arg0}")
        # print("End functionOne")
        return f1_arg0
