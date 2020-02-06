from django.http import JsonResponse
import json
from pi.solver_enums import PolyKind, GameLevel
from calculator.solver import Poly2, Poly1
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def generate(request):
    # try:
        if not request.method == 'POST':
            raise Exception("USE POST")
        body = request.body.decode('utf-8')
        params = json.loads(body)
        kind = params.get('kind')
        level = params.get('level')
        if not level:
            level = GameLevel.simple.value
        if not kind:
            kind = PolyKind.polynomial2.value
        if kind == PolyKind.polynomial2.value:
            solver = Poly2
        elif kind == PolyKind.polynomial1.value:
            solver = Poly1
        else:
            raise Exception("Invalid kind")
        problem = solver.generate(level=level)
        print(problem)
        return JsonResponse(problem)
    # except Exception as e:
    #     return JsonResponse({"e": str(e)}, status=400)
