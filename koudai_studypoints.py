# -*- coding:utf-8 -*-
import urllib
import json
import requests
from requests.exceptions import RequestException
import random 
import re
import os
import pathlib
api4_koudaitiku_com_url = "http://api4.koudaitiku.com/"
current_dir = os.getcwd()  #/home/curie/gitcode/koudaitk_get
def get_name_pwd():
    # read userID and pwd from txt
    account = []
    f = open("name_pwd.txt", "r")   # 读取user.txt文件的账户和密码信息
    for user in f:     
        tmp = []                    # 每一行的信息临时列表    
        tmpUser, tmpPassword = user.split(" ", 1)   # 以空格拆分出每一行的用户名和密码，并存入tmpUser和tmpPassword变量中    
        tmp.append(tmpUser.strip())
        tmp.append(tmpPassword.strip())# 把tmp列表存入account列表中    
        account.append(tmp)         # 读取每一行
    f.close()
    name = account[0][0]
    pwd = account[0][1]
    return (name,pwd)

name,pwd = get_name_pwd()
sess = requests.session() # 创建可传递cookies的会话

login_url = "http://api4.koudaitiku.com/login.htm"
koudai_user = "kdtk/4.3.1 (com.yunti.kdtk; build:63 Android 23) okhttp/3.5.0"
ContentType = "application/x-www-form-urlencoded"
Host = "api4.koudaitiku.com"

login_headers_to_send = {
        'User-Agent': koudai_user,
        'Content-Type': ContentType,
        # 'Content-Length': 34,
        'Host': Host ,
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip'
        # Cookie: _kdsess=shjbun6avlukkhpyy5cplxy5qh4lhulaij2srmcbpsvqt2i64gcbtxyne6zdpw44rvnxohj7q
}

def login():
    login_form_data = 'name='+name+'&'+'pwd='+pwd
    l_response = sess.post(url=login_url, headers=login_headers_to_send,data=login_form_data)
    l_r=l_response.text
    # print(l_r)
    return


def get_subject_id():
    subject_url = api4_koudaitiku_com_url+"/member/mistake/subject.htm"
    subject_r = sess.get(url=subject_url, headers=login_headers_to_send)
    # {"id":24076,"name":"组成原理","score":0}
    print(json.dumps(json.loads(subject_r.text),ensure_ascii=False,indent=4))
    # json_save_to_path(subject_r.text, current_dir+"/get_json/subjectId.json")
    return
# subjectId :  政治 2; 英语一 18; 数学一 15; 计算机联考 5

subjects_dict = {'政治': 2, '英语一': 18, '数学一': 15,'计算机联考':5}

def json_save_to_path(text,json_file_path):
    with open(json_file_path, 'w') as f:
        json.dump(json.loads(text), f,ensure_ascii=False,indent=4)
    print("[already saved]:",json_file_path)
    return


def get_mistaked_problems_list_by_id_test(subjectId):
    mistakes_url = api4_koudaitiku_com_url+"/member/mistake/detail.htm"+"?"
    # NOTE! this "?" is very important!
    # 我的错题
    # subjectId :  政治 2; 英语一 18; 数学一 15; 计算机联考 5
    query_json = {'subjectId':subjectId,
    'page':1,
    'pageSize':10000
    }
    get_mistakes_url = mistakes_url + urllib.parse.urlencode(query_json) # "subjectId=2&page=1&pageSize=20"
    mistaked_problems_r = sess.get(url= get_mistakes_url, headers=login_headers_to_send)
    text = json.loads(mistaked_problems_r.text)
    print(json.dumps(text,ensure_ascii=False,indent=4))
    return 

def get_mistaked_problems_list_by_name(subject_name):
    subjectId = subjects_dict[subject_name]
    mistakes_url = api4_koudaitiku_com_url+"/member/mistake/detail.htm"+"?"
    # NOTE! this "?" is very important!
    # 我的错题
    # subjectId :  政治 2; 英语一 18; 数学一 15; 计算机联考 5
    query_json = {'subjectId':subjectId,
    'page':1,
    'pageSize':10000
    }
    get_mistakes_url = mistakes_url + urllib.parse.urlencode(query_json) # "subjectId=2&page=1&pageSize=20"
    mistaked_problems_r = sess.get(url= get_mistakes_url, headers=login_headers_to_send)
    path = current_dir+"/get_json/mistaked_problems_list_by_subject/"
    path_things(path)
    json_save_to_path(mistaked_problems_r.text,current_dir+"/get_json/mistaked_problems_list_by_subject/"+subject_name+".json")
    return 

def get_mistaked_problems_lists_and_save():
# 把各个学科所有错题的id按学科保存下来
    get_mistaked_problems_list_by_name('政治')
    # get_mistaked_problems_list_by_name(英语一)
    get_mistaked_problems_list_by_name('计算机联考')
    return

def test_get_exam_problem_details_by_Id(examId):
# 根据题目的id获取相应题目内容，在本代码文件中目前暂不使用    
    exam_details_url = api4_koudaitiku_com_url + "/examitem/detail.htm"+"?"
    # NOTE! this "?" is very important!
    query_json ={
        'examId': examId # eg.5719
    }

    get_exam_problem_details_by_Id_url = exam_details_url  + urllib.parse.urlencode(query_json)
    exam_details_by_id_r = sess.get(url= get_exam_problem_details_by_Id_url, headers=login_headers_to_send)
    text = json.loads(exam_details_by_id_r.text)
    print(json.dumps(text,ensure_ascii=False,indent=4))
    print(text['data']['description'])#　这里已经好了，没有反斜杠了
    return
def get_exam_problem_details_by_Id(examId):
# 根据题目的id获取相应题目内容，在本代码文件中目前暂不使用    
    exam_details_url = api4_koudaitiku_com_url + "/examitem/detail.htm"+"?"
    # NOTE! this "?" is very important!
    query_json ={
        'examId': examId # eg.5719
    }
    get_exam_problem_details_by_Id_url = exam_details_url  + urllib.parse.urlencode(query_json)
    exam_details_by_id_r = sess.get(url= get_exam_problem_details_by_Id_url, headers=login_headers_to_send)
    return exam_details_by_id_r.text

def get_dict_from_json_file(json_file_path):
    with open(json_file_path, 'r') as f:
        temp_dict = json.loads(f.read())
        # json.dump(json.loads(text), f,ensure_ascii=False,indent=4)
    return temp_dict

def test_problems_info(subject_name):
    data_dict_list = get_dict_from_json_file(current_dir+"/get_json/mistaked_problems_list_by_subject/"+subject_name+".json")['data']
    i = 1
    for data_dict in data_dict_list:
        # 这里的data_dict就是包含错题控制信息的单个东西
        print(str(i).zfill(3),"_",data_dict['name'])
        i += 1
        examItems = data_dict['examItems']
        for it in examItems:
            print(it['id'],end=" ")
            get_exam_problem_details_by_Id(it['id'])
        print("")
    return


def path_things(path):
    pathlib.Path(path).mkdir(parents=True, exist_ok=True) 
    return

def problem_detail_html_save_to_path(problems_detail_json,detail_base_path,int_id):
    # print(problems_detail_json["data"]["description"])
    # print(problems_detail_json["data"]["solveGuide"])
    # 112_政治权利与义务 里　111111.txt有个服务器异常 {"msg": "服务器异常","code": "500"}
    if(problems_detail_json["code"]=="200"):
        with open(detail_base_path+str(int_id)+"_"+"description"+".htm", 'w') as f1:
            f1.write(problems_detail_json["data"]["description"])
        with open(detail_base_path+str(int_id)+"_"+"solveGuide"+".htm", 'w') as f2:
            f2.write(problems_detail_json["data"]["solveGuide"])
    else:
        print(problems_detail_json) # 服务器异常
    # grep -o "\"http.*\"" 5238_description.htm > 题目图片.txt
    return

def save_problems_detail(subject_name):
    path_problems_detail=current_dir+"/problems_detail"
    path_things(path_problems_detail+"/politics")
    path_things(path_problems_detail+"/computer")
    if(subject_name == '政治'):
        path_subject_details = path_problems_detail+"/politics"
    if(subject_name == '计算机联考'):
        path_subject_details = path_problems_detail+"/computer"
    data_dict_list = get_dict_from_json_file(current_dir+"/get_json/mistaked_problems_list_by_subject/"+subject_name+".json")['data']
    # data_dict_list = get_dict_from_json_file(current_dir+"/"+subject_name+".json")['data']
    i = 1
    for data_dict in data_dict_list:
        # 这里的data_dict就是包含错题控制信息的单个东西
        print(str(i).zfill(3)+"_"+data_dict['name'].strip()) # 删除空白字符
        # path_point_name = path_subject_details + "/"+str(i).zfill(3)+"_"+data_dict['name'].strip()+"/"
        path_point_name = path_subject_details + "/"+str(i).zfill(3)+"_"+data_dict['name'].strip().replace("/","_")+"/"
        # I/O 被当成路径了
        path_things(path_point_name)
        i += 1
        examItems = data_dict['examItems']
        for it in examItems:
            print(it['id'],end=" ")
            file_problem_detail = path_point_name+str(it['id'])+".txt"
            problem_detail_text = get_exam_problem_details_by_Id(int(it['id']))
            json_save_to_path(problem_detail_text,file_problem_detail)
            problems_detail_json = json.loads(problem_detail_text)
            problem_detail_html_save_to_path(problems_detail_json,path_point_name,it['id'])
            # 这里把题干和解答都保存为htm页面
            # get_exam_problem_details_by_Id(it['id']) # answerType: 单选0 多选1 综合题4
        print("")
    return

# import pypandoc
def get_studyPoint_by_id(studypoint_id,pname):
    studyPoint_url = api4_koudaitiku_com_url+"/studyPoint/detail.htm"
    studyPoint_r = sess.get(url=studyPoint_url, headers=login_headers_to_send)
    studypointId=int(studypoint_id)
    query_json ={
        'id': studypointId # eg.5719
    }
    get_exam_problem_details_by_Id_url = studyPoint_url  + "?"+urllib.parse.urlencode(query_json)
    exam_details_by_id_r = sess.get(url= get_exam_problem_details_by_Id_url, headers=login_headers_to_send)
    # return exam_details_by_id_r.text
    # print(type(exam_details_by_id_r.text))
    # print(json.dumps(json.loads(exam_details_by_id_r.text),ensure_ascii=False,indent=4))
    points_json = json.loads(exam_details_by_id_r.text)
    # path_things(current_dir+"/"+"studypoints")
    study_points_name_html = current_dir+"/"+"studypoints_html"+"/"+ str(studypoint_id).zfill(5)+"-"+pname.replace("/","-").replace("_","-")+".html"
    # study_points_name_tex = current_dir+"/"+"studypoints_tex"+"/"+ str(studypoint_id).zfill(5)+"-"+pname.replace("/","-").replace("_","-")+".tex"
    path_things(current_dir+"/"+"studypoints_html")
    # path_things(current_dir+"/"+"studypoints_tex")
    with open(study_points_name_html,"w") as f:
        f.write(points_json['data']['content'])
    print(str(points_json['data']['id'])+"-"+points_json['data']['name'])
    # out1 = pypandoc.convert_file(study_points_name_html, 'tex', outputfile = study_points_name_tex, format='html')
    # json_save_to_path(points_json['data'], current_dir+"/"+"studypoints"+"/"+str(studypoint_id).zfill(5)+"-"+pname+".html")
    return

def get_json(url,save_path):
    url_r = sess.get(url=url, headers=login_headers_to_send)
    # {"id":24076,"name":"组成原理","score":0}
    print(json.dumps(json.loads(url_r.text),ensure_ascii=False,indent=4))
    if(save_path!=""):
        json_save_to_path(url_r.text, current_dir+"/"+save_path)
    return url_r.text

def post_url(url,):
    url_r = sess.get(url= url, headers=login_headers_to_send)
    return url_r.text
login()
# get_subject_id()
# subject_points =get_json("http://api4.koudaitiku.com/exam/index.htm","exam_index.json")
# subject_point_dict = get_dict_from_json_file("exam_index.json")
# for s in subject_point_dict['data']['subjects']:
#     print(s['id'],s['name'])
# 604 计算机学科
# 15 数学一
# 18 英语一
# 2 政治
# print(subject_point_dict['data']['subjects'][0]['name'])
# get_studyPoint_id()
# get_json("http://api4.koudaitiku.com/studyPoint/list.htm","")
# get_json("http://api4.koudaitiku.com/v2/channel/list.htm?subjectId=5&pid=306&type=2")
# get_mistaked_problems_lists_and_save() #获得错题们的id

# subject_points_dict = get_dict_from_json_file("计算机联考.json")
# points_list = subject_points_dict['data']
# for p in points_list:
#         get_studyPoint_by_id(p['id'],p['name'])

subject_points_dict = get_dict_from_json_file("政治.json")
points_list = subject_points_dict['data']
for p in points_list:
        get_studyPoint_by_id(p['id'],p['name'].replace("/","-").replace("_","-"))
        # with open(current_dir+"/"+"htmlstudypoints"+"/"+str(p['id']).zfill(5)+"-"+p['name']+".html", 'w') as f1:
        #     f1.write(problems_detail_json["data"]["description"])
#  rename 's/\.html/\.json/' *       

#     print(p['id'],p['name'])

# save_problems_detail('政治')
# save_problems_detail('计算机联考')

   

