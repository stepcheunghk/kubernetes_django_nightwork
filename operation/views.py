from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, UpdateView
from django.db.models import Count
from .models import Operation, SpecialDate
from django.http import HttpResponse
from .forms import OperationForm, RawOperationForm, SpecialDateForm
from django.contrib import messages
import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import JsonResponse
from django.db.models.functions import ExtractMonth, ExtractYear
from django.shortcuts import render
from django.template.loader import render_to_string
from django.template import Context
from django.core.mail import send_mail, EmailMultiAlternatives
import json
import calendar
import csv
import os
from datetime import date

class AdminStaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

# Create your views here.
@login_required(login_url="/login/")
def plannedmain(request, id=None):
    if request.user.is_authenticated:
        username = request.user.get_username()
    form = Operation.objects.get(id=id)
    subject = "[Planned Maintenance]" + form.subject + " on " + str(form.startdate)
    context = {
        'form': form
    }
    msg_html = render_to_string('plannedmain.html', context)
    subject, from_email, to = subject, 'stephencheung@hk.chinamobile.com', 'stephencheung@hk.chinamobile.com'
    html_content = msg_html
    msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    # msg.send()
    return render(request, 'plannedmain.html', context)

@login_required(login_url="/login/")
def application(request, id=None):
    form = Operation.objects.get(id=id)
    subject = "Application for " + form.subject + " on " + str(form.startdate)
    mop = form.mop
    context = {
        'form': form
    }
    msg_html = render_to_string('application.html', context)
    subject, from_email, to = subject, 'stephencheung@hk.chinamobile.com', 'stephencheung@hk.chinamobile.com'
    html_content = msg_html
    filename = "/var/mycode/nightwork/file/" + str(form.mop)
    # msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.attach_file(filename)
    # msg.send()
    return render(request, 'application.html', context)    

@login_required(login_url="/login/")
def operation(request):
    initial_data = {
        'remarks' : "N/A",
        'impact': "No Service Impact"
    }
    form = RawOperationForm(request.POST or None, request.FILES or None, initial=initial_data)
    if form.is_valid():
        new = Operation.objects.create(**form.cleaned_data)
        id = new.id
        messages.success(request, "Operation Created")
        return redirect('result', pk=id)
    else:
        print(form.errors)
    context = {
        "form": form
    }
    return render(request, "operation.html", context)

@login_required(login_url="/login/")
def update(request, id=None):
    instance = get_object_or_404(Operation, pk=id)
    form = OperationForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "Operation Saved")
        return redirect('result', pk=id)
    context  = {
        "form": form,
    } 
    return render(request, "update.html", context)

def api(request):
    if  request.method == 'DELETE':
        data = json.loads(request.body.decode('utf-8'))
        id = data['id']
        Operation.objects.filter(id=id).delete()
        return JsonResponse({'msg':'true'})
    else:
        return JsonResponse({'msg':'fail'})        

@login_required(login_url="/login/")
def dateInput(request):
    if  request.method == 'POST':
        form = SpecialDateForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            new = SpecialDate.objects.create(**form.cleaned_data)
            id = new.id
            form = SpecialDate.objects.get(id=id)
            return redirect('result', pk=id)
        else:
            print(form.errors)
    return render(request, "date_input.html",{
        'form'       : SpecialDateForm(request.POST or None)
    })


def chart(request):
    if  request.method == 'POST':
        form = RawOperationForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            new = Operation.objects.create(**form.cleaned_data)
            id = new.id
            form = Operation.objects.get(id=id)
            subject = "A new operation has just been created by " + form.name
            context = {
                'form': form
            }
            msg_html = render_to_string('notice.html', context)
            subject, from_email, to = subject, 'stephencheung@hk.chinamobile.com', 'stephencheung@hk.chinamobile.com'
            html_content = msg_html
            msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            # msg.send()
            messages.success(request, "Operation Created")
            return redirect('result', pk=id)
        else:
            print(form.errors)
    domains     = [] #/ operations by domain
    reasontypes = [] #/ operations by reasontype
    years       = []
    months      = []
    counts      = []
    data        = [] #/ sorted by domain
    data2       = [] #/ sorted by reasontype
    today       = date.today()
    last        = today.replace(year=today.year-1)
    startrange  = calendar.monthrange(today.year,today.month)[1]
    thisyear    = today.replace(day=startrange)
    lastyear    = last.replace(day=1)
    #startrange = find the last day of the month
    #thisyear   = replace "the day of today" with "the last day of the month"
    #lastyear   = replace the day with 1st day of the month
    #queryset: operation, 2020 by domain
    #queryset2: operation, 2020 by reasontype
    #queryset3: operation, sorted by year-month 
    queryset  = Operation.objects.all().values('domain').filter(startdate__year=today.year).annotate(total=Count('domain')).order_by('domain')
    queryset2 = Operation.objects.all().values('reason_type').filter(startdate__year=today.year).annotate(total=Count('reason_type')).order_by('reason_type')
    queryset3 = Operation.objects.all().values('startdate').filter(startdate__range=[lastyear,thisyear]).annotate(month=ExtractMonth('startdate'), year=ExtractYear('startdate')).values('month', 'year').annotate(count=Count('id')).values('month', 'year', 'count').order_by('year','month')
    op_count  = Operation.objects.all().filter(startdate__year=today.year).count()
    for domain in queryset.values_list('domain', flat=True):
        domains.append(domain)
    for total in queryset.values_list('total', flat=True):
        data.append(total)
    for month in queryset3.values_list('month', flat=True):
        months.append(str(calendar.month_abbr[month]))
    for year in queryset3.values_list('year', flat=True):
        years.append(str(year))
    for count in queryset3.values_list('count', flat=True):
        counts.append(count)
    for reason_type in queryset2.values_list('reason_type', flat=True):
        reasontypes.append(reason_type)
    for total in queryset2.values_list('total', flat=True):
        data2.append(total)
    period = [i + " " + j for i, j in zip(months, years)] 
    return render(request, "chart.html",{
        'count'      : op_count,
        'domain'     : domains,
        'data'       : data,
        'reason_type': reasontypes,
        'data2'      : data2,
        'period'     : period,
        'ym_count'   : counts,
        'form'       : RawOperationForm(request.POST or None)
    })


@login_required(login_url="/login/")
def export(request):
    response = HttpResponse(content_type='text/csv')
    now = datetime.datetime.now().strftime("%Y-%m-%d")
    response['Content-Disposition'] = 'attachment; filename="OperationSummary ({}).csv"'.format(str(now))
    writer   = csv.writer(response)
    writer.writerow([
        'name',
        'phone',
        'domain',
        'category',
        'startdate',
        'starttime',
        'enddate',
        'endtime',
        'location',
        'subject',
        'reason_type',
        'reason',
        'impact',
        'remarks',
        'vendor',
        'vendor_phone',
        'mop',])
    
    for operation in Operation.objects.all().values_list(
        'name',
        'phone',
        'domain',
        'category',
        'startdate',
        'starttime',
        'enddate',
        'endtime',
        'location',
        'subject',
        'reason_type',
        'reason',
        'impact',
        'remarks',
        'vendor',
        'vendor_phone',
        'mop',
    ):
        writer.writerow(operation)

    return response

class HistoryListView(AdminStaffRequiredMixin, ListView):
    login_url = '/login/'
    model = Operation
    template_name = 'history.html'
    context_object_name = 'operations'
    ordering = ['-startdate']

    def get_context_data(self, **kwargs):
        initial_data = {
            'remarks' : "N/A",
            'impact': "No Service Impact"
        }
        if self.request.method == 'GET':
            context = super(HistoryListView, self).get_context_data(**kwargs)
            context['form'] = RawOperationForm(initial=initial_data)
            return context
    
    def post(self, request):
        form = RawOperationForm(self.request.POST or None, self.request.FILES or None)
        if form.is_valid():
            new = Operation.objects.create(**form.cleaned_data)
            id = new.id
            form = Operation.objects.get(id=id)
            subject = "A new operation has just been created by " + form.name
            context = {
                'form': form
            }
            msg_html = render_to_string('notice.html', context)
            subject, from_email, to = subject, 'stephencheung@hk.chinamobile.com', 'stephencheung@hk.chinamobile.com'
            html_content = msg_html
            msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            messages.success(self.request, "Operation Created")
            return redirect('result', pk=id)
        else:
            print(form.errors)
        context = {
            "form": form
        }
        return context

class HomeTestListView(ListView):
    template_name = 'homeTest.html'
    context_object_name = 'operations'
    queryset = Operation.objects.all()

    def get_context_data(self, **kwargs):
        initial_data = {
            'remarks' : "N/A",
            'impact': "No Service Impact"
        }
        context = super(HomeTestListView, self).get_context_data(**kwargs)
        context['ops'] = Operation.objects.all()
        context['dates'] = SpecialDate.objects.all()
        return context  

class HomeListView(ListView):
    model = Operation
    template_name = 'home.html'
    context_object_name = 'operations'
    ordering = ['-startdate']

    def get_context_data(self, **kwargs):
        initial_data = {
            'remarks' : "N/A",
            'impact': "No Service Impact"
        }
        context = super(HomeListView, self).get_context_data(**kwargs)
        context['form'] = RawOperationForm(self.request.POST or None, initial=initial_data)
        return context
    
    def post(self, request):
        if request.method == 'POST':
            print(request.POST)
            if request.POST.get('form-id'):
                op = Operation.objects.get(id=request.POST.get('form-id'))
                op.name= request.POST.get('form-name')
                op.phone= request.POST.get('form-phone')
                op.domain= request.POST.get('form-domain')
                op.category= request.POST.get('form-category')
                startdatetime = str(request.POST.get('form-startdate')) +  ' ' + str(request.POST.get('form-starttime'))
                if len(str(request.POST.get('form-starttime')).split(":")) == 2:
                    startdatetime = datetime.datetime.strptime(startdatetime, '%Y-%m-%d %H:%M')
                else:
                    startdatetime = datetime.datetime.strptime(startdatetime, '%Y-%m-%d %H:%M:%S')
                op.startdate= startdatetime
                op.starttime= startdatetime
                enddatetime = str(request.POST.get('form-enddate')) +  ' ' + str(request.POST.get('form-endtime'))
                if len(str(request.POST.get('form-endtime')).split(":")) == 2:
                    enddatetime = datetime.datetime.strptime(enddatetime, '%Y-%m-%d %H:%M')
                else:
                    enddatetime = datetime.datetime.strptime(enddatetime, '%Y-%m-%d %H:%M:%S')
                op.enddate= enddatetime
                op.endtime= enddatetime
                op.location= request.POST.get('form-location')
                op.subject= request.POST.get('form-subject')
                op.reason_type= request.POST.get('form-reason_type')
                op.reason= request.POST.get('form-reason')
                op.impact= request.POST.get('form-impact')
                op.remarks= request.POST.get('form-remarks')
                op.vendor= request.POST.get('form-vendor')
                op.vendor_phone= request.POST.get('form-vendor_phone')
                op.save()
                messages.success(self.request, "Operation Updated")
                return redirect('result', pk=request.POST.get('form-id'))
            else:
                form = RawOperationForm(self.request.POST or None, self.request.FILES or None)
                if form.is_valid():
                    new = Operation.objects.create(**form.cleaned_data)
                    id = new.id
                    form = Operation.objects.get(id=id)
                    subject = "A new operation has just been created by " + form.name
                    context = {
                        'form': form
                    }
                    msg_html = render_to_string('notice.html', context)
                    subject, from_email, to = subject, 'stephencheung@hk.chinamobile.com', 'stephencheung@hk.chinamobile.com'
                    html_content = msg_html
                    msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
                    msg.attach_alternative(html_content, "text/html")
                    # msg.send()
                    messages.success(self.request, "Operation Created")
                    return redirect('result', pk=id)
                else:
                    print(form.errors)
                context = {
                    "form": form
                }
                return context

class DomainListView(ListView):
    model = Operation
    context_object_name = 'operations'
    template_name = 'info.html'

    def get_context_data(self, *args, **kwargs):
        initial_data = {
            'remarks' : "N/A",
            'impact': "No Service Impact"
        }
        if self.request.method == "GET":
            context = super(DomainListView, self).get_context_data(*args, **kwargs)
            context['domain'] = Operation.objects.filter(domain__icontains=self.kwargs['domain'])
            context['domain'] = context['domain'].filter(startdate__year='2020').order_by('startdate').reverse()
            context['form'] = RawOperationForm(self.request.POST or None, initial=initial_data)
            return context

    def post(self, request, *args, **kwargs):
        if self.request.method == "POST":
            form = RawOperationForm(self.request.POST or None, self.request.FILES or None)
            if form.is_valid():
                new = Operation.objects.create(**form.cleaned_data)
                id = new.id
                form = Operation.objects.get(id=id)
                subject = "A new operation has just been created by " + form.name
                context = {
                    'form': form
                }
                msg_html = render_to_string('notice.html', context)
                subject, from_email, to = subject, 'stephencheung@hk.chinamobile.com', 'stephencheung@hk.chinamobile.com'
                html_content = msg_html
                msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
                msg.attach_alternative(html_content, "text/html")
                # msg.send()
                messages.success(self.request, "Operation Created")
                return redirect('result', pk=id)
            else:
                print(form.errors)
            context = {
                "form": form
            }
            return context

class ResultListView(AdminStaffRequiredMixin, DetailView):
    login_url = '/login/'
    model = Operation
    template_name = 'result.html'

    def get_context_data(self, **kwargs):
        initial_data = {
            'remarks' : "N/A",
            'impact': "No Service Impact"
        }
        context = super(ResultListView, self).get_context_data(**kwargs)
        context['form'] = RawOperationForm(self.request.POST or None, initial=initial_data)
        return context

    def post(self, request, *args, **kwargs):
        form = RawOperationForm(self.request.POST or None, self.request.FILES or None)
        if form.is_valid():
            new = Operation.objects.create(**form.cleaned_data)
            id = new.id
            form = Operation.objects.get(id=id)
            subject = "A new operation has just been created by " + form.name
            context = {
                'form': form
            }
            msg_html = render_to_string('notice.html', context)
            subject, from_email, to = subject, 'stephencheung@hk.chinamobile.com', 'stephencheung@hk.chinamobile.com'
            html_content = msg_html
            msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            # msg.send()
            messages.success(self.request, "Operation Created")
            return redirect('result', pk=id)
        else:
            print(form.errors)
        context = {
            "form": form
        }
        return context
