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
month = datetime.now() - timedelta(days=30)
week = datetime.now() - timedelta(days=7)
today = date.today()

# dateStr = today.strftime("%d %b %Y ")

@csrf_exempt
def get_records(request, *args, **kwargs):
    request_data = json.loads(request.body)
    daily_activities_dict = {}
    daily_elapsedtime = 0
    weekly_activities_dict = {}
    weekly_elapsedtime = 0
    monthly_activities_dict = {}
    monthly_elapsedtime = 0
    custom_date_activities_dict = {}
    custom_date_elapsedtime = 0
    tilldate_activities_dict = {}
    tilldate_elapsedtime = 0

    if "date" in request_data:
        date = request_data["date"]
        m, d, y = map(int, date.split('/'))
        custom_date = datetime(y, m, d)
        custom_date_activities = ActivityTracker.objects.filter(date=custom_date)

        for i, custom_date_activity in enumerate(custom_date_activities):
            custom_date_elapsedtime += custom_date_activity.elapsed_time
            custom_date_activities_dict[i] = {
                "date":custom_date_activity.date.strftime("%d %b %Y"),
                "start_time":custom_date_activity.start_time.strftime("%H:%M"),
                "end_time":custom_date_activity.end_time.strftime("%H:%M"),
                "elapsed_time":custom_date_activity.elapsed_time,
                "category_name":custom_date_activity.category_name,
                "category_bar_color":custom_date_activity.category_bar_color,
                "category_group_num":custom_date_activity.category_group_num
            }

        custom_date_activities_dict["custom_date_elapsedtime"] = custom_date_elapsedtime

    daily_activities = ActivityTracker.objects.filter(date=today)
    weekly_activities = ActivityTracker.objects.filter(date__gte=datetime.date(week))
    monthly_activities = ActivityTracker.objects.filter(date__gte=datetime.date(month))
    tilldate_activities = ActivityTracker.objects.all()


    
    for i, daily_activity in enumerate(daily_activities):
        daily_elapsedtime += daily_activity.elapsed_time
        daily_activities_dict[i] = {
            "date":daily_activity.date.strftime("%d %b %Y"),
            "start_time":daily_activity.start_time.strftime("%H:%M"),
            "end_time":daily_activity.end_time.strftime("%H:%M"),
            "elapsed_time":daily_activity.elapsed_time,
            "category_name":daily_activity.category_name,
            "category_bar_color":daily_activity.category_bar_color,
            "category_group_num":daily_activity.category_group_num
        }
    
    daily_activities_dict["daily_elapsedtime"] = daily_elapsedtime

        
    for i, weekly_activity in enumerate(weekly_activities):
        weekly_elapsedtime += weekly_activity.elapsed_time
        weekly_activities_dict[i] = {
            "date":weekly_activity.date.strftime("%d %b %Y"),
            "start_time":weekly_activity.start_time.strftime("%H:%M"),
            "end_time":weekly_activity.end_time.strftime("%H:%M"),
            "elapsed_time":weekly_activity.elapsed_time,
            "category_name":weekly_activity.category_name,
            "category_bar_color":weekly_activity.category_bar_color,
            "category_group_num":weekly_activity.category_group_num
        }

    weekly_activities_dict["weekly_elapsedtime"] = weekly_elapsedtime

    
    
    for i, monthly_activity in enumerate(monthly_activities):
        monthly_elapsedtime += monthly_activity.elapsed_time
        monthly_activities_dict[i] = {
            "date":monthly_activity.date.strftime("%d %b %Y"),
            "start_time":monthly_activity.start_time.strftime("%H:%M"),
            "end_time":monthly_activity.end_time.strftime("%H:%M"),
            "elapsed_time":monthly_activity.elapsed_time,
            "category_name":monthly_activity.category_name,
            "category_bar_color":monthly_activity.category_bar_color,
            "category_group_num":monthly_activity.category_group_num
        }

    monthly_activities_dict["monthly_elapsedtime"] = monthly_elapsedtime

    
    for i, tilldate_activity in enumerate(tilldate_activities):
        tilldate_elapsedtime += tilldate_activity.elapsed_time
        tilldate_activities_dict[i] = {
            "date":tilldate_activity.date.strftime("%d %b %Y"),
            "start_time":tilldate_activity.start_time.strftime("%H:%M"),
            "end_time":tilldate_activity.end_time.strftime("%H:%M"),
            "elapsed_time":tilldate_activity.elapsed_time,
            "category_name":tilldate_activity.category_name,
            "category_bar_color":tilldate_activity.category_bar_color,
            "category_group_num":tilldate_activity.category_group_num
        }

    tilldate_activities_dict["tilldate_elapsedtime"] = tilldate_elapsedtime


    return JsonResponse({
        "custom_date_dict":custom_date_activities_dict,
        "daily_dict":daily_activities_dict,
        "week_dict":weekly_activities_dict,
        "month_dict":monthly_activities_dict,
        "tilldate_dict":tilldate_activities_dict
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






