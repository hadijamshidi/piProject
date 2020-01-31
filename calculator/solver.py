from calculator.solver_enums import Poly2Delta, Poly2Square, Poly2Decompose


class PublicMath:
    @staticmethod
    def float2int(n, f=2):
        if n == int(n):
            return int(n)
        return round(n, f)

class Poly1:
    def __init__(self, params):
        self.params = params

    def solve(self):
        a, b, c = self.params["coeffs"]
        return {"s": 1}


class Poly2:
    def __init__(self, params):
        self.a, self.b, self.c = params["coeffs"]
        self.delta = self.b ** 2 - 4 * self.a * self.c
        if self.delta > 0:
            self.rdelta = PublicMath.float2int(self.delta**.5)
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
        for method, solution in self.solutions.items():
            solution_steps = solution["solver"]()
            if solution_steps:
                solutions[method] = {
                    "name": solution["name"],
                    "steps": solution_steps
                }
        return solutions

    def delta_solver(self):
        steps = []
        steps.append({
            "pre": Poly2Delta.pre_delta.value,
            "formula": [
                "delta = b^2 - 4ac",
                "delta = ({})^2 - 4({})({})".format(self.b, self.a, self.c),
                "delta = {} ".format(self.b ** 2) + (
                    "+ " if self.a * self.c < 0 else "- " + "{}".format(4 * self.a * self.c))
            ],
            "code": Poly2Delta.delta_calculation_code.value,
        })
        if self.delta < 0:
            steps.append({
                "post": Poly2Delta.negative_delta.value,
                "formula": ["delta = {} < 0".format(self.delta)]
            })
        elif self.delta == 0:
            steps.append({
                "post": Poly2Delta.zero_delta.value,
                "formula": ["delta = 0"],
            })
            steps.append({
                "formula": [
                    "x1, x2 = (-({}) +- r^{})/2({})".format(self.b, self.delta, self.a),
                    "x1, x2 = {}/{}".format(-self.b, 2 * self.a),
                    "x1, x2 = {}".format(PublicMath.float2int(-self.b / 2 * self.a)),
                ],
            })
        else:
            steps.append({
                "post": Poly2Delta.positive_delta.value,
                "formula": ["delta = {} > 0".format(self.delta)]
            })
            steps.append({
                "formula": [
                    "x1 = (-({}) + r^{})/2({})".format(self.b, self.delta, self.a),
                    "x1 = ({} + {})/{}".format(-self.b, self.rdelta, 2 * self.a),
                    "x1 = {}/{}".format(-self.b + self.rdelta, 2 * self.a),
                    "x1 = {}".format(PublicMath.float2int((-self.b + self.rdelta) / 2 * self.a)),
                ]
            })
            steps.append({
                "formula": [
                    "x2 = (-({}) - r^{})/2({})".format(self.b, self.delta, self.a),
                    "x2 = ({} - {})/{}".format(-self.b, self.rdelta, 2 * self.a),
                    "x2 = {}/{}".format(-self.b - self.rdelta, 2 * self.a),
                    "x2 = {}".format(PublicMath.float2int((-self.b - self.rdelta) / 2 * self.a)),
                ]
            })
        return steps

    def square_solver(self):
        return [2]

    def decompose_solver(self):
        return [22]
