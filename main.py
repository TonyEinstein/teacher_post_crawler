# 这是一个示例 Python 脚本。

# 按 Shift+F10 执行或将其替换为您的代码。
# 按 双击 Shift 在所有地方搜索类、文件、工具窗口、操作和设置。
import sys

import requests
from lxml import etree
import pandas as pd
import time


# 获取每个学校的学校名字、入口URL
def get_main_url(url,headers,page_lenght,city_name,areaCode,keyword):
    all_data = []
    for i in range(1,page_lenght+1):
        try:
            page_respones = requests.get(url=url.format(keyword,areaCode,i),headers=headers,timeout=1)
        except Exception as e:
            print("---------------->>>>>>>当前的翻页页数URL无法抓取！链接是：{}".format(url.format(i)))
            print(e)
            continue
        #获取职位链接
        html = etree.HTML(page_respones.text)
        href = html.xpath('//div[@class="job-list-box"]/div[@class="job-item"]//div[@class="content-left-1-left"]/a[@class="left-name"]/@href')
        href = ['https://www.job910.com'+h for h in href]
        print("该页面已经抓取完成：\n",href)
        print("------------抓取职位信息-----------------")
        for hf in href:
            data_dict = {
                '学校名字':None,
                '学校类型':None,
                '学生人数':None,
                '教师人数':None,
                '职位名字':None,
                '薪资':None,
                '地区':'{}'.format(city_name),
                '工作经验要求':None,
                '学历要求':None,
                '岗位类型':None,
                '招聘人数':None,
                '教师类型':None,
                '上课方式':None,
                '到岗时间':None,
                '职位更新时间':None,
                '福利待遇简述':None,
                '工作地点':None,
                '职位链接':None,
                '福利待遇详细':None,
                '职位详情与职责':None,
            }
            try:
                job_response = requests.get(url=hf,headers=headers,timeout=1)
            except Exception as e:
                print("---------------->>>>>>>当前的岗位信息URL无法抓取！链接是：{}".format(hf))
                print(e)
                continue
            #获取职位详细信息
            html_job = etree.HTML(job_response.text)
            #学校名字
            try:
                school_name = html_job.xpath('//*[@id="jobs-page"]//div[@class="companyname"]/a/@title')
                school_name = [x.strip() for x in school_name if x.strip() != '']
                data_dict['学校名字'] = school_name[0]
            except Exception as e:
                pass
                # print(e)
            # 学校类型，教师人数，学生人数
            try:
                school_detail = html_job.xpath('//*[@id="jobs-page"]//div[@class="school-intro"]/p/text()')
                school_detail = [x.strip() for x in school_detail if x.strip() != '']
                data_dict['学校类型'] = school_detail[0][5:]
                data_dict['学生人数'] = school_detail[1][5:]
                data_dict['教师人数'] = school_detail[2][5:]
            except Exception as e:
                pass
                # print(e)
            # 职位名字
            try:
                job_name = html_job.xpath('//*[@id="jobs-page"]//div[@class="job-name"]/h1/@title')[0]
                data_dict['职位名字'] = job_name
            except Exception as e:
                pass
                # print(e)
            # 薪资
            try:
                salary = html_job.xpath('//*[@id="jobs-page"]//div[@class="joblist"]/span/p/text()')
                salary = [x.strip() for x in salary if x.strip() != '']
                data_dict['薪资'] = salary[0]
            except Exception as e:
                pass
            # 地区
            try:
                region = html_job.xpath('//*[@id="jobs-page"]//div[@class="joblist"]/span[2]/text()')
                region = [x.strip() for x in region if x.strip() != '']
                data_dict['地区'] = region[0]
            except Exception as e:
                pass
            # 工作经验要求
            try:
                work_experience = html_job.xpath('//*[@id="jobs-page"]//div[@class="joblist"]/span[3]/text()')
                work_experience = [x.strip() for x in work_experience if x.strip() != '']
                data_dict['工作经验要求'] = work_experience[0]
            except Exception as e:
                pass
            # 学历要求
            try:
                formal_schooling = html_job.xpath('//*[@id="jobs-page"]//div[@class="joblist"]/span[4]/text()')
                formal_schooling = [x.strip() for x in formal_schooling if x.strip() != '']
                data_dict['学历要求'] = formal_schooling[0]
            except Exception as e:
                pass
            #岗位类型
            try:
                job_type = html_job.xpath('//*[@id="jobs-page"]//div[@class="joblist"]/span[5]/text()')
                job_type = [x.strip() for x in job_type if x.strip() != '']
                data_dict['岗位类型'] = job_type[0]
            except Exception as e:
                pass
            # 招聘人数
            try:
                hiring = html_job.xpath('//*[@id="jobs-page"]//div[@class="joblist"]/span[6]/text()')
                hiring = [x.strip() for x in hiring if x.strip() != '']
                data_dict['招聘人数'] = hiring[0]
            except Exception as e:
                pass

            # 教师类型 上课方式
            try:
                typekeys = html_job.xpath('//*[@id="jobs-page"]//div[@class="typekeys"]/p/text()')
                typekeys = [x.strip() for x in typekeys if x.strip() != '']
                data_dict['教师类型'] = typekeys[0]
                data_dict['上课方式'] = typekeys[1]
            except Exception as e:
                pass
                # print(e)
            # 到岗时间
            try:
                worktime = html_job.xpath('//*[@id="jobs-page"]//div[@class="jobs-desc"]//p[@class="worktime"]/text()')
                worktime = [x.strip() for x in worktime if x.strip() != '']
                data_dict['到岗时间'] = worktime[0][5:]
            except Exception as e:
                pass
                # print(e)
            # 职位更新时间
            try:
                publish_time = html_job.xpath('//*[@id="jobs-page"]//p[@class="publish_time"]/text()')
                # publish_time = [x.strip() for x in publish_time if x.strip() != '']
                data_dict['职位更新时间'] = publish_time[0].replace('\n', '').replace('\r', '').replace(' ', '')[3:]
            except Exception as e:
                pass
                # print(e)
            # 福利待遇简述
            try:
                typekeys2 = html_job.xpath('//*[@id="jobs-page"]//div[@class="desc-wrap"]/div[@class="typekeys"]/p/text()')
                typekeys2 = [x.strip() for x in typekeys2 if x.strip() != '']
                data_dict['福利待遇简述'] = ';'.join(typekeys2)
            except Exception as e:
                pass
                # print(e)
            # 工作地点
            try:
                addresdata = html_job.xpath('//*[@id="jobs-page"]//div[@class="desc-wrap contact"]//span[@class="addresdata"]/text()')
                addresdata = [x.strip() for x in addresdata if x.strip() != '']
                data_dict['工作地点'] = addresdata[0]
            except Exception as e:
                pass
                # print(e)
            # 职位链接
            data_dict['职位链接'] = hf
            # 福利待遇详细
            try:
                daiyu = html_job.xpath('//*[@id="jobs-page"]//p[@class="daiyu"]/text()')
                # daiyu = [x.strip() for x in daiyu if x.strip() != '']
                data_dict['福利待遇详细'] = daiyu[0]
            except Exception as e:
                pass
                # print(e)
            # 职位详情与职责
            try:
                zhize = html_job.xpath('//*[@id="jobs-page"]//p[@class="zhize"]/text()')
                data_dict['职位详情与职责'] = zhize[0]
            except Exception as e:
                pass
            print(data_dict)
            all_data.append(data_dict)
    return all_data



"""
dict：
{学校，学校类型，学生人数，教师人数，职位名字，薪资，地区，工作经验要求，学历要求，岗位类型，招聘人数，教师类型，上课方式，
到岗时间，职位更新时间，福利待遇简述，工作地点，职位链接，福利待遇详细，职位详情与职责，应聘流程}
"""
def working(main_url,headers,file_name,page_lenght,city_name,areaCode,keyword):
    all_data = get_main_url(main_url,headers,page_lenght,city_name,areaCode,keyword)
    df = pd.DataFrame(all_data)
    print(df)
    # df.to_csv('data/main_url.csv',index=False,encoding='utf-8')
    df.to_excel(file_name,encoding='utf-8',index=False)

# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
    """
    areaCode=440000广东  430000湖南 450000广西
    companyType=20公办  10名办 30培训机构 40教育服务商 90其他
    pageIndex=2翻页
    """
    main_url = 'https://www.job910.com/job/search?keyword={}&areaCode={}&jobType=102012&pageIndex={}'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'}
    file_name ='data/0510广西小学英语教师招聘职位表.xlsx'
    page_lenght = 1
    keyword = '英语老师'
    areaCode = '450000'
    city_name = '广西'
    working(main_url,headers,file_name,page_lenght,city_name,areaCode,keyword)
