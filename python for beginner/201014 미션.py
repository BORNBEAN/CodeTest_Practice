'''
3일차 미션
(미션1)
    - 화면을 100 밝게 한다. (오버플로 처리)
    - 화면을 100 어둡게 한다. (언더플로 처리)
    - 화면을 반전한다
    - 화면을 흑백 처리한다 (127 기준)
    - 화면을 흑백 처리한다 (평균값 기준)
    - 화면을 흑백 처리한다 (중앙값 기준)

'''

from tkinter import *
from tkinter import messagebox
from tkinter.simpledialog import *
from tkinter.filedialog import *
import os
import math

## 함수 선언부

def malloc(h, w, init=0):
    retMemory = [[init for _ in range(w)] for _ in range(h)]
    return retMemory

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
    window.geometry(str(outH) + 'x' + str(outW))
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
        tmpStr = " "  # 각 한줄씩
        for k in range(outW):
            r = g = b = outImage[i][k]
            # 점마다 줄마다 뒤에 한칸식 띄어야한다 -> 구분될 수 있도록
            tmpStr += '#%02x%02x%02x ' % (r, g, b)
        rgbString += '{' + tmpStr + '} '
    paper.put(rgbString)

    canvas.pack()

### 영상 처리 함수 모음 ###
def equal():  # 동일 영상 알고리즘
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


def addImage():  # 영상 덧셈 알고리즘
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
            if inImage[i][k] > (255 - value):
                outImage[i][k] = 255
            else:
                outImage[i][k] = inImage[i][k] + value
    display()

def subImage(): # 영상 뺄셈 알고리즘
    global window, canvas, paper, inImage, outImage, inH, inW, outH, outW, fileName
    outH = inH
    outW = inW
    outImage = malloc(inH, inW)
    value = askinteger("어둡게 하기", "값 입력 : ", minvalue=1, maxvalue=255)
    for i in range(inH):
        for k in range(inW):
            if (inImage[i][k] - value) < 0:
                outImage[i][k] = 0
            else:
                outImage[i][k] = inImage[i][k] - value
    display()

def revImage(): # 영상 반전 알고리즘
    global window, canvas, paper, inImage, outImage, inH, inW, outH, outW, fileName
    outH = inH
    outW = inW
    outImage = malloc(inH, inW)
    for i in range(inH):
        for k in range(inW):
            outImage[i][k] = 255 - inImage[i][k]
    display()

def bw127Image(): # 127기준으로 흑백처리 알고리즘
    global window, canvas, paper, inImage, outImage, inH, inW, outH, outW, fileName
    outH = inH
    outW = inW
    outImage = malloc(inH, inW)
    for i in range(inH):
        for k in range(inW):
            if inImage[i][k] >= 128:
                outImage[i][k] = 255
            else:
                outImage[i][k] = 0
    display()

def bwAvgImage():  # 평균값 기준으로 흑백처리 알고리즘
    global window, canvas, paper, inImage, outImage, inH, inW, outH, outW, fileName
    outH = inH
    outW = inW
    outImage = malloc(inH, inW)
    # 이차원 배열을 리스트로 만들어서 평균값 구하기
    imageList = []
    for i in range(inH):
        for k in range(inW):
            imageList.append(inImage[i][k])
    avg = sum(imageList) / (inH*inW)
    ###############################
    for i in range(inH):
        for k in range(inW):
            if inImage[i][k] >= avg:
                outImage[i][k] = 255
            else:
                outImage[i][k] = 0
    display()

def bwMidImage():  # 중간값 기준으로 흑백처리 알고리즘
    global window, canvas, paper, inImage, outImage, inH, inW, outH, outW, fileName
    outH = inH
    outW = inW
    outImage = malloc(inH, inW)
    # 이차원 배열을 리스트로 만들어서 중앙값 구하기
    imageList = []
    for i in range(inH):
        for k in range(inW):
            imageList.append(inImage[i][k])
    imageList.sort()
    midIndex = int((inH*inW)/2)
    mid = imageList[midIndex]
    ########################################
    for i in range(inH):
        for k in range(inW):
            if inImage[i][k] >= mid:
                outImage[i][k] = 255
            else:
                outImage[i][k] = 0
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
    window.title('영상처리 Ver0.01')  # window의 title
    window.geometry('500x500')  # 크기지정
    window.resizable(width=False, height=False)  # 크기달라지는거 막기

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
    photoMenu.add_command(label='어둡게 하기', command=subImage)
    photoMenu.add_command(label='반전 하기', command=revImage)
    photoMenu.add_command(label='흑백 처리 (127기준)', command=bw127Image)
    photoMenu.add_command(label='흑백 처리 (평균값 기준)', command=bwAvgImage)
    photoMenu.add_command(label='흑백 처리 (중앙값 기준)', command=bwMidImage)


    window.mainloop()
