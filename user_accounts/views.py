"""User account related views code"""
import account.views
from .forms  import SignupForm

class SignupView(account.views.SignupView):
    """Views to handle new account sign-ups"""
    form_class = SignupForm

    def after_signup(self, form):
        self.create_profile(form)
        super(SignupView, self).after_signup(form)

    def create_profile(self, form):
        profile = self.created_user.get_profile()
        profile.name = form.cleaned_data["name"]
        profile.save()

