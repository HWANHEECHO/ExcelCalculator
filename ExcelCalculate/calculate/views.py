from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd

# Create your views here.
def calculate(request):
    file = request.FILES['fileInput']
    print("# 사용자가 등록한 파일의 이름: ", file)
    df = pd.read_excel(file, sheet_name = "Sheet1", header = 0)
    # print(df.head())

    grade_dic = {}
    total_row_num = len(df.index)
    # print(total_row_num)
    
    for i in range(total_row_num):
        data = df.loc[i]
        if not data.grade in grade_dic.keys():
            grade_dic[data.grade] = [data.value]
        else:
            grade_dic[data.grade].append(data.value)
    # print(grade_dic)

    grade_calculate_dic = {}
    for key in grade_dic.keys():
        grade_calculate_dic[key] = {}
        grade_calculate_dic[key]['grade'] = key
        grade_calculate_dic[key]['min'] = min(grade_dic[key])
        grade_calculate_dic[key]['max'] = max(grade_dic[key])
        grade_calculate_dic[key]['avg'] = float(sum(grade_dic[key])) / len(grade_dic[key])
    # print(grade_calculate_dic)

    grade_list = list(grade_calculate_dic.keys())
    # print(grade_list)
    grade_list.sort()
    # print(grade_list)
    for key in grade_list:
        print("# grade: ", key)
        print("min:", grade_calculate_dic[key]['min'], end="")
        print("/ max:", grade_calculate_dic[key]['max'], end="")
        print("/ avg:", grade_calculate_dic[key]['avg'], end="\n\n")

    email_domain_dic = {}
    for i in range(total_row_num):
        data = df.loc[i,:]
        email_domain = data['email'].split("@")[1]
        if not email_domain in email_domain_dic.keys():
            email_domain_dic[email_domain] = 1
        else:
            email_domain_dic[email_domain] += 1

    print("## Email 도메인별 사용 인원")
    for key in email_domain_dic.keys():
        print("#", key, ": ", email_domain_dic[key], "명")

    """
    df_grouped = df.groupby(['grade'])
    print(df_grouped.value.agg(['min', 'max', 'mean']).rename_axis('grade').reset_index())

    df['domain'] = df.email.str.split('@').str[1]
    df_grouped2 = df.groupby(['domain'])
    print(df_grouped2.value.count().sort_values(ascending = False))

    -------------------------------------------------------------------------------------------------------------------

    grade_df = df.groupby('grade')['value'].agg(["min", "max", "mean"]).reset_index().rename(columns = {"mean" : "avg"})
    print(grade_df)
    print("")
    
    df['domain'] = df['email'].apply(lambda x : x.split("@")[1])
    email_df = df.groupby('domain')['value'].agg("count").sort_values(ascending=False).reset_index()
    print(email_df)
    """

    return HttpResponse("calculate, calculate function!")