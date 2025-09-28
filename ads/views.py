from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Ad
from .forms import AdForm  # We'll create this form

# ----------------------------
# List all ads
# ----------------------------
def ads_list(request):
    ads = Ad.objects.all().order_by('-created_at')
    return render(request, 'ads/ads_list.html', {'ads': ads})



def ad_detail(request, slug):
    ad = get_object_or_404(Ad, slug=slug)
    return render(request, 'ads/ads_detail.html', {'ad': ad})


# ----------------------------
# Add a new ad
# ----------------------------
def add_ad(request):
    if request.method == 'POST':
        form = AdForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ad added successfully!')
            return redirect('ads:ads_list')
    else:
        form = AdForm()
    return render(request, 'ads/ads_form.html', {'form': form})

# ----------------------------
# Edit an ad
# ----------------------------
def edit_ad(request, slug):
    ad = get_object_or_404(Ad, slug=slug)
    if request.method == 'POST':
        form = AdForm(request.POST, instance=ad)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ad updated successfully!')
            return redirect('ads:ads_detail', slug=ad.slug)
    else:
        form = AdForm(instance=ad)
    return render(request, 'ads/ads_form.html', {'form': form})

# ----------------------------
# Delete an ad
# ----------------------------
def delete_ad(request, slug):
    ad = get_object_or_404(Ad, slug=slug)
    ad.delete()
    messages.success(request, 'Ad deleted successfully!')
    return redirect('ads:ads_list')
