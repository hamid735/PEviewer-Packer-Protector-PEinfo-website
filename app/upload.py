#-*- coding: utf-8 -*-
import subprocess
import os
import sys
from flask import Flask, render_template, request
from flask import send_file
from werkzeug import secure_filename
app = Flask(__name__)
main='main.html'
pack='pack_protector'
howto='howtouse.html'
total='total.html'
peinfo='peinfo'
peview='peview'
jpg1='1.JPG'
jpg2='2.JPG'
jpg3='3.JPG'
jpg4='4.JPG'
jpg5='5.JPG'

#업로드 HTML 렌더링

@app.route('/')
def main():
    return render_template('main.html',src1=howto)

@app.route('/total')
def total():
    return render_template('total.html',src1=pack,src2=peinfo, src3=peview)

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/howtouse')
def howtouse():
    return render_template('howtouse.html')

@app.route('/peinfo')
def peinfo_e():
    return render_template('peinfo.html')

@app.route('/peview')
def peview_e():
    return render_template('peview.html')

@app.route('/pack_protector', methods = ['GET','POST'])
def render_file():
    return render_template('pack_protector.html')

#파일 업로드 처리
@app.route('/upload', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      global f
      f = request.files['file']
      #저장할 경로 + 파일명
      f.save(secure_filename(f.filename))
      os.system('./viruscheck '+f.filename)
      TXT = open("/root/TorF.txt",'r');
      line = TXT.readline()
      TXT.close()
      if line=='None':
      	return render_template('pack_protector.html')
      else:
	os.system('rm '+f.filename);
	return "Virus detected"
	

@app.route('/pack_download', methods = ['GET', 'POST'])
def pack_download_file():
   if request.method == 'POST':
    try:
        path="/PEviewer-Packer-Protector-PEinfo-website/app/"+f.filename+".7z"
        os.system('upx '+f.filename)
        os.system('7z a '+f.filename+'.7z '+f.filename)
	os.system('rm '+f.filename)
        return send_file(path,as_attachment=True)
    except Exception as e:
	os.system('rm '+f.filename)
        return "Please upload the Windows executable"

@app.route('/unpack_download', methods = ['GET', 'POST'])
def unpack_download_file():
   if request.method == 'POST':
    try:
        path="/PEviewer-Packer-Protector-PEinfo-website/app/"+f.filename+".7z"
        os.system('upx -d '+f.filename)
        os.system('7z a '+f.filename+'.7z '+f.filename)
	os.system('rm '+f.filename)
        return send_file(path,as_attachment=True)
    except Exception as e:
	os.system('rm '+f.filename)
        return "Please upload the packed Windows executable"

if __name__ == '__main__':
    #서버 실행
   app.run(host='0.0.0.0', port=80)

