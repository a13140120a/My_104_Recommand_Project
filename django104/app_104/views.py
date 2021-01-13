from django.shortcuts import render, HttpResponse, redirect
from django.http import Http404
import time
from .models import Job
from .model_functions import cv_category_predict, string_clean, jieba_cut,show_recommendation_id,recommendation_id_2_result

# Create your views here.


def back_main_page(request):
    return render(request,"find_job.html")


def submit(request):
    if request.method == "GET":
        return render(request, "find_job.html")
    try:
        posted_data = request.POST
        area = posted_data['area']
        years = posted_data['years']
        edu = posted_data['edu']
        work = posted_data['work']

        work_str_clean = string_clean(work)
        work_cut = jieba_cut(work_str_clean)
        work_cut_join = " ".join(work_cut)
        category = cv_category_predict(work_cut_join)
        job_queryset = Job.objects.filter(jobCat_main=category,
                                          addressRegion=area,
                                          workExp=int(years),
                                          edu__contains=edu
                                          )
        jobs = [job for job in job_queryset]
        top10_recommendation_id = show_recommendation_id(work_cut_join, jobs)  # 計算推薦結果，顯示前10筆推薦
        """
        top10_recommendation_id: [(0.7991363, '71dd9'), (0.77002245, '6kvwp'), (0.76840985, '4d1wo'), (0.7683129, '6xbtq'), (0.74619126, '64vg5'), (0.74272764, '6ct9m'), (0.7402217, '6k5ft'), (0.7
        394142, '71k2j'), (0.73791146, '74udw'), (0.7169924, '6uhsq')]
        左邊是 cosine_similarity, 右邊是 id
        """
        top10_recommendation = recommendation_id_2_result(top10_recommendation_id)
        return render(request,"result.html",locals())
    except ValueError as e:
        print(e)
        return HttpResponse('<font size="50">錯誤</font>')
    except ZeroDivisionError as e:
        print(e)
        return HttpResponse('<font size="50">錯誤</font>')


