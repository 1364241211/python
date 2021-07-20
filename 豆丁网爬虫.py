import pathlib
import requests
import re
import fake_useragent
import threading
from pathlib import Path
import os
import fitz

#创建线程对象继承threading.Thread
class Thread_Spdier(threading.Thread):
    #构造函数 url = 需要下载的网址
    def __init__(self,url):
        threading.Thread.__init__(self)
        self.url=url
    #调用start()方法时执行的方法
    def run(self):
        Re_data(resp_data(url))
        getpng(get_Urls())
#获取网址内容
def resp_data(urls):
    resp = requests.session().get(url=urls)
    #请求头
    resp.headers = {'user-agent': fake_useragent.UserAgent().random}
    return  resp
#获取需要的信息：包括id,totalpage,title,token等信息，用于构造请求网址
def Re_data(content):
    global totalpage,title,token,id
    id=re.findall(r'(?<=productId:)\d+',content.text)[0]
    totalpage=re.findall(r'(?<=allPage:)\d+',content.text)[0]
    title=re.findall(r'(?<=productName:").*?(?=")',content.text)[0]
    token=re.findall(r'(?<=flash_param_hzq:").*?(?=")',content.text)[0]
    return id,title,totalpage,token
#构造网址
def get_Urls():
    urls=[]
    for i in range(1,int(totalpage)+1):
        url = 'https://docimg1.docin.com/docinpic.jsp?file={0}&width=1000&sid={1}&pageno={2}&pcimg=1'.format(str(id),str(token),str(i))
        urls.append(url)
    return urls
#下载图片并转存为pdf文件
def getpng(urls):
    dir = r'C:\Users\X\Desktop\新建文件夹\pyimg'
    #构造文件保存文件夹
    path= pathlib.Path(dir+'\\'+title)
    doc=fitz.open()
    try:
        #创建文件夹，如果文件夹存在就删除文件夹
        if path.exists():
            os.remove(path)
        path.mkdir()
        for url,i in zip(urls,range(1,int(totalpage)+1)):
            with open(str(path)+'\\'+str(i)+'.png',mode='ab') as f:
                print('正在获取第'+str(i)+'张照片。。。')
                f.write(requests.session().get(url).content)
                #打开图片
                imgdoc = fitz.open(f)
                #将图片转为pdf
                pdfbytes=imgdoc.convertToPDF()
                #打开pdf文件
                imgpdf=fitz.open('pdf',pdfbytes)
                #将pdf文件添加到文档中
                doc.insertPDF(imgpdf)
        #创建pdf保存位置
        save_pdf_path = dir+'\\'+title+'\\'+title+'.pdf'
        #如果文件已存在则删除
        if os.path.exists(save_pdf_path):
            os.remove(save_pdf_path)
        #将文件保存
        doc.save(save_pdf_path)
        #关闭文件
        doc.close()
    except FileNotFoundError as e:
        print(e)
if __name__ == "__main__":
    url = input('请输入要下载的网址（豆丁网）：')
    #创建线程对象
    t1=Thread_Spdier(url=url)
    try:
        #启动线程
        t1.start()
        #将线程加入主线程
        t1.join()
    except:
        print("ERROR")
