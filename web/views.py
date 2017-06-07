from itertools import chain

from django.conf import settings
from django.core import serializers
from django.http import JsonResponse
from django.shortcuts import render, HttpResponse, Http404, get_object_or_404, HttpResponseRedirect, render_to_response
from django.urls import reverse
from .models import *


def getContext():
    primary_navbar = PrimaryNavigationMenu.objects.all().order_by('order')
    secondary_navbar = SecondaryNavigationMenu.objects.all().order_by('order')
    primary_menu = PrimaryMenu.objects.all().order_by('order')
    latest_news = LatestNews.objects.filter(visible=True)
    notices = Notice.objects.filter(visible=True)
    secondary_menu = []
    for menu in primary_menu:
        secondary_menu = SecondaryMenu.objects.all()
    marquee = Marquee.objects.all().order_by('order')
    context = {
        'primary_navbar': primary_navbar,
        'secondary_navbar': secondary_navbar,
        'primary_menu': primary_menu,
        'secondary_menu': secondary_menu,
        'latest_news': latest_news,
        'notices': notices,
        'marquee': marquee
    }
    return context


def home(request):
    context = getContext()
    return render(request, 'home.html', context=context)


def timetable(request):
    morning = TimeTable.objects.filter(shift='M').order_by('semester') or []
    evening = TimeTable.objects.filter(shift='E').order_by('semester') or []

    context = getContext()
    context['morning'] = morning
    context['evening'] = evening
    return render(request, 'timetable.html', context=context)


def attendance(request):
    morning = Attendance.objects.filter(shift='M').order_by('semester') or []
    evening = Attendance.objects.filter(shift='E').order_by('semester') or []
    context = getContext()
    context['morning'] = morning
    context['evening'] = evening
    return render(request, 'attendance.html', context=context)


def syllabus(request):
    syllabus = Syllabus.objects.all().order_by('semester') or []
    context = getContext()
    context['syllabus'] = syllabus
    return render(request, 'syllabus.html', context=context)

def facilities(request):
    context = getContext()
    return render(request, 'facilities.html', context=context)


def society(request):
    societies = StudentSociety.objects.order_by('order') or []
    context = getContext()
    context['societies'] = societies
    return render(request, 'society.html', context=context)


def achievements(request):
    achievements = Achievement.objects.all().order_by('order') or []
    context = getContext()
    context['achievements'] = achievements
    return render(request, 'achievements.html', context=context)


def events(request):
    try:
        event = Event.objects.all().order_by('-date')
    except:
        event = Event.objects.all()
    context = getContext()
    context['events'] = event
    return render(request, 'events.html', context=context)

#
# Available Department Choices are ::
# CSE, IT, ECE, EEE, APPLIED SCIENCES


def get_modifier(department, a=None, b=None):
    '''
        Sorting Modes are ::
        ('1', 'Name wise')
        ('2', 'Designation wise')
        ('3', 'Date-of-joining wise')
    '''
    modifier = ''
    a = a or department.sort_faculty
    b = b or department.sorting_order
    a = int(a)
    b = int(b)
    if a == 1:
        modifier = 'full_name'
    elif a == 2:
        modifier = 'designation'
    elif a == 3:
        modifier = 'date_of_joining'
    if b == 2:
        modifier = '-' + modifier
    return modifier


def get_faculties(department, modifier, a=False, b=False, c=False, d=False):
    context = {}
    if department.display_1st_faculty or a:
        hod = Faculty.objects.filter(department=department, shift='M', designation='1HOD').order_by('full_name')
        morning = Faculty.objects.filter(
            category__icontains='teaching', department=department, shift='M').exclude(designation='1HOD').order_by(modifier, 'full_name') or []
        morning = list(chain(hod, morning))
        context['morning'] = morning
    if department.display_2nd_faculty or b:
        hod = Faculty.objects.filter(department=department, shift='E', designation='1HOD').order_by('full_name')
        evening = Faculty.objects.filter(
            category__icontains='teaching', department=department, shift='E').exclude(designation='1HOD').order_by(modifier, 'full_name') or []
        evening = list(chain(hod, evening))
        context['evening'] = evening
    if department.display_1st_assistant or c:
        mlab = Faculty.objects.filter(
            category__icontains='assistant', department=department, shift='M').order_by(modifier, 'full_name') or []
        context['mlab'] = mlab
    if department.display_2nd_assistant or d:
        elab = Faculty.objects.filter(
            category__icontains='assistant', department=department, shift='E').order_by(modifier, 'full_name') or []
        context['elab'] = elab
    return context

def get_modifier_new(sort, order):

    sort = int(sort)
    order = int(order)

    if sort == 1:
        modifier = 'full_name'
    elif sort == 2:
        modifier = 'designation'
    elif sort == 3:
        modifier = 'date_of_joining'
    else:
        modifier = 'full_name'
    if order == 2:
        modifier = '-' + modifier
    return modifier

def cse(request, sort=-1, order=-1):
    department = Department.objects.get(department='CSE')
    tabs = department.departmentpage_set.all().order_by('order')

    if sort == -1:
        modifier = get_modifier(department)
    else:
        modifier = get_modifier_new(sort, order)

    context = getContext()
    context = context.copy()
    context.update(get_faculties(department, modifier))
    context['settings'] = department
    context['tabs'] = tabs
    context['heading'] = 'Computer Science Engineering'
    return render(request, 'faculty.html', context=context)


def it(request, sort=-1, order=-1):
    department = Department.objects.get(department='IT')
    tabs = department.departmentpage_set.all().order_by('order')
    if sort == -1:
        modifier = get_modifier(department)
    else:
        modifier = get_modifier_new(sort, order)
    context = getContext()
    context = context.copy()
    context.update(get_faculties(department, modifier))
    context['settings'] = department
    context['tabs'] = tabs
    context['heading'] = 'Information technology'
    return render(request, 'faculty.html', context=context)


def ece(request, sort=-1, order=-1):
    department = Department.objects.get(department='ECE')
    tabs = department.departmentpage_set.all().order_by('order')
    if sort == -1:
        modifier = get_modifier(department)
    else:
        modifier = get_modifier_new(sort, order)
    context = getContext()
    context = context.copy()
    context.update(get_faculties(department, modifier))
    context['settings'] = department
    context['tabs'] = tabs
    context['heading'] = 'Electronics and Communication Engineering'
    return render(request, 'faculty.html', context=context)


def eee(request, sort=-1, order=-1):
    department = Department.objects.get(department='EEE')
    tabs = department.departmentpage_set.all().order_by('order')
    if sort == -1:
        modifier = get_modifier(department)
    else:
        modifier = get_modifier_new(sort, order)
    context = getContext()
    context = context.copy()
    context.update(get_faculties(department, modifier))
    context['settings'] = department
    context['tabs'] = tabs
    context['heading'] = 'Electrical and Electronics Engineering'
    return render(request, 'faculty.html', context=context)


def ap(request, sort=-1, order=-1):
    department = Department.objects.get(department='APPLIED SCIENCES')
    tabs = department.departmentpage_set.all().order_by('order')
    if sort == -1:
        modifier = get_modifier(department)
    else:
        modifier = get_modifier_new(sort, order)
    context = getContext()
    context = context.copy()
    context.update(get_faculties(department, modifier))
    context['settings'] = department
    context['tabs'] = tabs
    context['heading'] = 'Applied Science'
    return render(request, 'faculty.html', context=context)


def faculty_api(request, department, shift, teaching, types, order):
    if request.method != 'GET' or not request.is_ajax():
        return HttpResponse(status=400)
    dep = get_object_or_404(Department, department__icontains=department)
    modifier = get_modifier(dep, types, order)
    if teaching=='1' and shift=='M':
        context = get_faculties(dep, modifier, a=True)
        index='morning'
    elif teaching=='0' and shift=='M':
        context = get_faculties(dep, modifier, b=True)
        index='mlab'
    elif teaching=='1' and shift=='E':
        context = get_faculties(dep, modifier, c=True)
        index='evening'
    elif teaching=='0' and shift=='E':
        context = get_faculties(dep, modifier, d=True)
        index='elab'
    else:
        return HttpResponse(status=400)
    try:
        result = serializers.serialize('json', context[index])
        return HttpResponse(result, content_type='application/json')
    except Exception as e:
        return HttpResponse(str(e), status=400)


def latestNews(request):
    news = LatestNews.objects.all().order_by('-created_at')
    context = getContext()
    context['news'] = news
    return render(request, 'latest.html', context=context)


def notices(request):
    notices = Notice.objects.all().order_by('-created_at')
    context = getContext()
    context['notices'] = notices
    return render(request, 'notices.html', context=context)


def custom(request, key):
    filters = [' ', '@', '#', '^', '!', '&', '~', '/', '`']
    Flag = True
    for c in filters:
        if c in key:
            Flag = False
            break
    if not Flag:
        return render_to_response('404.html')
    key = '/' + key
    try:
      page = Page.objects.get(link=key)
    except:
      return render_to_response('404.html')
    tabs = page.tab_set.all().order_by('order')
    context = getContext()
    context['tabs'] = tabs
    return render(request, 'general.html', context=context)


def send_to_notice(request, pk):
    if not request.user.is_superuser:
        return HttpResponseRedirect(reverse('latest_news'))
    try:
        item = LatestNews.objects.get(pk=pk)
    except:
        return HttpResponseRedirect(reverse('latest_news'))
    notice = Notice()
    notice.title = item.title
    notice.link = item.link
    notice.files = item.files
    notice.new = item.new
    notice.visible = item.visible
    notice.additional_title = item.additional_title
    notice.additional_link = item.additional_link
    notice.additional_files = item.additional_files
    notice.save()
    notice.created_at = item.created_at
    notice.save()
    item.delete()
    return HttpResponseRedirect(reverse('latest_news'))
