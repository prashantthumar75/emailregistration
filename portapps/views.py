from django.shortcuts import render, redirect, HttpResponse
# from django.contrib.auth import views
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from .forms import ContactForm
from .models import ContactModel

import datetime

from xlutils.copy import copy # http://pypi.python.org/pypi/xlutils
from xlrd import open_workbook # http://pypi.python.org/pypi/xlrd
from django.core.mail import SafeMIMEText, EmailMessage
from django.conf import settings
import os

# Create your views here.

def ContactView(request):
    if request.method == "POST":
        firstName = request.POST.get('first_name')
        lastName = request.POST.get('last_name')
        Email = request.POST.get('email')
        Message = request.POST.get('message')

        if firstName and lastName and Email and Message:
            ContactModel.objects.create(first_name=firstName, last_name=lastName, email=Email, message=Message)
            return redirect('/portfolio/excel')
        else:
            return redirect('/portfolio/excel')
    return render(request, 'index.html')

def excel(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'inline'; filename="users.xls"

    path = os.path.dirname(__file__)
    file = os.path.join(path, 'contact_list.xls')


    rb = open_workbook(file, formatting_info=False)
    r_sheet = rb.sheet_by_index(0)
    columns = ['date', 'First Name', 'Last Name', 'Email Address',  'Message']

    wb = copy(rb)
    ws = wb.get_sheet(0)

    row_num = 2  # index start from 0

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num])  # at 0 row 0 column


    rows = ContactModel.objects.all().values_list('first_name', 'last_name','email','message')
    date_Today = datetime.date.today()  # Returns 2018-01-15
    time_Today = datetime.datetime.now()  # Returns 2018-01-15 09:00



    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num+1, row[col_num])

    ws.write(row_num, 0, str(time_Today))

    wb.save(file + os.path.splitext(file)[-1]) # will save file where the excel file is
    wb.save(file) # will replace original file

    # wb.save(response)
    # return HttpResponse('Your information has benn sent!! \n\n Will Response Soon')
    return redirect('/portfolio/email')

def contact(request):
    rows = ContactModel.objects.last()
    name_ = rows.first_name
    email_ = rows.email
    cont = rows.last_name
    msg = rows.message

    path = os.path.dirname(__file__)
    file = os.path.join(path, 'contact_list.xls')

    mail = EmailMessage(  # subject
        "all list",
        # message
        'New Customer Raised Question Below Are Details\n\n'
        + 'you can find Sheet Attact below\n'
          'First Name:- ' + name_  + '\nLast Name:- ' + str(cont) + '\n Email:- ' + email_ + '\n Message:- ' + msg,
        #     'name',
        # from_email
        settings.EMAIL_HOST_USER,
        # recipient_list
        ['parthardeshana82@gmail.com']
        # ['pp119740@gmail.com']
    )
    mail.attach_file(file)
    mail.send()
    # return render(request, 'contactEmail.html')
    return redirect('/portfolio')