from pi.solver_enums import *
import numpy as np
import json


class PublicMath:
    @staticmethod
    def float2int(n, f=2):
        if n == int(n):
            return int(n)
        return round(n, f)

    @staticmethod
    def make_persian(data_str, active=False):
        if not active:
            return data_str
        eng2per = {
            '0': '۰',
            '1': '۱',
            '2': '۲',
            '3': '۳',
            '4': '۴',
            '5': '۵',
            '6': '۶',
            '7': '۷',
            '8': '۸',
            '9': '۹',
        }
        for eng_num, per_num in eng2per.items():
            data_str = data_str.replace(eng_num, per_num)
        return data_str

    @staticmethod
    def format_formula(formula, horiz=False, then=True):
        if isinstance(formula, str):
            formula = [PublicMath.make_persian(formula)]
        then_str = MathSymbols.then.value if then else ""
        formatted_formula = [MathSymbols.start_statement.value + then_str + PublicMath.make_persian(formula[
            0]) + MathSymbols.end_statement.value]
        for step in formula[1:]:
            formatted_formula.append(
                MathSymbols.start_statement.value + MathSymbols.then.value + PublicMath.make_persian(step) + MathSymbols.end_statement.value)
        if horiz:
            return ["".join(formatted_formula)]
        return formatted_formula

    @staticmethod
    def n2str(n, a=False):
        if a:
            return "" if n == 1 else str(n)
        else:
            return "+{}".format(n) if n >= 0 else str(n)

    @staticmethod
    def is_int(n):
        return n == int(n)


class Poly1:
    def __init__(self, params):
        self.params = params
        self.a, self.b = self.params["coeffs"]
        self.a_str = PublicMath.n2str(self.a, a=True)
        self.b_str = PublicMath.n2str(self.b)

    def solve(self):
        steps = [{
            "formula": PublicMath.format_formula([
                "{}x {} = 0".format(self.a_str, self.b_str),
            ])
        }]
        if self.a == 0:
            steps.append({
                "formula": PublicMath.format_formula([
                    "{} = 0".format(self.b),
                ])
            })
            if not self.b == 0:
                steps.append({
                    "post": EquationStates.impossible.value
                })
            else:
                steps.append({
                    "post": EquationStates.trivial.value
                })

            return steps
        steps.append({
            "formula": PublicMath.format_formula([
                "{}x = -({}) = {}".format(self.a_str, self.b, -self.b) if not self.b == 0 else "{}x = 0".format(
                    self.a_str),
                "x = {" + "{}{}{}".format(-self.b, MathSymbols.fraction.value, self.a) + "}",
            ])
        })
        if int(self.b / self.a) == (self.b / self.a):
            steps.append({
                "formula": PublicMath.format_formula(
                    "x = {}".format(int(-self.b / self.a)),
                )
            })
        return steps


class Poly2:
    def __init__(self, params):
        self.a, self.b, self.c = params["coeffs"]
        self.a_str = PublicMath.n2str(self.a, a=True)
        self.b_str = PublicMath.n2str(self.b)
        self.c_str = PublicMath.n2str(self.c)
        self.delta_symbol = MathSymbols.delta.value
        self.delta = self.b ** 2 - 4 * self.a * self.c
        if self.delta > 0:
            self.rdelta = PublicMath.float2int(self.delta ** .5)
        else:
            self.rdelta = 0
        self.solutions = {
            "delta": {
                "name": Poly2Delta.name.value,
                "solver": self.delta_solver,
            },
            "square": {
                "name": Poly2Square.name.value,
                "solver": self.square_solver,
            },
            "decompose": {
                "name": Poly2Decompose.name.value,
                "solver": self.decompose_solver,
            }
        }

    def analyze(self):
        delta = -1
        x1, x2 = 0, 0
        if self.delta == 0:
            delta = 0
            x1 = (-self.b + self.rdelta) / (2 * self.a)
            x2 = x1
        if self.delta > 0:
            x1 = (-self.b + self.rdelta) / (2 * self.a)
            x2 = (-self.b - self.rdelta) / (2 * self.a)
            if PublicMath.is_int(x1) and PublicMath.is_int(x2):
                x1 = int(x1)
                x2 = int(x2)
                delta = 2
            else:
                delta = 1
        return {"delta": delta, "x1": x1, "x2": x2}

    def solve(self):
        solutions = {}
        if self.a == 0:
            solutions["poly1"] = {
                "name": Poly2States.poly1.value,
                "steps": self.poly1()
            }
            return solutions
        for method, solution in self.solutions.items():
            solution_steps = solution["solver"]()
            if solution_steps:
                solutions[method] = {
                    "name": solution["name"],
                    "steps": solution_steps
                }

        return solutions

    def poly1(self):
        steps = [
            {
                "formula": PublicMath.format_formula([
                    "{}x^2 {}x {} = 0".format(self.a_str, self.b_str, self.c_str),
                ])
            },
        ]
        for step in Poly1(params={"coeffs": [self.b, self.c]}).solve():
            steps.append(step)
        return steps

    def delta_solver(self):
        steps = [
            {
                "formula": PublicMath.format_formula([
                    "{}x^2 {}x {} = 0".format(self.a_str, self.b_str, self.c_str),
                    "({})x^2 +({})x +({}) = 0".format(self.a, self.b, self.c),
                    "ax^2 +bx +c = 0",
                    "a={}, b={}, c={}".format(self.a, self.b, self.c)
                ])
            },
        ]
        formula = [
            "{} = b^2-4ac".format(self.delta_symbol),
            "{} = ({})^2 - 4({})({})".format(self.delta_symbol, self.b, self.a, self.c),
            "{} = {} ".format(self.delta_symbol, self.b ** 2) + (
                "+ " if self.a * self.c < 0 else "- ") + "{}".format(abs(4 * self.a * self.c))
        ]
        steps.append({
            "pre": Poly2Delta.pre_delta.value,
            "formula": PublicMath.format_formula(formula),
            "code": Poly2Delta.delta_calculation_code.value,
        })
        if self.delta < 0:
            steps.append({
                "post": Poly2Delta.negative_delta.value,
                "formula": PublicMath.format_formula("{} = {} < 0".format(self.delta_symbol, self.delta), then=True)
            })
        elif self.delta == 0:
            steps.append({
                "post": Poly2Delta.zero_delta.value,
                "formula": PublicMath.format_formula("{} = 0".format(self.delta_symbol), then=True),
            })
            steps.append({
                "formula": PublicMath.format_formula([
                    "x_1, x_2 = " + "{" + "-({}) \pm {}".format(self.b, MathSymbols.radical.value) + "{" + str(
                        self.delta) + "}" + "{}2({})".format(MathSymbols.fraction.value, self.a) + "}",
                    "x_1, x_2 = {" + "{}{}{}".format(-self.b, MathSymbols.fraction.value, 2 * self.a) + "}",
                    "x_1, x_2 = {}".format(PublicMath.float2int(-self.b / 2 * self.a)),
                ]),
            })
        else:
            steps.append({
                "post": Poly2Delta.positive_delta.value,
                "formula": PublicMath.format_formula("{} = {} > 0".format(self.delta_symbol, self.delta))
            })
            steps.append({
                "formula": PublicMath.format_formula([
                    "x_1, x_2 = {" + "-b {} {}".format(MathSymbols.plum_minus.value,
                                                       MathSymbols.radical.value) + "{" + MathSymbols.delta.value + "}" + "{} 2a".format(
                        MathSymbols.fraction.value) + "}",
                    "x_1, x_2 = {" + "-({}) {} {}".format(self.b, MathSymbols.plum_minus.value,
                                                          MathSymbols.radical.value) + "{" + str(
                        self.delta) + "}" + "{} 2({})".format(
                        MathSymbols.fraction.value, self.a) + "}",
                    "x_1, x_2 = {" + "{} {} {}".format(-self.b, MathSymbols.plum_minus.value,
                                                       MathSymbols.radical.value) + "{" + str(
                        self.delta) + "}" + "{} {}".format(
                        MathSymbols.fraction.value, 2 * self.a) + "}"

                ])
            })
            if not self.rdelta == int(self.rdelta):
                steps.append({
                    "parr": [
                        PublicMath.format_formula([
                            "x_1 = {" + "{} + {}".format(-self.b, MathSymbols.radical.value) + "{" + str(
                                self.delta) + "}" + "{} {}".format(
                                MathSymbols.fraction.value, 2 * self.a) + "}",
                            "x_2 = {" + "{} - {}".format(-self.b, MathSymbols.radical.value) + "{" + str(
                                self.delta) + "}" + "{} {}".format(
                                MathSymbols.fraction.value, 2 * self.a) + "}"
                        ])
                    ]
                })
                return steps
            steps.append({
                "formula": PublicMath.format_formula([
                    "x_1, x_2 = {" + "{} {} {}".format(-self.b, MathSymbols.plum_minus.value,
                                                       self.rdelta) + "{} {}".format(
                        MathSymbols.fraction.value, 2 * self.a) + "}"
                ])
            })
            steps.append({
                "parr": [
                    PublicMath.format_formula([
                        "x_1 = " + "{" + "{} + {}".format(-self.b, self.rdelta) + "{}{}".format(
                            MathSymbols.fraction.value, 2 * self.a) + "}",
                        "x_2 = " + "{" + "{} - {}".format(-self.b, self.rdelta) + "{}{}".format(
                            MathSymbols.fraction.value, 2 * self.a) + "}"
                    ]),
                    PublicMath.format_formula([
                        "x_1 = " + "{" + "{}{}{}".format(-self.b + self.rdelta, MathSymbols.fraction.value,
                                                         2 * self.a) + "}",
                        "x_2 = " + "{" + "{}{}{}".format(-self.b - self.rdelta, MathSymbols.fraction.value,
                                                         2 * self.a) + "}",
                    ]),
                    PublicMath.format_formula([
                        "x_1 = {}".format(PublicMath.float2int((-self.b + self.rdelta) / 2 * self.a)),
                        "x_2 = {}".format(PublicMath.float2int((-self.b - self.rdelta) / 2 * self.a)),
                    ]),
                ]
            })
        return steps

    def square_solver(self):
        steps = []
        if self.a < 0:
            steps.append({
                "pre": Poly2Square.negative_a.value,
                "formula": PublicMath.format_formula([
                    "-({}x^2 {}x {}) = -(0)".format(self.a_str, self.b_str, self.c_str),
                ])
            })
            steps += Poly2(params={"coeffs": [-self.a, -self.b, -self.c]}).square_solver()
            return steps
        if not self.a ** .5 == int(self.a ** .5):
            steps.append({
                "pre": Poly2Square.multiple_a.value,
                "formula": "{}({}x^2 {}x {}) = {}(0)".format(self.a, self.a_str, self.b_str, self.c_str, self.a),
            })
            steps += Poly2(params={"coeffs": [self.a ** 2, self.a * self.b, self.a * self.c]}).square_solver()
            return steps
        ra = int(self.a ** .5)
        c_b2 = -int(4 * self.c - self.b ** 2)
        steps.append({
            "pre": Poly2Square.multiple4.value,
            "formula": PublicMath.format_formula([
                "4({}x^2 {}x {}) = 4(0)".format(self.a_str, self.b_str, self.c_str),
                "({}x)^2 + 2 ({}x)({}) {} = 0".format(2 * ra, 2 * ra, self.b, self.c_str),
                "({}x)^2 + 2 ({}x)({}) + ({})^2 - ({})^2 {} = 0".format(2 * ra, 2 * ra, self.b, self.b, self.b,
                                                                        self.c_str),
                "({}x + {})^2 {} = 0".format(2 * ra, self.b, PublicMath.n2str(-c_b2)),
                "({}x {})^2 = ".format(2 * ra, self.b_str) + ("0" if c_b2 == 0 else str(c_b2)),
            ])
        })
        if c_b2 < 0:
            steps.append({
                "post": EquationStates.impossible.value
            })
            return steps
        if c_b2 == 0:
            steps.append({
                "formula": PublicMath.format_formula([
                    "{}x {} = {}0".format(2 * ra, self.b_str, MathSymbols.plum_minus.value),
                    "{}x = {}".format(2 * ra, PublicMath.n2str(-self.b)),
                    "x_1, x_2 = {" + "{}{}{}".format(-self.b, MathSymbols.fraction.value, 2 * ra) + "}",
                ])
            })
            if int(self.b / (2 * self.a)) == self.b / (2 * self.a):
                steps.append({
                    "formula": PublicMath.format_formula([
                        "x_1, x_2 = {}".format(int(-self.b / (2 * ra))),
                    ])
                })
            return steps
        steps.append({
            "formula": PublicMath.format_formula([
                "{}x {} = {}{}".format(2 * ra, self.b_str, MathSymbols.plum_minus.value,
                                       MathSymbols.radical.value) + "{" + str(c_b2) + "}",
            ])
        })
        if PublicMath.is_int(c_b2 ** .5):
            rc_b2 = int(c_b2 ** .5)
            steps.append({
                "formula": PublicMath.format_formula([
                    "{}x {} = {}{}".format(2 * ra, self.b_str, MathSymbols.plum_minus.value, rc_b2),
                ]),
                "parr": [
                    PublicMath.format_formula([
                        "{}x_1 = {} - ({})".format(2 * ra, rc_b2, self.b),
                        "{}x_2 = -{} - ({})".format(2 * ra, rc_b2, self.b),
                    ]),
                    PublicMath.format_formula([
                        "{}x_1 = {}".format(2 * ra, rc_b2 - self.b),
                        "{}x_2 = {}".format(2 * ra, -rc_b2 - self.b),
                    ]),
                    PublicMath.format_formula([
                        "x_1 = {" + "{}{}{}".format(rc_b2 - self.b, MathSymbols.fraction.value, 2 * ra) + "}",
                        "x_2 = {" + "{}{}{}".format(-rc_b2 - self.b, MathSymbols.fraction.value, 2 * ra) + "}",
                    ]),
                ]
            })
            # TODO: simplify last ...
            return steps
        else:
            # TODO: complete for ...
            pass
        return steps

    def decompose_solver(self):
        analysis = self.analyze()
        steps = []
        if not analysis["delta"] == 2:
            return steps
        if not self.a == 1:
            steps.append({
                "pre": Poly2Decompose.devide_a.value,
                "formula": PublicMath.format_formula(
                    "{" + "{}x^2 {}x {} = 0 {} {}".format(self.a_str, self.b_str, self.c_str,
                                                          MathSymbols.fraction.value, self.a) + "}",
                )
            })
            steps += Poly2(params={"coeffs": [1, int(self.b / self.a), int(self.c / self.a)]}).decompose_solver()
            return steps
        steps.append({
            "pre": Poly2Decompose.looking.value.format(self.b, self.c)
        })
        x1, x2 = analysis["x1"], analysis["x2"]
        steps.append({
            "pre": Poly2Decompose.finding.value.format(-x1, -x2)
        })
        steps.append({
            "formula": PublicMath.format_formula([
                "{}x^2 {}x {} = 0".format(self.a_str, self.b_str, self.c_str),
                "(x {})(x {}) = 0".format(PublicMath.n2str(-x1), PublicMath.n2str(-x2))
            ]),
            "post": Poly2Decompose.zero_equal.value
        })
        steps.append({
            "parr": [
                PublicMath.format_formula([
                    "x {}= 0".format(PublicMath.n2str(-x1)),
                    "x {}= 0".format(PublicMath.n2str(-x2)),
                ]),
                PublicMath.format_formula([
                    "x_1 = {}".format(PublicMath.n2str(x1)),
                    "x_2 = {}".format(PublicMath.n2str(x2)),
                ]),
            ]
        })
        return steps

    @staticmethod
    def generate(level=GameLevel.simple.value):
        choice_list = [_ for _ in range(-9, 10, 1)]
        a_list = [_ for _ in range(1, 6)] + [-_ for _ in range(1, 6)]
        x1, x2 = np.random.choice(choice_list, 2)
        x1, x2 = int(x1), int(x2)
        a, b, c = 1, x1 + x2, x1 * x2
        if not level == GameLevel.simple.value:
            a = int(np.random.choice(a_list))
            b *= a
            c *= a
        return {"coeffs": [a, b, c], "solution": [-x1, -x2]}
