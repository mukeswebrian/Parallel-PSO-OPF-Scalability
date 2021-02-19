from django.shortcuts import render
from . import utils
import os

# Create your views here.
def index(request):
    root = os.path.join(os.getcwd(), 'graph_viewer', 'run_results')
    context = {}

    if request.POST.get('network') is None:
        selected = 1
    else:
        selected = int(request.POST.get('network'))

    source = os.path.join(root, os.listdir(root)[selected])
    context['title'] = os.listdir(root)[selected]
    context['dot_string'] =  utils.get_dot_string(source)
    context['options'] = []
    context['selected'] = selected


    for i, f in enumerate(os.listdir(root)):
        context['options'].append( {'name': f.replace('.html',''), 'value':i} )

    return render(request, 'graph_viewer/view_network.html', context)
