from calculator.solver_enums import SolverKind, Steps


class Solver:
    def __init__(self, params):
        self.params = params
        kind = params.get('kind')
        if not kind:
            kind = SolverKind.polynomial2.value
        if kind == SolverKind.polynomial2.value:
            self.solver = self.polynomial2_solver
        elif kind == SolverKind.polynomial1.value:
            self.solver = self.polynomial1_solver
        else:
            raise Exception("Invalid kind")

    def polynomial1_solver(self):
        return {"s": 1}

    def polynomial2_solver(self):
        a, b, c = self.params["coeffs"]
        steps = []
        delta = b ** 2 - 4 * a * c
        steps.append({
            "pre": Steps.pre_delta.value,
            "formula": ["Delta = b^2 - 4ac"],
            "code": Steps.delta_calculation_code.value,
        })
        if delta < 0:
            steps.append({
                "post": Steps.negative_delta.value,
                "formula": ["delta = {} < 0".format(delta)]
            })
        elif delta == 0:
            steps.append({
                "post": Steps.zero_delta.value,
                "formula": ["delta = 0"],
            })
        else:
            steps.append({
                "pre": Steps.positive_delta.value,
            })
        return {"steps": steps}
