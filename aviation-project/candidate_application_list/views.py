from django.shortcuts import render

# Create your views here.
def applicationList(request):
    return render(request, "candidateApplications.html")
