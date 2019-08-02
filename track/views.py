from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.http import Http404
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from .models import ActivityTracker, Activity
import json
from datetime import timedelta, datetime, date
from django.db.models import Sum

today = date.today()

# dateStr = today.strftime("%d %b %Y ")

@csrf_exempt
def get_records(request, *args, **kwargs):
    request_data = json.loads(request.body)
    daily_activities_dict = {}
    weekly_activities_dict = {}
    monthly_activities_dict = {}
    custom_date_activities_dict = {}
    custom_week_activities_dict = {}
    tilldate_activities_dict = {}
    monthnum_activities_dict = {}

# --------------------------Custom Date--------------------------------------

    if "date" in request_data:
        date = request_data["date"]
        m, d, y = map(int, date.split('/'))
        custom_date = datetime(y, m, d)
        month = custom_date - timedelta(days=30)
        week = custom_date - timedelta(days=7)
        custom_date_activities = ActivityTracker.objects.filter(date=custom_date)
        custom_date_elapsed = ActivityTracker.objects.filter(date=custom_date).values('category_name').annotate(Sum('elapsed_time'))
        custom_date_categories = ActivityTracker.objects.filter(date=custom_date).values('category_name','category_bar_color','category_group_num').distinct()
        custom_date_gnum_elapsed = ActivityTracker.objects.filter(date=custom_date).values('category_group_num').annotate(Sum('elapsed_time'))
        
        for i, custom_date_activity in enumerate(custom_date_activities):
            custom_date_activities_dict[i] = {
                "id":custom_date_activity.id,
                "date":custom_date_activity.date.strftime("%d %b %Y"),
                "start_time":custom_date_activity.start_time.strftime("%H:%M"),
                "end_time":custom_date_activity.end_time.strftime("%H:%M"),
                "elapsed_time":custom_date_activity.elapsed_time,
                "category_name":custom_date_activity.category_name,
                "category_bar_color":custom_date_activity.category_bar_color,
                "category_group_num":custom_date_activity.category_group_num
        }
    
        custom_date_activities_dict["total"] = {}
        for elapsed_time in custom_date_elapsed:
            custom_date_activities_dict["total"][elapsed_time["category_name"]] = elapsed_time["elapsed_time__sum"]

        custom_date_activities_dict["category"] = {}
        for custom_date_category in custom_date_categories:
            custom_date_activities_dict["category"][custom_date_category["category_name"]] = {
                "category_bar_color":custom_date_category["category_bar_color"],
                "category_group_num":custom_date_category["category_group_num"],
                "total":custom_date_activities_dict["total"][custom_date_category["category_name"]]
            }
        
        custom_date_activities_dict["groups"] = {}
        for elapsed_time in custom_date_gnum_elapsed:
            custom_date_activities_dict["groups"]["Group " + str(elapsed_time["category_group_num"])] = elapsed_time["elapsed_time__sum"]

        start_week = custom_date - timedelta(custom_date.weekday())
        # end_week = start_week + timedelta(6)
        custom_week_activities = ActivityTracker.objects.filter(date__range=[start_week, custom_date])
        custom_week_elapsed = ActivityTracker.objects.filter(date__range=[start_week, custom_date]).values('category_name').annotate(Sum('elapsed_time'))
        custom_week_categories = ActivityTracker.objects.filter(date__range=[start_week, custom_date]).values('category_name','category_bar_color','category_group_num').distinct()
        custom_week_gnum_elapsed = ActivityTracker.objects.filter(date__range=[start_week, custom_date]).values('category_group_num').annotate(Sum('elapsed_time'))


        for i, custom_week_activity in enumerate(custom_week_activities):
            custom_week_activities_dict[i] = {
                "id":custom_week_activity.id,
                "date":custom_week_activity.date.strftime("%d %b %Y"),
                "start_time":custom_week_activity.start_time.strftime("%H:%M"),
                "end_time":custom_week_activity.end_time.strftime("%H:%M"),
                "elapsed_time":custom_week_activity.elapsed_time,
                "category_name":custom_week_activity.category_name,
                "category_bar_color":custom_week_activity.category_bar_color,
                "category_group_num":custom_week_activity.category_group_num
        }
    
        custom_week_activities_dict["total"] = {}
        for elapsed_time in custom_week_elapsed:
            custom_week_activities_dict["total"][elapsed_time["category_name"]] = elapsed_time["elapsed_time__sum"]

        custom_week_activities_dict["category"] = {}
        for custom_week_category in custom_week_categories:
            custom_week_activities_dict["category"][custom_week_category["category_name"]] = {
                "category_bar_color":custom_week_category["category_bar_color"],
                "category_group_num":custom_week_category["category_group_num"],
                "total":custom_week_activities_dict["total"][custom_week_category["category_name"]]
            }

        custom_week_activities_dict["groups"] = {}
        for elapsed_time in custom_week_gnum_elapsed:
            custom_week_activities_dict["groups"]["Group " + str(elapsed_time["category_group_num"])] = elapsed_time["elapsed_time__sum"]



    daily_activities = ActivityTracker.objects.filter(date=today)
    daily_categories = ActivityTracker.objects.filter(date=today).values('category_name','category_bar_color','category_group_num').distinct()
    daily_elapsed= ActivityTracker.objects.filter(date=today).values('category_name').annotate(Sum('elapsed_time'))
    daily_gnum_elapsed= ActivityTracker.objects.filter(date=today).values('category_group_num').annotate(Sum('elapsed_time'))

    weekly_activities = ActivityTracker.objects.filter(date__range=[datetime.date(week), custom_date])
    weekly_categories = ActivityTracker.objects.filter(date__range=[datetime.date(week), custom_date]).values('category_name','category_bar_color','category_group_num').distinct()
    weekly_elapsed = ActivityTracker.objects.filter(date__range=[datetime.date(week), custom_date]).values('category_name').annotate(Sum('elapsed_time'))
    weekly_gnum_elapsed = ActivityTracker.objects.filter(date__range=[datetime.date(week), custom_date]).values('category_group_num').annotate(Sum('elapsed_time'))

    monthly_activities = ActivityTracker.objects.filter(date__range=[datetime.date(month), custom_date])
    monthly_elapsed = ActivityTracker.objects.filter(date__range=[datetime.date(month), custom_date]).values('category_name').annotate(Sum('elapsed_time'))
    monthly_categories = ActivityTracker.objects.filter(date__range=[datetime.date(month), custom_date]).values('category_name','category_bar_color','category_group_num').distinct()
    monthly_gnum_elapsed = ActivityTracker.objects.filter(date__range=[datetime.date(month), custom_date]).values('category_group_num').annotate(Sum('elapsed_time'))

    monthnum_activities = ActivityTracker.objects.filter(date__month=int(m))
    monthnum_elapsed = ActivityTracker.objects.filter(date__month="8").values('category_name').annotate(Sum('elapsed_time'))
    monthnum_categories = ActivityTracker.objects.filter(date__month="8").values('category_name','category_bar_color','category_group_num').distinct()
    monthnum_gnum_elapsed = ActivityTracker.objects.filter(date__month="8").values('category_group_num').annotate(Sum('elapsed_time'))

    tilldate_activities = ActivityTracker.objects.all()
    tilldate_elapsed = ActivityTracker.objects.all().values('category_name').annotate(Sum('elapsed_time'))
    tilldate_categories = ActivityTracker.objects.all().values('category_name','category_bar_color','category_group_num').distinct()
    tilldate_gnum_elapsed = ActivityTracker.objects.all().values('category_group_num').annotate(Sum('elapsed_time'))

# --------------------------Daily--------------------------------------

    for i, daily_activity in enumerate(daily_activities):
        daily_activities_dict[i] = {
            "id":daily_activity.id,
            "date":daily_activity.date.strftime("%d %b %Y"),
            "start_time":daily_activity.start_time.strftime("%H:%M"),
            "end_time":daily_activity.end_time.strftime("%H:%M"),
            "elapsed_time":daily_activity.elapsed_time,
            "category_name":daily_activity.category_name,
            "category_bar_color":daily_activity.category_bar_color,
            "category_group_num":daily_activity.category_group_num
    }

    daily_activities_dict["total"] = {}
    for elapsed_time in daily_elapsed:
        daily_activities_dict["total"][elapsed_time["category_name"]] = elapsed_time["elapsed_time__sum"]

    daily_activities_dict["category"] = {}
    for daily_category in daily_categories:
        daily_activities_dict["category"][daily_category["category_name"]] = {
            "category_bar_color":daily_category["category_bar_color"],
            "category_group_num":daily_category["category_group_num"],
            "total":daily_activities_dict["total"][daily_category["category_name"]]
        }
    
    daily_activities_dict["groups"] = {}
    for elapsed_time in daily_gnum_elapsed:
        daily_activities_dict["groups"]["Group " + str(elapsed_time["category_group_num"])] = elapsed_time["elapsed_time__sum"]

# --------------------------Weekly--------------------------------------
     
    for i, weekly_activity in enumerate(weekly_activities):
        weekly_activities_dict[i] = {
            "id":weekly_activity.id,
            "date":weekly_activity.date.strftime("%d %b %Y"),
            "start_time":weekly_activity.start_time.strftime("%H:%M"),
            "end_time":weekly_activity.end_time.strftime("%H:%M"),
            "elapsed_time":weekly_activity.elapsed_time,
            "category_name":weekly_activity.category_name,
            "category_bar_color":weekly_activity.category_bar_color,
            "category_group_num":weekly_activity.category_group_num
        }
    
    weekly_activities_dict["total"] = {}
    for elapsed_time in weekly_elapsed:
        weekly_activities_dict["total"][elapsed_time["category_name"]] = elapsed_time["elapsed_time__sum"]

    weekly_activities_dict["category"] = {}
    for weekly_category in weekly_categories:
        weekly_activities_dict["category"][weekly_category["category_name"]] = {
            "category_bar_color":weekly_category["category_bar_color"],
            "category_group_num":weekly_category["category_group_num"],
            "total":weekly_activities_dict["total"][weekly_category["category_name"]]
        }
    
    weekly_activities_dict["groups"] = {}
    for elapsed_time in weekly_gnum_elapsed:
        weekly_activities_dict["groups"]["Group " + str(elapsed_time["category_group_num"])] = elapsed_time["elapsed_time__sum"]

# --------------------------Monthly Num--------------------------------------
    if "date" in request_data:
        for i, monthnum_activity in enumerate(monthnum_activities):
            monthnum_activities_dict[i] = {
                "id":monthnum_activity.id,
                "date":monthnum_activity.date.strftime("%d %b %Y"),
                "start_time":monthnum_activity.start_time.strftime("%H:%M"),
                "end_time":monthnum_activity.end_time.strftime("%H:%M"),
                "elapsed_time":monthnum_activity.elapsed_time,
                "category_name":monthnum_activity.category_name,
                "category_bar_color":monthnum_activity.category_bar_color,
                "category_group_num":monthnum_activity.category_group_num
            }
        
        monthnum_activities_dict["total"] = {}
        for elapsed_time in monthnum_elapsed:
            monthnum_activities_dict["total"][elapsed_time["category_name"]] = elapsed_time["elapsed_time__sum"]

        monthnum_activities_dict["category"] = {}
        for monthnum_category in monthnum_categories:
            monthnum_activities_dict["category"][monthnum_category["category_name"]] = {
                "category_bar_color":monthnum_category["category_bar_color"],
                "category_group_num":monthnum_category["category_group_num"],
                "total":monthnum_activities_dict["total"][monthnum_category["category_name"]]
            }
        
        monthnum_activities_dict["groups"] = {}
        for elapsed_time in monthnum_gnum_elapsed:
            monthnum_activities_dict["groups"]["Group " + str(elapsed_time["category_group_num"])] = elapsed_time["elapsed_time__sum"]

# --------------------------Monthly--------------------------------------

    for i, monthly_activity in enumerate(monthly_activities):
            monthly_activities_dict[i] = {
                "id":monthly_activity.id,
                "date":monthly_activity.date.strftime("%d %b %Y"),
                "start_time":monthly_activity.start_time.strftime("%H:%M"),
                "end_time":monthly_activity.end_time.strftime("%H:%M"),
                "elapsed_time":monthly_activity.elapsed_time,
                "category_name":monthly_activity.category_name,
                "category_bar_color":monthly_activity.category_bar_color,
                "category_group_num":monthly_activity.category_group_num
            }
    
    monthly_activities_dict["total"] = {}
    for elapsed_time in monthly_elapsed:
        monthly_activities_dict["total"][elapsed_time["category_name"]] = elapsed_time["elapsed_time__sum"]

    monthly_activities_dict["category"] = {}
    for monthly_category in monthly_categories:
        monthly_activities_dict["category"][monthly_category["category_name"]] = {
            "category_bar_color":monthly_category["category_bar_color"],
            "category_group_num":monthly_category["category_group_num"],
            "total":monthly_activities_dict["total"][monthly_category["category_name"]]
        }

    monthly_activities_dict["groups"] = {}
    for elapsed_time in monthly_gnum_elapsed:
        monthly_activities_dict["groups"]["Group " + str(elapsed_time["category_group_num"])] = elapsed_time["elapsed_time__sum"]

# --------------------------Till Date--------------------------------------
    
    for i, tilldate_activity in enumerate(tilldate_activities):
        tilldate_activities_dict[i] = {
            "id":tilldate_activity.id,
            "date":tilldate_activity.date.strftime("%d %b %Y"),
            "start_time":tilldate_activity.start_time.strftime("%H:%M"),
            "end_time":tilldate_activity.end_time.strftime("%H:%M"),
            "elapsed_time":tilldate_activity.elapsed_time,
            "category_name":tilldate_activity.category_name,
            "category_bar_color":tilldate_activity.category_bar_color,
            "category_group_num":tilldate_activity.category_group_num
        }
    
    tilldate_activities_dict["total"] = {}
    for elapsed_time in tilldate_elapsed:
        tilldate_activities_dict["total"][elapsed_time["category_name"]] = elapsed_time["elapsed_time__sum"]

    tilldate_activities_dict["category"] = {}
    for tilldate_category in tilldate_categories:
        tilldate_activities_dict["category"][tilldate_category["category_name"]] = {
            "category_bar_color":tilldate_category["category_bar_color"],
            "category_group_num":tilldate_category["category_group_num"],
            "total":tilldate_activities_dict["total"][tilldate_category["category_name"]]
        }
    
    tilldate_activities_dict["groups"] = {}
    for elapsed_time in tilldate_gnum_elapsed:
        tilldate_activities_dict["groups"]["Group " + str(elapsed_time["category_group_num"])] = elapsed_time["elapsed_time__sum"]

    
    return JsonResponse({
        "custom_date":custom_date_activities_dict,
        "tillweek":custom_week_activities_dict,
        "today":daily_activities_dict,
        "last_7":weekly_activities_dict,
        "month":monthnum_activities_dict,
        "last_30":monthly_activities_dict,
        "tilldate":tilldate_activities_dict
    })

@csrf_exempt
def add_activity(request):
    request_data = json.loads(request.body)

    # loading request data
    date = request_data["date"]
    start_time = request_data["start_time"]
    end_time = request_data["end_time"]
    elapsed_time = request_data["elapsed_time"]
    category_name = request_data["category_name"]
    category_bar_color = request_data["category_bar_color"]
    category_group_num = request_data["category_group_num"]

    # date_entry = "2019,7,22"
    m, d, y = map(int, date.split('/'))
    custom_date = datetime(y, m, d)

    row = ActivityTracker(
        date=custom_date,
        start_time=start_time,
        end_time=end_time,
        elapsed_time=elapsed_time,
        category_name=category_name,
        category_bar_color=category_bar_color,
        category_group_num=category_group_num
        )
    row.save()
    return JsonResponse({"status":"True", "message":"Activity has been added."})



@csrf_exempt
def add_category(request):
    request_data = json.loads(request.body)
    # loading request data
    name = request_data["name"]
    bar_color = request_data["bar_color"]
    group_num = request_data["group_num"]

    row = Activity(
        name=name,
        bar_color=bar_color,
        group_num=group_num
    )
    row.save()
    return JsonResponse({"status":"True", "message":"Category has been added."})


@csrf_exempt
def category(request, *args, **kwargs):
    categories_dict = {}
    categories = Activity.objects.all()
    for i, category in enumerate(categories):
        categories_dict[i] = {
            "id":category.id,
            "name":category.name,
            "bar_color":category.bar_color,
            "group_num":category.group_num
            }

    return JsonResponse({"categories_dict":categories_dict})


@csrf_exempt
def custom_category(request, *args, **kwargs):
    request_data = json.loads(request.body)

    category_name = request_data["name"]
    categories_dict = {}
    categories = Activity.objects.filter(name__iexact=category_name)
    for i, category in enumerate(categories):
        categories_dict[i] = {
            "id":category.id,
            "name":category.name,
            "bar_color":category.bar_color,
            "group_num":category.group_num
            }

    return JsonResponse({"categories_dict":categories_dict})


@csrf_exempt
def edit_category(request):
    request_data = json.loads(request.body)
    # loading request data
    _id = request_data["id"]
    name = request_data["name"]
    bar_color = request_data["bar_color"]
    group_num = request_data["group_num"]

    if bar_color:
        activities = ActivityTracker.objects.filter(category_name__iexact=name)
        for a in activities:
            a.category_bar_color = bar_color
            a.save()
    
    if group_num:
        activities = ActivityTracker.objects.filter(category_name__iexact=name)
        for a in activities:
            a.category_group_num = group_num
            a.save()

    activity = Activity.objects.get(pk=_id)
    activity.name = name
    activity.bar_color = bar_color
    activity.group_num = group_num
    activity.save()

    return JsonResponse({"status":"True", "message":"Category has been edited."})

@csrf_exempt
def delete_category(request):
    request_data = json.loads(request.body)

    # loading request data
    _id = request_data["id"]
    activity = Activity.objects.get(pk=_id)
    activity.delete()
    return JsonResponse({"status":"True", "message":"Category has been deleted."})

@csrf_exempt
def delete_activity(request):
    request_data = json.loads(request.body)

    # loading request data
    _id = request_data["id"]
    activity = ActivityTracker.objects.get(pk=_id)
    activity.delete()
    return JsonResponse({"status":"True", "message":"Activity has been deleted."})






