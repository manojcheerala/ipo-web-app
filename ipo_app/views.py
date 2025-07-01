# Create your views here.
from django.shortcuts import render, get_object_or_404
from .models import IPO

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
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import IPOSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ipo_detail_api(request, pk):
    try:
        ipo = IPO.objects.get(pk=pk)
    except IPO.DoesNotExist:
        return Response({'error': 'IPO not found'}, status=404)

    serializer = IPOSerializer(ipo)
    return Response(serializer.data)
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import IPO
from .serializers import IPOSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ipo_api_view(request):
    ipos = IPO.objects.all()
    serializer = IPOSerializer(ipos, many=True)
    return Response(serializer.data)