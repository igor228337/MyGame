from django.shortcuts import redirect

class CheckAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == '/login/' and 'access_token' in request.COOKIES:
            return redirect('/game/')

        response = self.get_response(request)
        return response