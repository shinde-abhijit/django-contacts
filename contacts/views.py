from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import ContactListForm
from .models import ContactList
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from accounts.views import title_tailwind_classes



@login_required
def add_contact(request):
    if request.method == "POST":
        form = ContactListForm(request.POST, request.FILES)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.user = request.user
            contact.created_by = request.user
            contact.save()
            messages.success(request, "Contact added successfully.")
            return redirect("contact_list")
    else:
        form = ContactListForm()
    context = {
        "form": form, 
        'title_tailwind_classes':title_tailwind_classes
    }
    return render(request, "contacts/add_contact.html", context)


@login_required
def contact_list(request):
    contact_qs = ContactList.objects.filter(user=request.user).order_by("-created_at")
    paginator = Paginator(contact_qs, 50)  # 50 contacts per page

    page = request.GET.get("page")
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)
    
    context = {
        'title_tailwind_classes':title_tailwind_classes,
        "contacts": contacts,
        "page_obj": contacts,
        "is_paginated": contacts.has_other_pages(),
    }

    return render(
        request,
        "contacts/contact_list.html",
        context
    )


@login_required
def contact_details(request, pk):
    contact = get_object_or_404(ContactList, pk=pk, user=request.user)
    context = {
        "contact": contact, 
        'title_tailwind_classes':title_tailwind_classes
    }
    return render(request, "contacts/contact_details.html", context)


@login_required
def contact_update(request, pk):
    contact = get_object_or_404(ContactList, pk=pk, user=request.user)
    if request.method == "POST":
        form = ContactListForm(request.POST, request.FILES, instance=contact)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.updated_by = request.user
            contact.save()
            messages.success(request, "Contact updated successfully.")
            return redirect("contact_details", pk=contact.pk)
    else:
        form = ContactListForm(instance=contact)
    context = {
        "form": form, 
        'title_tailwind_classes':title_tailwind_classes,
        "contact": contact
    }
    return render(request, "contacts/contact_update.html", context)


@login_required
def contact_delete(request, pk):
    contact = get_object_or_404(ContactList, pk=pk, user=request.user)
    if request.method == "POST":
        contact.delete()
        messages.success(request, "Contact deleted successfully.")
        return redirect("contact_list")
    context = {
        'title_tailwind_classes':title_tailwind_classes,
        "contact": contact
    }
    return render(request, "contacts/contact_delete.html", context)


@login_required
def contact_search(request):
    query = request.GET.get("q", "")
    contacts = ContactList.objects.filter(user=request.user)

    if query:
        contacts = contacts.filter(
            Q(first_name__icontains=query)
            | Q(last_name__icontains=query)
            | Q(email__icontains=query)
            | Q(contact__icontains=query)
        ).order_by("-created_at")

    paginator = Paginator(contacts, 50)
    page = request.GET.get("page")

    try:
        contacts_page = paginator.page(page)
    except PageNotAnInteger:
        contacts_page = paginator.page(1)
    except EmptyPage:
        contacts_page = paginator.page(paginator.num_pages)

    context = {
        "contacts": contacts_page,
        "query": query,
        "page_obj": contacts_page,
        "is_paginated": contacts_page.has_other_pages(),
        'title_tailwind_classes':title_tailwind_classes,
    }
    return render(
        request,
        "contacts/contact_search.html", context
    )


@login_required
def city_list(request):
    cities = (
        ContactList.objects.filter(user=request.user)
        .values_list("city", flat=True)
        .distinct()
        .order_by("city")
    )
    selected_city = request.GET.get("city")
    contacts = ContactList.objects.filter(user=request.user)
    if selected_city:
        contacts = contacts.filter(city=selected_city)

    paginator = Paginator(contacts, 50)
    page = request.GET.get("page")
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)

    context = {
        "cities": cities,
        "selected_city": selected_city,
        "contacts": contacts,
        "page_obj": contacts,
        "is_paginated": contacts.has_other_pages(),
        'title_tailwind_classes':title_tailwind_classes,
    }

    return render( request, "contacts/city_list.html", context)


@login_required
def state_list(request):
    states = (
        ContactList.objects.filter(user=request.user)
        .values_list("state", flat=True)
        .distinct()
        .order_by("state")
    )
    selected_state = request.GET.get("state")
    contacts = ContactList.objects.filter(user=request.user)
    if selected_state:
        contacts = contacts.filter(state=selected_state)

    paginator = Paginator(contacts, 50)
    page = request.GET.get("page")
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)
    
    context = {
        "states": states,
        "selected_state": selected_state,
        "contacts": contacts,
        "page_obj": contacts,
        "is_paginated": contacts.has_other_pages(),
        'title_tailwind_classes':title_tailwind_classes,
    }
    return render( request, "contacts/state_list.html", context)


@login_required
def country_list(request):
    countries = (
        ContactList.objects.filter(user=request.user)
        .values_list("country", flat=True)
        .distinct()
        .order_by("country")
    )
    selected_country = request.GET.get("country")
    contacts = ContactList.objects.filter(user=request.user)
    if selected_country:
        contacts = contacts.filter(country=selected_country)

    paginator = Paginator(contacts, 50)
    page = request.GET.get("page")
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)
    context = {
        "countries": countries,
        "selected_country": selected_country,
        "contacts": contacts,
        "page_obj": contacts,
        "is_paginated": contacts.has_other_pages(),
    }
    return render( request, "contacts/country_list.html", context)


@login_required
def contact_type_list(request):
    contact_types = (
        ContactList.objects.filter(user=request.user)
        .values_list("contact_type", flat=True)
        .distinct()
        .order_by("contact_type")
    )
    selected_type = request.GET.get("contact_type")
    contacts = ContactList.objects.filter(user=request.user)
    if selected_type:
        contacts = contacts.filter(contact_type=selected_type)

    paginator = Paginator(contacts, 50)
    page = request.GET.get("page")
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)

    context = {
        "contact_types": contact_types,
        "selected_type": selected_type,
        "contacts": contacts,
        "page_obj": contacts,
        "is_paginated": contacts.has_other_pages(),
    }

    return render( request, "contacts/contact_type_list.html", context)


@login_required
def preferred_communication_list(request):
    preferred_comms = (
        ContactList.objects.filter(user=request.user)
        .values_list("preferred_communication", flat=True)
        .distinct()
        .order_by("preferred_communication")
    )
    selected_comm = request.GET.get("preferred_communication")
    contacts = ContactList.objects.filter(user=request.user)
    if selected_comm:
        contacts = contacts.filter(preferred_communication=selected_comm)

    paginator = Paginator(contacts, 50)
    page = request.GET.get("page")
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)
    context = {
        "preferred_comms": preferred_comms,
        "selected_comm": selected_comm,
        "contacts": contacts,
        "page_obj": contacts,
        "is_paginated": contacts.has_other_pages(),
    }
    return render( request, "contacts/preferred_communication_list.html", context)
