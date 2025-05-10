from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from core.services.generator import generate_blog_post

class GeneratePostAPIView(APIView):
    def post(self, request):
        prompt = request.data.get("prompt")
        if not prompt:
            return Response({"error": "Prompt is required"}, status=400)

        try:
            blog = generate_blog_post(prompt)
            return Response({"post": blog})
        except Exception as e:
            return Response({"error": str(e)}, status=500)
