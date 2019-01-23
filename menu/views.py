from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404

from django.db.models import Q
from datetime import datetime, timedelta
from django.http import Http404, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse

from .models import *
from .forms import *


def menu_list(request):
    actual_menus = Menu.objects.prefetch_related(
        'items'
    ).filter(
        Q(expiration_date__gte=timezone.now().date()) |
        Q(expiration_date__isnull=True)
    )
    menus = sorted(actual_menus,
                   key=lambda i: i.expiration_date or datetime.date(timezone.now() + timedelta(days=3650))
                   )
    return render(request, 'menu/menu_info.html', {'menus': menus})


def menu_detail(request, pk):
    menu = Menu.objects.get(pk=pk)
    return render(request, 'menu/menu_detail.html', {'menu': menu})


def item_detail(request, pk):
    try: 
        item = Item.objects.get(pk=pk)
    except ObjectDoesNotExist:
        raise Http404
    return render(request, 'menu/detail_item.html', {'item': item})


def create_new_menu(request):
    form = MenuForm(request.POST or None)
    if form.is_valid():
        menu = form.save()
        menu.created_date = timezone.now()
        menu.save()
        return redirect('menu_detail', pk=menu.pk)
    return render(request, 'menu/menu_edit.html', {'form': form})


def edit_menu(request, pk):
    menu = get_object_or_404(Menu, pk=pk)
    form = MenuForm(instance=menu)
    if request.method == "POST":
        form = MenuForm(instance=menu, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('menu:menu_detail', pk=menu.pk)
    return render(request, 'menu/menu_edit.html', {'form': form})
