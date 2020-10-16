from tkinter import *
from tkinter import messagebox
from tkinter.simpledialog import *
from tkinter.filedialog import *
import os
import math
import pymysql
import tempfile
'''
window에 canvas를 올리고 그 위에 점을 찍을 수 있는 paper를 올린다
'''

## 함수 선언부
# openImage saveImage display -> 공통함수
# equal -> 영상처리 함수

def malloc(h, w, init = 0):
    retMemory = [ [ init for _ in range(w)] for _ in range(h)]
    return retMemory

def openMySQL():
    global window, canvas, paper, inImage, outImage, inH, inW, outH, outW, fileName
    global fileList
    ## DB에서 파일이 목록을 가져오기
    conn = pymysql.connect(host='172.20.18.106', user='root', password='1234', db='image_db', charset='utf8')
    cur = conn.cursor()
    sql = "SELECT i_id, i_fname, i_ext FROM image_table"
    cur.execute(sql)
    fileList = cur.fetchall()
    cur.close()
    conn.close()

    # downLoadFile 은 이곳에서만 쓰이므로 inner function을 사용하면 메모리관리, 코드가독성 모두 좋아진다
    def downLoadFile():
        global window, canvas, paper, inImage, outImage, inH, inW, outH, outW, fileName
        # inner function이라도 global 전역변수는 선언해주어야 한다
        global fileList
        # 리스트박스에서 선택한 정보를 추출
        selectIndex = listbox.curselection()[0]  # 선택이 여러개 된 경우 처음 선택한 것만 다운로드받기 위해 [0]을 써준다
        i_id = fileList[selectIndex][0]  # id접근
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
        fp.write(i_file)  # 파일 저장
        fp.close()
        print(fullPath)

        cur.close()
        conn.close()
        print('Ok~')
        subWindow.destroy()

        # 파일 선택하기
        fileName = fullPath
        # (중요!) 입력영상의 높이, 폭을 알아내기
        fSize = os.path.getsize(fileName)
        inH = inW = int(math.sqrt(fSize))
        # 입력영상의 메모리 할당
        inImage = malloc(inH, inW)
        # 파일 --> 메모리로 로딩 (loading)
        fp = open(fileName, 'rb')
        for i in range(inH):
            for k in range(inW):
                inImage[i][k] = ord(fp.read(1))
        fp.close()
        equal()


    ## 서브 윈도창에 파일 목록 나오게 하기 --> 파일 열기 대화상자와 비슷한 개념
    subWindow = Toplevel(window)
    subWindow.geometry('300x400')
    listbox = Listbox(subWindow, bg='yellow')
    listbox.pack()
    for file in fileList:
        listbox.insert(END, file)
    btnDownLoad = Button(subWindow, text='다운로드', command=downLoadFile)
    btnDownLoad.pack()

import random
import struct
def saveMySQL() :
    global window, canvas, paper,inImage, outImage, inH, inW, outH, outW, fileName
    ## 메모리 --> 임시파일로 저장
    tmp = os.path.basename(fileName)
    tmpFname, tmpExt = tmp.split('.')
    saveFullPath = tempfile.gettempdir() + '/' + tmpFname + '_' \
                   + str(random.randint(100, 999)) +'.' + tmpExt
    fp = open(saveFullPath, 'wb')
    for i in range(0, outH) :
        for k in range(0, outW) :
            fp.write(struct.pack('B', outImage[i][k]))
    fp.close()
    print('save ok..')

    ## 임시파일 --> DB 에 업로드 (이건 했음)
    conn = pymysql.connect(host='172.20.18.106', user='root', password='1234', db='image_db', charset='utf8')
    cur = conn.cursor()

    # 파일명, 확장명 골라내기
    fullName = saveFullPath
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
    print('DB Upload Ok~')


def openImage():
    # 지역변수인지 전역변수인지 알 수 없기 때문에 global을 붙인다
    global window, canvas, paper, inImage, outImage, inH, inW, outH, outW, fileName
    # 파일 선택하기
    fileName = askopenfilename(parent=window, filetypes=(('RAW파일', '*.raw'), ('모든 파일', '*.*')))
    # (중요!) 입력영상의 높이, 폭을 알아내기
    fSize = os.path.getsize(fileName)
    inH = inW = int(math.sqrt(fSize))
    # 입력영상의 메모리 할당
    inImage = malloc(inH, inW)
    # 파일 --> 메모리로 로딩 (loading)
    fp = open(fileName, 'rb')
    for i in range(inH):
        for k in range(inW):
            inImage[i][k] = ord(fp.read(1))
    fp.close()
    equal()

def saveImage():
    pass

def display():
    # 지역변수인지 전역변수인지 알 수 없기 때문에 global을 붙인다
    global window, canvas, paper, inImage, outImage, inH, inW, outH, outW, fileName
    # window 크기조절
    window.geometry (str(outH) + 'x' + str(outW))
    # 2번째부터는 캔버스를 뜯어내고 새로운 캔버스를 장착해야한다
    if canvas != None:
        canvas.destroy()
    # image의 크기에 따라 canvas랑 paper의 크기를 조정해야한다 -> display에서
    # canvas 붙이기
    canvas = Canvas(window, height=outH, width=outW)
    # paper 붙이기 ( paper는 사진이미지 개념이다 )
    paper = PhotoImage(height=outH, width=outW)
    canvas.create_image((outH // 2, outW // 2), image=paper, state='normal')  # paper를 canvas 중앙에 붙일것이므로 /2 이다

    # 화면에 하나씩점을 찍으면 느리니까 메모리에서 찍어서 문자열로 put..?
    # for i in range(outH):
    #     for k in range(outW):
    #         data = outImage[i][k]
    #         paper.put('#%02x%02x%02x' % (data, data, data), (k, i))

    # 개선방향
    rgbString = " "
    for i in range(outH):
        tmpStr = " " # 각 한줄씩
        for k in range(outW):
            r = g = b = outImage[i][k]
            # 점마다 줄마다 뒤에 한칸식 띄어야한다 -> 구분될 수 있도록
            tmpStr += '#%02x%02x%02x ' % (r, g, b)
        rgbString += '{' + tmpStr + '} '
    paper.put(rgbString)

    canvas.pack()

### 영상 처리 함수 모음 ###
def equal(): # 동일 영상 알고리즘
    # 지역변수인지 전역변수인지 알 수 없기 때문에 global을 붙인다
    global window, canvas, paper, inImage, outImage, inH, inW, outH, outW, fileName
    # (중요!) 출력영상의 크기를 결정 --> 알고리즘에 영향
    outH = inH
    outW = inW
    # 출력영상의 메모리 할당
    outImage = malloc(inH, inW)
    ## 진짜 영상처리 알고리즘 ##
    for i in range(inH):
        for k in range(inW):
            outImage[i][k] = inImage[i][k]
    display()

def addImage(): # 영상 덧셈 알고리즘
    # 지역변수인지 전역변수인지 알 수 없기 때문에 global을 붙인다
    global window, canvas, paper, inImage, outImage, inH, inW, outH, outW, fileName
    # (중요!) 출력영상의 크기를 결정 --> 알고리즘에 영향
    outH = inH
    outW = inW
    # 출력영상의 메모리 할당
    outImage = malloc(inH, inW)
    ## 진짜 영상처리 알고리즘 ##
    value = askinteger("밝게하기", "값 입력 : ", minvalue=1, maxvalue=255)
    for i in range(inH):
        for k in range(inW):
            if inImage[i][k] > (255-value):
                outImage[i][k] = 255
            else:
                outImage[i][k] = inImage[i][k] + value
    display()


## 전역 변수부
# 정수형 데이터는 0 으로 나머지는 None으로 초기화 시키는 것이 깔끔하다
# python에서 전역변수는 전역변수라고 따로 명시해주어야 한다
window, canvas, paper = None, None, None
inImage, outImage = [], []
inH, inW, outH, outW = [0] * 4
fileName = ""




## 메인 코드부
if __name__ == '__main__':
    
    # 기본 window 띄우기
    window = Tk()
    window.title('영상처리 Ver0.01')             # window의 title
    window.geometry('500x500')                  # 크기지정
    window.resizable(width=False, height=False) # 크기달라지는거 막기

    # # 이미지를 종이에 찍기
    # fileName = 'RAW/lena.raw'
    # rfp = open(fileName, 'rb')
    # ROW = COL = 256
    #
    # inImage = []
    # inImage = [[0 for _ in range(COL)] for _ in range(ROW)]
    #
    # for i in range(ROW):
    #     for k in range(COL):
    #         pixel = int(ord(rfp.read(1)))
    #         inImage[i][k] = pixel
    #
    # rfp.close()
    #
    # for i in range(ROW):
    #     for k in range(COL):
    #         data = inImage[i][k]
    #         paper.put('#%02x%02x%02x' % (data, data, data), (k, i)) # red, blue, green 이랑 위치 -> raw 이미지는 흑백이므로 rgb가 같다

    mainMenu = Menu(window)
    window.config(menu=mainMenu)

    fileMenu = Menu(mainMenu)
    mainMenu.add_cascade(label='파일', menu=fileMenu)
    fileMenu.add_command(label='열기', command=openImage)
    fileMenu.add_command(label='저장', command=saveImage)
    fileMenu.add_separator()
    fileMenu.add_command(label='종료')

    photoMenu = Menu(mainMenu)
    mainMenu.add_cascade(label='영상처리', menu=photoMenu)
    photoMenu.add_command(label='동일 이미지', command=equal)
    photoMenu.add_command(label='밝게 하기', command=addImage)

    mysqlMenu = Menu(mainMenu)
    mainMenu.add_cascade(label='MySQL연동', menu=mysqlMenu)
    mysqlMenu.add_command(label='DB에서 불러오기', command=openMySQL)
    mysqlMenu.add_command(label='DB에 저장하기', command=saveMySQL)

    window.mainloop()
