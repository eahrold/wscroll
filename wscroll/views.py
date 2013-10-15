from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render_to_response, get_object_or_404, redirect, render
from django.template import RequestContext, Template, Context, loader
from django.template.loader import get_template
from django.forms.models import inlineformset_factory

from plistlib import writePlistToString
from wscroll.models import *
from forms import *

@login_required(redirect_field_name='')
def index(request):
    #show list of pages and groups
    collections = Collection.objects.all()
    pages = WebPage.objects.all()
    wpform = WebPageForm(request.POST)
    colform = CollectionNameForm(request.POST)
    context = {'collections': collections,'wpform':wpform,'colform':colform,'pages' : pages}
    return render(request, 'wscroll/index.html', context)

########################################
#########  WebPage Methods ################
########################################  
@login_required(redirect_field_name='')
def page_list(request):
    pages = WebPage.objects.all()
    return render(request, 'wscroll/page_list.html', {'pages': pages})

@login_required(redirect_field_name='')
def page_add(request):
    if request.method == 'POST':
        form = WebPageForm(request.POST)
        if form.is_valid():        
            url = form.cleaned_data['url']
            if url:
                form.save()
        return redirect('wscroll.views.index')
    else:
        form = WebPageForm()
    return render_to_response('wscroll/add_page.html', {'form': form,}, context_instance=RequestContext(request))
    
   
@login_required(redirect_field_name='')
def page_delete(request,id):
    p = get_object_or_404(WebPage, pk=id)
    p.delete()
    return redirect('wscroll.views.index')

@login_required(redirect_field_name='')
def page_edit(request, page_id):
    page=get_object_or_404(WebPage, pk=page_id)
    if request.POST:
        form = WebPageForm(request.POST,instance=page)
        if form.is_valid(): 
            form.save()            
        return redirect('wscroll.views.page_details', page.id)            
    else:
        form = WebPageForm(instance=page)
        
    return render_to_response('wscroll/edit_page.html', {'form': form,'page':page}, context_instance=RequestContext(request))


    
########################################
######  WebPage List Methods    ########
########################################  
@login_required(redirect_field_name='')
def collection_add(request):
    if request.method == 'POST':
        form = CollectionForm(request.POST)
        if form.is_valid():
            collection = form.save(commit=True)
            new_url = form.cleaned_data['new_url']
            if new_url:
                collection.url.create(url=new_url)            
            collection.save()
            return redirect('wscroll.views.index')
    else:
        form = CollectionForm()
    return render_to_response('wscroll/add_collection.html', {'form': form,}, context_instance=RequestContext(request))

def collection_add_from_index(request):
    if request.method == 'POST':
        form = CollectionForm(request.POST)
        if form.is_valid():
            new_url = form.cleaned_data['new_url']
            collection = form.save(commit=True)
            if new_url:
                collection.url.create(url=new_url)            
                collection.save()
            return redirect('wscroll.views.collection_edit', collection.id)
    else:
        form = CollectionForm()
    return render_to_response('wscroll/add_collection.html', {'form': form,}, context_instance=RequestContext(request))
    
@login_required(redirect_field_name='')
def collection_details(request, id):
    collection = get_object_or_404(Collection, pk=id)
    return render(request, 'wscroll/collection_details.html', {'collection': collection})

@login_required(redirect_field_name='')
def collection_edit(request, collection_id):
    collection = Collection.objects.get(id=collection_id)  
    if request.POST:
        form = CollectionForm(request.POST,instance=collection)
        print collection.url.all()
        if form.is_valid():
            form.save()
            new_url = form.cleaned_data['new_url']
            if new_url:
                collection.url.create(url=new_url)            
                collection.save()
            return redirect('wscroll.views.index')
    else:
        form = CollectionForm(instance=collection)
    return render_to_response('wscroll/edit_collection.html', {'form': form,'collection':collection}, context_instance=RequestContext(request))
    
@login_required(redirect_field_name='')
def collection_delete(request, id):
    p = get_object_or_404(Collection, pk=id)
    p.delete()
    return redirect('wscroll.views.index')
    
    
def getlist(request, name):       
    pl = get_object_or_404(Collection, name=name)    
    wpages=pl.url.all()
    if pl.delay:
        delay=pl.delay
    else:
        delay=30
        
    plist = []
    
    for p in wpages:
        plist.append(p.url)
        
    detail=writePlistToString({'webpages':plist,'delay':delay})
    return HttpResponse(detail)