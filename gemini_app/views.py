from django.shortcuts import render
from django.http import JsonResponse
from google import generativeai as genai
import os

"""GEMINI API REQUEST EXAMPLE:

curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=GEMINI_API_KEY" \
-H 'Content-Type: application/json' \
-X POST \
-d '{
  "contents": [{
    "parts":[{"text": "Explain how AI works"}]
    }]
   }'
"""

def gemini_request(request):
    # Configure the API key
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    
    # For Gemini 2.0 Flash
    model = genai.GenerativeModel('gemini-2.0-flash')
    
    # Generate content
    response = model.generate_content("Write a poem about AI")
    
    # Handle the response
    if response and hasattr(response, 'text'):
        return JsonResponse({"response": response.text})
    else:
        return JsonResponse({"error": "Failed to generate response"}, status=500)

# Create your views here.
