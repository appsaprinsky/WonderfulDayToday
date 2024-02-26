from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import UserCreationForm
from django.http import Http404
from .forms import SignUpForm, ToDoForm,  SpendingsForm, UploadFileForm
from django.contrib.auth.decorators import login_required
from .models import ToDo, Spendings, UploadFile
from django.contrib.auth.mixins import LoginRequiredMixin

from django.utils import timezone
from django.views.generic.list import ListView
from django.views.generic import DetailView
from django.views.generic.edit import UpdateView, DeleteView
from django.views.generic import TemplateView
from django.db.models import Sum
from .filters import SpendingsFilter
from random import randrange

from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta
from django_filters.views import FilterView

from django.template import loader
from django.http import HttpResponse
import pandas as pd
import os
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent

#---------------------- Signup Login Logout Start ----------------------
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            auth_login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'app_main/signup.html', {'form': form})


def login(request):
    if request.method == 'POST':
        user = authenticate(username=request.POST['username'],password = request.POST['password'])
        if user is not None:
            auth_login(request,user)
            return redirect('home')
        else:
            return render(request,'app_main/login.html', {'error':'Username or password is incorrect!'})
    else:
        return render(request,'app_main/login.html')

def logout(request):
    if request.method == 'POST':
        auth_logout(request)
    return redirect('home')

# def register(request):
#     return render(request, 'app_main/register.html', {'segment': 'index'})


#---------------------- Signup Login Logout End ----------------------




# @login_required(login_url="/login/")
# def index(request):
#     context = {'segment': 'index'}
#
#     html_template = loader.get_template('app_main/index.html')
#     return HttpResponse(html_template.render(context, request))
#


def index(request):
    return render(request, 'app_main/index.html', {'segment': 'index'})

def handle_uploaded_file(f):
    with open('test.csv', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)




@login_required(login_url='/login/')
def ai(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data

            UploadFile.objects.filter(user=request.user).all().delete()



            user_upload = UploadFile.objects.create(**data, user=request.user)
            user_upload.save()

            csv_data = pd.read_csv('media/media/uploads/user_'+str(request.user.id)+'/'+str(data['file'])  )
            print(csv_data)
            num = randrange(0, 5)
            if num == 0:
                prediction = 'Down by more 20 %'
            elif num == 1:
                prediction = 'Down by between 20 % to 5 %'
            elif num == 2:
                prediction = 'Random between -5 % to 5 %'
            elif num == 3:
                prediction = 'Up by between 5 % to 20 %'
            else:
                prediction = 'Up by 20 %'


            return render(request, 'app_main/ai-received.html', {'prediction': prediction})
    else:
        form = UploadFileForm()
    return render(request, 'app_main/ai.html', {'form': form})


# def ai(request):
#     if "GET" == request.method:
#         print('Hi1')
#         return render(request, 'app_main/ai.html', {'segment': 'index'})
#
#     if request.method=='POST':
#         try:
#             print('Hi2')
#             csv_file = request.FILES["csv_file"]
#             print('Hi2')
#             if not csv_file.name.endswith('.csv'):
#                 messages.error(request, 'File is not CSV type')
#                 return HttpResponseRedirect(reverse("ai"))
#
#             file_data = csv_file.read().decode("utf-8")
#             print('Hi2 22')
#             if 'shortPrediction' in request.POST:
#                 print(file_data)
#             return render(request, 'app_main/ai.html', {'segment': 'index'})
#
#         except:
#             print('Hi3')
#             return render(request, 'app_main/ai.html', {'segment': 'index'})
#
#
# @login_required(login_url='/login/')
# def ai_received(request):
#     return render(request, 'app_main/ai-received.html', {'segment': 'index'})
#
#
# def upload_data(request):
#     if 'shortPrediction' in request.POST:
#         # gaussian = pickle.load(open('gNB.sav', 'rb'))
#         # y_pred = gaussian.predict(test_data_preprocessed)
#         # output = pd.DataFrame(y_pred)
#         # output.to_csv('gaussianNB.csv')
#         #
#         # filename = 'gaussianNB.csv'
#         # response = HttpResponse(open(filename, 'rb').read(), content_type='text/csv')
#         # response['Content-Length'] = os.path.getsize(filename)
#         # response['Content-Disposition'] = 'attachment; filename=%s' % 'gaussianNB.csv'
#
#         response = HttpResponse()
#         response['prediction'] = 'up'
#         return response
#
#     if 'mediumPrediction' in request.POST:
#         # multi = pickle.load(open('classifier_multi_NB.sav', 'rb'))
#         # y_pred = multi.predict(test_data_preprocessed)
#         # output = pd.DataFrame(y_pred)
#         # output.to_csv('multi_NB.csv')
#         #
#         # filename = 'multi_NB.csv'
#         # response = HttpResponse(open(filename, 'rb').read(), content_type='text/csv')
#         # response['Content-Length'] = os.path.getsize(filename)
#         # response['Content-Disposition'] = 'attachment; filename=%s' % 'multi_NB.csv'
#
#         response = HttpResponse()
#         response['prediction'] = 'up'
#
#         return response
#
#     if 'longPrediction' in request.POST:
#         # rf = pickle.load(open('random_forest.sav', 'rb'))
#         # y_pred = rf.predict(test_data_preprocessed)
#         # output = pd.DataFrame(y_pred)
#         # output.to_csv('rf.csv')
#         #
#         # filename = 'rf.csv'
#         # response = HttpResponse(open(filename, 'rb').read(), content_type='text/csv')
#         # response['Content-Length'] = os.path.getsize(filename)
#         # response['Content-Disposition'] = 'attachment; filename=%s' % 'rf.csv'
#         response = HttpResponse()
#         response['prediction'] = 'up'
#         return response




# @login_required(login_url='/login/')
# def dashboard(request):
#     labels_spend = []
#     data_spend = []
#
#
#     labels_todo = []
#     data_todo = []
#
#     queryset = Spendings.objects.order_by('-type')[:5]
#     for spend in queryset:
#         labels_spend.append(spend.type)
#         data_spend.append(spend.value)
#
#
#     queryset = ToDo.objects.order_by('-run')
#     for todo in ['long', 'medium', 'short', 'other']:
#         labels_todo.append(todo)
#         data_todo.append(ToDo.objects.filter(user=self.request.user).filter(run=todo).count())
#
#     return render(request, 'app_main/dashboard.html', {
#         'labels_spend': labels_spend,
#         'data_spend': data_spend,
#         'labels_todo': labels_todo,
#         'data_todo': data_todo,
#
#     })

class DashboardView(LoginRequiredMixin, ListView):
    template_name = 'app_main/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        labels_spend = []
        data_spend = []
        labels_todo = []
        data_todo = []

        # queryset = Spendings.objects.order_by('-type')[:5]
        queryset = Spendings.objects.filter(user=self.request.user).values_list('type', flat=True).order_by('-type').values('type').distinct()
        for spend in queryset:
            labels_spend.append(spend['type'])
            data_spend.append(Spendings.objects.filter(user=self.request.user).filter(type=spend['type']).aggregate(Sum('value'))['value__sum'])



        queryset = ToDo.objects.order_by('-run')
        for todo in ['start', 'long', 'medium', 'short', 'other']:
            labels_todo.append(todo)
            data_todo.append(ToDo.objects.filter(user=self.request.user).filter(run=todo).count())

        month_dict = {'1': 'January',
                 '2': 'February',
                 '3': 'March',
                 '4': 'April',
                 '5': 'May',
                 '6': 'June',
                 '7': 'July',
                 '8': 'August',
                 '9': 'September',
                 '10': 'October',
                 '11': 'November',
                 '12': 'December'	}
        today_date = datetime.today()
        month_1 = today_date.month
        year_1 = today_date.year
        # print(year_1, month_1)

        first_month_1 = today_date.replace(day=1)
        month2_date = first_month_1 - timedelta(days=1)
        month_2 = month2_date.month
        year_2 = month2_date.year
        # print(year_2, month_2)


        first_month_2 = month2_date.replace(day=1)
        month3_date = first_month_2 - timedelta(days=1)
        month_3 = month3_date.month
        year_3 = month3_date.year
        # print(year_3, month_3)

        first_month_3 = month3_date.replace(day=1)
        month4_date = first_month_3 - timedelta(days=1)
        month_4 = month4_date.month
        year_4 = month4_date.year
        # print(year_4, month_4)

        first_month_4 = month4_date.replace(day=1)
        month5_date = first_month_4 - timedelta(days=1)
        month_5 = month5_date.month
        year_5 = month5_date.year
        # print(year_5, month_5)

        first_month_5 = month5_date.replace(day=1)
        month6_date = first_month_5 - timedelta(days=1)
        month_6 = month6_date.month
        year_6 = month6_date.year
        # print(year_6, month_6)





        list_data_6month = []
        list_labels_6month = [month_dict[str(month_6)], month_dict[str(month_5)], month_dict[str(month_4)], month_dict[str(month_3)], month_dict[str(month_2)], month_dict[str(month_1)]]

        month_year_1_6_range = [(month_6, year_6), (month_5, year_5), (month_4, year_4), (month_3, year_3), (month_2, year_2), (month_1, year_1)]


        for mon, yea in month_year_1_6_range:
            obj_total = Spendings.objects.filter(user=self.request.user).filter(date_of_spending__month__gte=str(mon), date_of_spending__year__gte=str(yea), date_of_spending__month__lte=str(mon), date_of_spending__year__lte=str(yea))
            # print(obj_total)
            obj = obj_total.aggregate(Sum('value'))['value__sum']
            # print(Spendings.objects.filter(user=self.request.user).filter(date_of_spending__year__gte=yea, date_of_spending__month__gte=mon))
            if not isinstance(obj, (int, float, complex)):
                obj = 0
            list_data_6month.append(obj)
            # print(yea)
            # print(mon)
            # print(list_data_6month)







        context["labels_spend"] = labels_spend
        context["data_spend"] = data_spend
        context["labels_todo"] = labels_todo
        context["data_todo"] = data_todo

        context["Long_Run"] = ToDo.objects.filter(user=self.request.user).filter(run='long')
        context["Medium_Run"] = ToDo.objects.filter(user=self.request.user).filter(run='medium')
        context["Short_Run"] = ToDo.objects.filter(user=self.request.user).filter(run='short')

        context["Long_Run_num"] = data_todo[1]
        context["Medium_Run_num"] = data_todo[2]
        context["Short_Run_num"] = data_todo[3]

        context["labels_6month"] = list_labels_6month
        context["data_6month"] = list_data_6month
        return context


    def get_queryset(self):
        return Spendings.objects.filter(user=self.request.user)





# def login(request):
#     return render(request, 'app_main/login.html', {'segment': 'index'})

def pageuser(request):
    return render(request, 'app_main/page-user.html', {'segment': 'index'})

#
# def dashboard(request):
#     return render(request, 'app_main/dashboard.html', {'segment': 'index'})








#---------------------- ToDos Start ----------------------

# @login_required(login_url='/login/')
# def todo(request):
#     return render(request, 'app_main/to-do.html', {'segment': 'index'})

class ToDoListView(LoginRequiredMixin, ListView):

    model = ToDo
    # paginate_by = 2  # if pagination is desired
    template_name = 'app_main/to-do.html'
    ordering = ['deadline_date']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        context['long_to_do'] = ToDo.objects.filter(run='long')
        context['medium_to_do'] = ToDo.objects.filter(run='medium')
        context['short_to_do'] = ToDo.objects.filter(run='short')
        context['others_to_do'] = ToDo.objects.filter(run='other')
        return context

    def get_queryset(self):
        return ToDo.objects.filter(user=self.request.user)




class ToDoDetailView(LoginRequiredMixin, DetailView):
    model = ToDo
    template_name = 'app_main/to-do-detail.html'


    def get_context_data(self, **kwargs):
        context = super(ToDoDetailView,self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        #
        # context['long_to_do'] = ToDo.objects.all()#filter(run='Long Run ToDo')
        # # print('long_to_do')
        return context



    def get_queryset(self):
        return ToDo.objects.filter(user=self.request.user)




class ToDoUpdateView(LoginRequiredMixin, UpdateView):
    model = ToDo
    template_name = 'app_main/to-do-update.html'
    fields = ('titel', 'run', 'importance', 'completed', 'detailed_description', 'deadline_date',)
    success_url = '/to-do'

    def get_queryset(self):
        return ToDo.objects.filter(user=self.request.user)


class ToDoDeleteView(LoginRequiredMixin, DeleteView):
    model = ToDo
    template_name = 'app_main/to-do-delete.html'
    success_url = '/to-do'
    def get_queryset(self):
        return ToDo.objects.filter(user=self.request.user)






@login_required(login_url='/login/')
def todoadd(request):
    if request.method == 'POST':
        form = ToDoForm(request.POST)
        if form.is_valid():
            # form.save(commit=False)
            # form.user = request.user
            # form.save()

            data = form.cleaned_data

            user_todo = ToDo.objects.create(**data, user=request.user)
            user_todo.save()
            return redirect('to-do')
    else:
        form = ToDoForm()
    return render(request, 'app_main/to-do-add.html', {'form': form})




#---------------------- ToDos End ----------------------





#---------------------- Spendings Pages Start ----------------------

# @login_required(login_url='/login/')
# def spendings(request):
#     return render(request, 'app_main/spendings.html', {'segment': 'index'})

@login_required(login_url='/login/')
def spendingsadd(request):
    if request.method == 'POST':
        form = SpendingsForm(request.POST)
        if form.is_valid():
            # form.save(commit=False)
            # form.user = request.user
            # form.save()

            data = form.cleaned_data

            user_todo = Spendings.objects.create(**data, user=request.user)
            user_todo.save()
            return redirect('spendings')
    else:
        form = SpendingsForm()
    return render(request, 'app_main/spendings-add.html', {'form': form})

class SpendingsListView(LoginRequiredMixin, FilterView):

    model = Spendings
    paginate_by = 10  # if pagination is desired
    template_name = 'app_main/spendings.html'
    ordering = ['type']
    filterset_class = SpendingsFilter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

    def get_queryset(self):
        return Spendings.objects.filter(user=self.request.user)



class SpendingsDetailView(LoginRequiredMixin, DetailView):
    model = Spendings
    template_name = 'app_main/spendings-detail.html'

    def get_queryset(self):
        return Spendings.objects.filter(user=self.request.user)

class SpendingsUpdateView(LoginRequiredMixin, UpdateView):
    model = Spendings
    template_name = 'app_main/spendings-update.html'
    fields = ('type', 'value', 'titel', 'importance', 'detailed_description','date_of_spending',)
    success_url = '/spendings'

    def get_queryset(self):
        return Spendings.objects.filter(user=self.request.user)


class SpendingsDeleteView(LoginRequiredMixin, DeleteView):
    model = Spendings
    template_name = 'app_main/spendings-delete.html'
    success_url = '/spendings'

    def get_queryset(self):
        return Spendings.objects.filter(user=self.request.user)




#---------------------- Spendings Pages Start ----------------------








