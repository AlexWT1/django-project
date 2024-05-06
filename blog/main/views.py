from django.shortcuts import render


# Create your views here.
def index(request):
    context = {
        'user': request.user,
    }
    return render(request, 'main/index.html', context)


def post_modal(request):
    return render(request, 'main/modals/postModal.html')


def post_modal_api(request):
    return render(request, 'main/modals/postModalApi.html')


def notification_modal(request):
    return render(request, 'main/modals/notificationModal.html')
