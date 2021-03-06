from allauth.socialaccount.adapter import DefaultSocialAccountAdapter


class DiscordSocialAccountAdapter(DefaultSocialAccountAdapter):

    def save_user(self, request, sociallogin, form):
        user = super().save_user(request, sociallogin, form)
        account = user.socialaccount_set.first()
        user.username = '{username}{discriminator}'.format(**account.extra_data)
        user.save()
        return user
