import json
from json import JSONDecodeError

from django.http import JsonResponse

from .GPT import GPT


def generate_post(request):
    try:
        # Parse the JSON string
        data = json.loads(request.body.decode('utf-8'))
        content = GPT.generate_post(data['title'])
        return JsonResponse({"response": content}, content_type="text/plain")  # Adjust content_type as needed
    except JSONDecodeError:
        return JsonResponse({"response": "You have Error in JSON format"})
    except KeyError:
        return JsonResponse({"response": "You must send title in JSON data"})


def summarize_post(request):
    try:
        # Parse the JSON string
        data = json.loads(request.body.decode('utf-8'))
        content = GPT.summarize_post(data['body'])
        return JsonResponse({"response": content}, content_type="text/plain")  # Adjust content_type as needed
    except JSONDecodeError:
        return JsonResponse({"response": "You have Error in JSON format"})
    except KeyError:
        return JsonResponse({"response": "You must send body in JSON data"})


def fix_post_grammar(request):
    try:
        # Parse the JSON string
        data = json.loads(request.body.decode('utf-8'))
        content = GPT.fix_grammar(data['body'])
        return JsonResponse({"response": content}, content_type="text/plain")  # Adjust content_type as needed
    except JSONDecodeError:
        return JsonResponse({"response": "You have Error in JSON format"})
    except KeyError:
        return JsonResponse({"response": "You must send body in JSON data"})
