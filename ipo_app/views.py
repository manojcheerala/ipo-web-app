from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import IPO
from .serializers import IPOSerializer

# ----------------------------
# Public Views
# ----------------------------

def home(request):
    ipos = IPO.objects.all()
    search = request.GET.get('search')
    status = request.GET.get('status')

    if search:
        ipos = ipos.filter(company_name__icontains=search)
    if status:
        ipos = ipos.filter(status=status)

    return render(request, 'home.html', {'ipos': ipos})

def ipo_detail(request, pk):
    ipo = get_object_or_404(IPO, pk=pk)
    return render(request, 'ipo_detail.html', {'ipo': ipo})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ipo_api_view(request):
    ipos = IPO.objects.all()
    serializer = IPOSerializer(ipos, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ipo_detail_api(request, pk):
    try:
        ipo = IPO.objects.get(pk=pk)
    except IPO.DoesNotExist:
        return Response({'error': 'IPO not found'}, status=404)

    serializer = IPOSerializer(ipo)
    return Response(serializer.data)

def upcoming_ipos(request):
    ipos = IPO.objects.filter(status='upcoming').order_by('open_date')
    query = request.GET.get('search')
    if query:
        ipos = ipos.filter(company_name__icontains=query)

    return render(request, 'public/upcoming_ipos.html', {'ipos': ipos, 'query': query})


# ----------------------------
# Admin Views
# ----------------------------

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    full_name = forms.CharField(label="Full Name")

    class Meta:
        model = User
        fields = ["full_name", "username", "email", "password1", "password2"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["full_name"]
        if commit:
            user.save()
        return user

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'admin/register.html', {'form': form})

@login_required(login_url='/dashboard/login/')
def admin_dashboard(request):
    total_ipos = IPO.objects.count()
    upcoming_ipos = IPO.objects.filter(status='upcoming').count()
    listed_ipos = IPO.objects.filter(status='listed').count()

    return render(request, 'admin/dashboard.html', {
        'total_ipos': total_ipos,
        'upcoming_ipos': upcoming_ipos,
        'listed_ipos': listed_ipos,
    })

class AddIPOForm(forms.ModelForm):
    class Meta:
        model = IPO
        fields = [
            'company_name', 'logo', 'price_band',
            'open_date', 'close_date', 'issue_size', 'issue_type',
            'listing_date', 'status',
            'ipo_price', 'listing_price', 'current_market_price',
            'rhp_pdf', 'drhp_pdf',
        ]
        widgets = {
            'open_date': forms.DateInput(attrs={'type': 'date'}),
            'close_date': forms.DateInput(attrs={'type': 'date'}),
            'listing_date': forms.DateInput(attrs={'type': 'date'}),
        }

@login_required(login_url='/dashboard/login/')
def add_ipo_view(request):
    form = AddIPOForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'IPO added successfully ')
        return redirect('admin-dashboard')
    return render(request, 'admin/add_ipo.html', {'form': form})


# ----------------------------
# IPO Table + Edit + Delete
# ----------------------------

@login_required(login_url='/dashboard/login/')
def ipo_table_view(request):
    ipos = IPO.objects.all().order_by('-open_date')
    return render(request, 'admin/ipo_table.html', {'ipos': ipos})

@login_required(login_url='/dashboard/login/')
def edit_ipo_view(request, pk):
    ipo = get_object_or_404(IPO, pk=pk)
    form = AddIPOForm(request.POST or None, request.FILES or None, instance=ipo)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'IPO updated successfully ')
        return redirect('ipo-table')
    return render(request, 'admin/edit_ipo.html', {'form': form, 'ipo': ipo})

@login_required(login_url='/dashboard/login/')
def delete_ipo_view(request, pk):
    ipo = get_object_or_404(IPO, pk=pk)
    if request.method == 'POST':
        ipo.delete()
        messages.warning(request, 'IPO deleted ')
        return redirect('ipo-table')
    return render(request, 'admin/delete_confirm.html', {'ipo': ipo})

