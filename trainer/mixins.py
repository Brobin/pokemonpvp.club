from django.contrib import messages
from django.shortcuts import redirect


class LoginMixin(object):

    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            messages.warning(self.request, 'Sign in to view this page.')
            return redirect('/')
        return super().dispatch(*args, **kwargs)
