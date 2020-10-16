from tkinter import *
from tkinter import messagebox
from tkinter.simpledialog import *
from tkinter.filedialog import *
import pymysql
import os

def selectFile():
    fullPath = askopenfilename(parent=window, filetypes=(('RAW파일', '*.raw'), ('모든 파일', '*.*')))
    entFullPath.delete(0, 'end')
    entFullPath.insert(0, fullPath)

def upLoadFile():
    conn = pymysql.connect(host='172.20.18.106', user='root', password='1234', db='image_db', charset='utf8')
    cur = conn.cursor()

    ''' 쿼리를 할때 sql문을 이런식으로 주석으로 달아놓으면 나중에 따로 안찾아도 된다
    CREATE TABLE image_table (
	i_id INT AUTO_INCREMENT PRIMARY KEY,
	i_fname VARCHAR(256),
	i_ext CHAR(5),
	i_file LONGBLOB );
    '''
    # 파일명, 확장명 골라내기
    fullName = entFullPath.get()
    filename = os.path.basename(fullName)
    i_fname, i_ext = filename.split('.')

    # 파일 Blob 데이터 읽어오기
    fp = open(fullName, 'rb')
    i_file = fp.read()
    fp.close()

    # DB에 Insert
    # i_file을 tuple 데이터와 연결 -> %s와 tuple을 연결시켜야 하기 때문
    sql = "insert into image_table values (NULL, '" + i_fname + "', '"+i_ext + "', %s)"
    tupleData = (i_file,)
    cur.execute(sql, tupleData)

    conn.commit()
    cur.close()
    conn.close()
    print("ok")

def downList():
    global fileList
    conn = pymysql.connect(host='172.20.18.106', user='root', password='1234', db='image_db', charset='utf8')
    cur = conn.cursor()
    sql = "SELECT i_id, i_fname, i_ext FROM image_table"
    cur.execute(sql)
    fileList = cur.fetchall()
    print(fileList)
    for file in fileList:
        filename = file[1]+'.'+file[2]
        listbox.insert(END, filename)

    cur.close()
    conn.close()
    print('Ok~')

import tempfile # temp폴더를 알아내는 패키지

def downLoadFile():
    global fileList
    # 리스트박스에서 선택한 정보를 추출
    selectIndex = listbox.curselection()[0] # 선택이 여러개 된 경우 처음 선택한 것만 다운로드받기 위해 [0]을 써준다
    i_id = fileList[selectIndex][0] # id접근
    i_fname = fileList[selectIndex][1]
    i_ext = fileList[selectIndex][2]

    conn = pymysql.connect(host='172.20.18.106', user='root', password='1234', db='image_db', charset='utf8')
    cur = conn.cursor()
    # 아이디로 파일 덩어리를 선택
    sql = "SELECT i_id, i_file FROM image_table WHERE i_id = " + str(i_id)
    cur.execute(sql)
    # 파일 덩어리를 변수에 저장
    i_id, i_file = cur.fetchone()
    # 파일 저장 위치 알아오기
    # 임시디렉토리 알아오는 메소드 -> tempfile.gettempdir()
    # 임시장소에 저장할 파일명을 지정
    fullPath = tempfile.gettempdir() + '/' + i_fname + '.' + i_ext
    fp = open(fullPath, 'wb')
    fp.write(i_file) # 파일 저장
    fp.close()
    print(fullPath)

    cur.close()
    conn.close()
    print('Ok~')

def selectFolder():
    global folder
    folder = askdirectory(parent=window, initialdir='/' )
    entFullPath.delete(0, 'end')
    entFullPath.insert(0, folder)

def upLoadFolder():
    # 선택한 폴더의 raw 파일 목록을 만들기 (전체경로 포함)
    global folder
    rawList = []
    for dirName, subDirList, fnames in os.walk(folder):
        for fname in fnames:
            # 파일명, 확장명 골라내기
            fullName = os.path.join(dirName, fname)
            try:
                filename = os.path.basename(fullName)
                tmpFname, tmpExt = filename.split('.')
                if tmpExt.lower() == 'raw':
                    rawList.append(fullName)
            except:
                pass
    print(rawList)
    conn = pymysql.connect(host='172.20.18.106', user='root', password='1234', db='image_db', charset='utf8')
    cur = conn.cursor()

    # 파일명, 확장명 골라내기
    for fullName in rawList:
        filename = os.path.basename(fullName)
        i_fname, i_ext = filename.split('.')

        # 파일 Blob 데이터 읽어오기
        fp = open(fullName, 'rb')
        i_file = fp.read()
        fp.close()

        # DB에 Insert
        sql = "INSERT INTO image_table VALUES(NULL, '" + i_fname + "', '" + i_ext + "', %s)"
        tupleData = (i_file,)
        cur.execute(sql, tupleData)

    conn.commit()  # 작업한 것을 저장..
    cur.close()
    conn.close()
    print('Ok~')

## 전역변수부
fileList = []
folder = ''

## 메인 코드부
window = Tk()
window.geometry('600x300')

entFullPath = Entry(window, width=50)
entFullPath.place(x=10, y=18)
btnSelect = Button(window, text='선택', font=('굴림체',15), bg='yellow', command=selectFile)
btnSelect.place(x=370, y=10)
btnUpload = Button(window, text='업로드', font=('굴림체',15), bg='red', command=upLoadFile)
btnUpload.place(x=450, y=10)

# 다운로드할 목록 보기
btnList = Button(window, text='목록보기', font=('굴림체',15), bg='red', command=downList)
btnList.place(x=200, y=60)
listbox = Listbox(window, bg='yellow')
listbox.place(x=30, y=60)
btnDownLoad = Button(window, text='다운로드', font=('굴림체',15), bg='red', command=downLoadFile)
btnDownLoad.place(x=200, y=120)

# 폴더째 업로드
entFolder = Entry(window, width=50)
entFullPath.place(x=10, y=240)
btnFolder = Button(window, text='선택', font=('굴림체',15), bg='green', command=selectFolder)
btnFolder.place(x=370, y=240)
btnFolderUpload = Button(window, text='업로드', font=('굴림체',15), bg='blue', command=upLoadFolder)
btnFolderUpload.place(x=450, y=240)


window.mainloop()