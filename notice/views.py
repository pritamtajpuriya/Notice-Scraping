
from datetime import datetime
from email.mime import image
from inspect import Parameter
from django.shortcuts import render
from pyBSDate import convert_AD_to_BS, convert_BS_to_AD, addate

from urllib.request import Request, urlopen, urlretrieve
# import beatifulsoup4 as bs4
from bs4 import BeautifulSoup


from rest_framework.views import APIView
from rest_framework.response import Response

from notice.models import Notice
from .serializers import *
from notice.utils import Utils
import requests
import json

import os

from django.core.files import File


def home(request):

    return render(request, 'base.html')


class Getjob(APIView):
    def get(self, request):
        clist = []

        for i in range(264504, 264504+500):

            try:
                dataSearch = {}
                url = "https://srv.dofe.gov.np/Services/DofeWebService.svc/GetPrePermissionByLotNo"
                parameter = {"LotNo": i}
                r = requests.post(url,  json=parameter)
                # j = json.loads(r.text)
                # print(j)
                data = r.json()
                datas = json.loads(r.text)
                print(datas['d'][0]['Country'])
                # if datas['d'][0]['Country'] == 'Japan' is None:
                dataSearch['country'] = datas['d'][0]['Country']
                dataSearch['lotno'] = datas['d'][0]['LotNo']
                dataSearch['Salary'] = datas['d'][0]['Salary']
                dataSearch['SkillName'] = datas['d'][0]['SkillName']

                print(datas['d'][0]['Country'])
                print(datas['d'][0]['LotNo'])
                clist.append(dataSearch)
            except:
                print('error')

        return Response({'data': clist})


class Bsc(APIView):

    def get(self, request):

        print('Fetching notices')
        subCategory = ['notice', 'schedule', 'result']
        data = []
        message = ''

        for cat in subCategory:
            print('Fetching ' + cat)

            try:
                reqURL = Request('https://www.tuiost.edu.np/' +
                                 cat, headers={'User-Agent': 'Mozilla/5.0'})
                html = urlopen(reqURL).read()

                bs = BeautifulSoup(html, 'html.parser')

                notices = bs.find(id="notices").select('.mt-3')

                for notice in notices:

                    da = {}
                    title = notice.find("a").text
                    date = notice.find("small").text

                    datestring = date.replace('st', '').replace(
                        'th', '').replace('rd', '').replace(',', '')
                #   print(datestring)

                    publishDate = datetime.strptime(datestring, '%d %b %Y')
                    # print(publishDate)

                    href = notice.find("a", href=True)
                    da["title"] = title.replace('\n', '')
                    da["date"] = publishDate
                    # da["file"] = href['href']

                    # title = title.replace('\n', '')
                    # date = publishDate
                    # file = href['href']

                    da["belongs"] = 'bsc csit'

                    notice = Notice.objects.filter(title=da["title"])

                    # category = Category.objects.filter(title='center')
                    da["category"] = cat
                    print(da)
                    print(href['href'])

                    if notice:
                        message = 'Notice already exists'

                    else:
                        myobj = Notice(**da)
                        image = urlretrieve(href['href'])
                        obj = Notice.objects.create(**da)

                        fname = os.path.basename(href['href'])

                        obj.file.save(fname, File(open(image, 'rb')))
                        obj.save()

                        message = 'Notice Created'

                    data.append(da)

            except:
                print('error')
                message = 'error'
        return Response({"messsage": message})


class Psc(APIView):

    def get(self, request):
        print('Fetching notices')
        data = {}

        data["vacancy"] = getPscVacancy()

        data["center"] = getPscExamCenter()
        return Response({"messsage": data})


def getPscExamCenter():
    try:
        print('center')

        reqURL = Request('https://psc.gov.np/category/center/all.html',
                         headers={'User-Agent': 'Mozilla/5.0'})
        html = urlopen(reqURL).read()

        bs = BeautifulSoup(html, 'html.parser')

        tablerow = bs.find(id='example').find('tbody').find_all('tr')

        dataa = []
        for row in tablerow:
            notice = {}
            data = []
            td = row.find_all('td')
            for t in td:
                data.append(t.text)

            notice["title"] = data[2].replace(
                '\n', '').replace('\t', '').replace('   ', '')
            # print(notice["title"])
            date = data[4].split(' ')
            notice["date"] = date[0]
            print(notice["date"])
            href = t.find('a', href=True)
            # print(href)
            if href:
                data.append(href['href'])
            notice["file"] = data[6]
            notice["category"] = 'center'
            notice["belongs"] = 'PSC'
            if Notice.objects.filter(title=notice["title"]):
                message = 'Notice already exists'
            else:
                Notice.objects.create(**notice)
                message = 'Notice Created'
            dataa.append(notice)

        # message = 'Notice Created'
        return message
    except:
        print('error')
        message = 'error'
        return message


def getPscVacancy():

    subCategory = ['notice-advertisement']
    message = ''

    for cat in subCategory:
        try:
            reqURL = Request('https://psc.gov.np/category/' + cat +
                             '/all.html', headers={'User-Agent': 'Mozilla/5.0'})
            html = urlopen(reqURL).read()
            bs = BeautifulSoup(html, 'html.parser')

            tablerow = bs.find(id='datatable1').find_all('tr')
            dataa = []
            for table in tablerow:

                notice = {}

                td = table.find_all('td')
                data = []
                for t in td:
                    data.append(t.text)

                    href = t.find('a', href=True)
                    # print(href)
                    if href:
                        data.append(href['href'])

                        # print(href['href'])

                if len(data) > 1:

                    notice["title"] = data[2].replace(
                        '\n', '').replace('\t', '').replace('   ', '')
                    date = Utils.nepaliNumberToEnglish(data[0])
                    d1 = date.split('/' and '-' and '|')
                    if '/' in date:
                        date = date.split('/')
                    if '-' in date:
                        date = date.split('-')
                    if '।' in date:
                        date = date.split('।')

                    # print(date)
                    # ad_date = convert_AD_to_BS(date[0], 0, date[2])
                    # print(ad_date)
                    ad_date = convert_BS_to_AD(
                        int(date[0]), int(date[1]), int(date[2]))

                    notice["date"] = addate(
                        ad_date[0], ad_date[1], ad_date[2])

                    notice["file"] = data[3]
                    notice["category"] = 'vacancy'

                    notice["belongs"] = 'PSC'

                    if Notice.objects.filter(title=notice["title"]):
                        message = 'Notice already exists'
                    else:
                        Notice.objects.create(**notice)
                        message = 'Notice Created'
                dataa.append(notice)

            return message

        except:
            message = 'error'

            return 'error'


class FetchNotice(APIView):

    def get(self, request):
        print('Fetching notices')
        notice = Notice.objects.order_by('-date').all()[0:20]
        serializer = NoticeSerializer(notice, many=True)

        return Response(serializer.data)
