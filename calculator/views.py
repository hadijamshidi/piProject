from django.http import JsonResponse
import json
from calculator.solver_enums import SolverKind
from calculator.solver import Poly2, Poly1
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def solve(request):
    try:
        if not request.method == 'POST':
            raise Exception("USE POST")
        body = request.body.decode('utf-8')
        params = json.loads(body)
        kind = params.get('kind')
        if not kind:
            kind = SolverKind.polynomial2.value
        if kind == SolverKind.polynomial2.value:
            solver = Poly2
        elif kind == SolverKind.polynomial1.value:
            solver = Poly1
        else:
            raise Exception("Invalid kind")
        solutions = solver(params=params).solve()
        return JsonResponse(solutions)
    except Exception as e:
        return JsonResponse({"e": str(e)}, status=400)
