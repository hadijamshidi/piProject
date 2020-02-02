from calculator.solver_enums import *


class PublicMath:
    @staticmethod
    def float2int(n, f=2):
        if n == int(n):
            return int(n)
        return round(n, f)

    @staticmethod
    def format_formula(formula, horiz=False, then=True):
        if isinstance(formula, str):
            formula = [formula]
        then_str = MathSymbols.then.value if then else ""
        formatted_formula = [MathSymbols.start_statement.value + then_str + formula[
            0] + MathSymbols.end_statement.value]
        for step in formula[1:]:
            formatted_formula.append(
                MathSymbols.start_statement.value + MathSymbols.then.value + step + MathSymbols.end_statement.value)
        if horiz:
            return ["".join(formatted_formula)]
        return formatted_formula

    @staticmethod
    def n2str(n, a=False):
        if a:
            return "" if n == 1 else str(n)
        else:
            return "+{}".format(n) if n >= 0 else str(n)


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
                "{}x = -({}) = {}".format(self.a_str, self.b, -self.b) if not self.b == 0 else "{}x = 0".format(self.a_str),
                "x = {" + "{}{}{}".format(-self.b, MathSymbols.fraction.value, self.a) + "}",
            ])
        })
        if int(self.b / self.a) == (self.b / self.a):
            steps.append({
                "formula": PublicMath.format_formula(
                    "x = {}".format(int(-self.b/self.a)),
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
        return []

    def decompose_solver(self):
        return []
