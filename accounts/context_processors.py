def profile_completion_notification(request):
    if request.user.is_authenticated:
        print(request.user.is_profile_incomplete())
        return {"show_profile_notification": request.user.is_profile_incomplete()}
    return {}
