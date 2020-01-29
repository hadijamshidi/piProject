from django.http import JsonResponse
import json
from calculator.solver import Solver
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def solve(request):
    try:
        if not request.method == 'POST':
            raise Exception("USE POST")
        body = request.body.decode('utf-8')
        params = json.loads(body)
        result = Solver(params=params).solver()
        return JsonResponse(result)
    except Exception as e:
        return JsonResponse({"e": str(e)}, status=400)
