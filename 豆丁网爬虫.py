import pathlib
import requests
import re
import fake_useragent
import threading
from pathlib import Path
import os
import fitz

class Thread_Spdier(threading.Thread):
    def __init__(self,url):
        threading.Thread.__init__(self)
        self.url=url
    def run(self):
        Re_data(resp_data(url))
        getpng(get_Urls())
def resp_data(urls):
    resp = requests.session().get(url=urls)
    resp.headers = {'user-agent': fake_useragent.UserAgent().random}
    return  resp
def Re_data(content):
    global totalpage,title,token,id
    id=re.findall(r'(?<=productId:)\d+',content.text)[0]
    totalpage=re.findall(r'(?<=allPage:)\d+',content.text)[0]
    title=re.findall(r'(?<=productName:").*?(?=")',content.text)[0]
    token=re.findall(r'(?<=flash_param_hzq:").*?(?=")',content.text)[0]
    return id,title,totalpage,token
def get_Urls():
    urls=[]
    for i in range(1,int(totalpage)+1):
        url = 'https://docimg1.docin.com/docinpic.jsp?file={0}&width=1000&sid={1}&pageno={2}&pcimg=1'.format(str(id),str(token),str(i))
        urls.append(url)
    return urls
def getpng(urls):
    dir = r'C:\Users\X\Desktop\新建文件夹\pyimg'
    path= pathlib.Path(dir+'\\'+title)
    doc=fitz.open()
    try:
        path.mkdir()
        for url,i in zip(urls,range(1,int(totalpage)+1)):
            with open(str(path)+'\\'+str(i)+'.png',mode='ab') as f:
                print('正在获取第'+str(i)+'张照片。。。')
                f.write(requests.session().get(url).content)
                imgdoc = fitz.open(f)
                pdfbytes=imgdoc.convertToPDF()
                imgpdf=fitz.open('pdf',pdfbytes)
                doc.insertPDF(imgpdf)
        save_pdf_path = dir+'\\'+title+'\\'+title+'.pdf'
        if os.path.exists(save_pdf_path):
            os.remove(save_pdf_path)
        doc.save(save_pdf_path)
        doc.close()
    except FileNotFoundError as e:
        print(e)
if __name__ == "__main__":
    url = 'https://www.docin.com/p-2196647220.html'
    t1=Thread_Spdier(url=url)
    try:
        t1.start()
        t1.join()
    except:
        print("ERROR")
