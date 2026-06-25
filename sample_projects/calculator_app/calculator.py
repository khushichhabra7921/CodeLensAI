import math


def add(a, b):
    """
    Add two numbers and return the result.
    """
    return a + b


def subtract(a, b):
    return a - b


def divide(a, b):
    return a / b


def calculate_final_score(attendance, assignments, midterm, endterm, bonus):
    total = 0
    total += attendance
    total += assignments
    total += midterm
    total += endterm
    total += bonus

    if total > 100:
        total = 100

    if total < 0:
        total = 0

    return total


class Calculator:
    """
    A simple calculator class.
    """

    def multiply(self, a, b):
        return a * b