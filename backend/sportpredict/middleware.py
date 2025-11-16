class DisableCSRFMiddleware(object):
    def __init__(self, get_response):
        print("DisableCSRFMiddleware INITIALIZED")
        self.get_response = get_response

    def __call__(self, request):
        print(f"DisableCSRFMiddleware called for {request.path}")
        setattr(request, '_dont_enforce_csrf_checks', True)
        response = self.get_response(request)
        return response