from django.shortcuts import render

def analytics_home(request):
    return render(request, "analytics/home.html")

def traffic_report(request):
    return render(request, "analytics/traffic_report.html")

def user_stats(request):
    return render(request, "analytics/user_stats.html")

def engagement_report(request):
    return render(request, "analytics/engagement_report.html")
