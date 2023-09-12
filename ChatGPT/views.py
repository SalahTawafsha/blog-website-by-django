import json

from django.http import HttpResponse

from .GPT import GPT


def generate_post(request):
    # Parse the JSON string
    data = json.loads(request.body.decode('utf-8'))
    content = GPT.generate_post(data['title'])
    return HttpResponse(content, content_type="text/plain")  # Adjust content_type as needed


def summarize_post(request):
    # Parse the JSON string
    data = json.loads(request.body.decode('utf-8'))
    content = GPT.summarize_post(data['body'])
    return HttpResponse(content, content_type="text/plain")  # Adjust content_type as needed


def fix_post_grammar(request):
    # Parse the JSON string
    data = json.loads(request.body.decode('utf-8'))
    content = GPT.fix_grammar(data['body'])
    return HttpResponse(content, content_type="text/plain")  # Adjust content_type as needed
