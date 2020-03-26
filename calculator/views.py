from django.http import JsonResponse
from pi.solver_enums import PolyKind
from calculator.solver import Poly2, Poly1


def solve(request):
    try:
        a = int(request.GET.get('a', 0))
        b = int(request.GET.get('b', 0))
        c = int(request.GET.get('c', 0))
        kind = request.GET.get('kind', None)
        params = {"coeffs": [a, b, c]}
        if not kind:
            kind = PolyKind.polynomial2.value
        if kind == PolyKind.polynomial2.value:
            solver = Poly2
        elif kind == PolyKind.polynomial1.value:
            solver = Poly1
        else:
            raise Exception("Invalid kind")
        solutions = solver(params=params).solve()
        return JsonResponse(solutions)
    except Exception as e:
        return JsonResponse({"e": str(e)}, status=400)
