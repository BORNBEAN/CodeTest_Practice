'''
3일차 미션
(미션1)
    - 화면을 100 밝게 한다. (오버플로 처리)
    - 화면을 100 어둡게 한다. (언더플로 처리)
    - 화면을 반전한다
    - 화면을 흑백 처리한다 (127 기준)
    - 화면을 흑백 처리한다 (평균값 기준)
    - 화면을 흑백 처리한다 (중앙값 기준)

(미션2-심화)
    - 영상 미러링
    - 영상 90도 회전
    - 영상 이동 --> x와 y를 입력한 값만큼 이동
    - 영상 축소 --> 입력을 2, 4, 8 ...
    - 영상 확대 --> 입력을 2, 4 까지만 ~~ 권장 : 256 또는 128 짜리를 열어서 테스트
    - 영상 입력한 각도로 회전
'''

from tkinter import *
from tkinter import messagebox
from tkinter.simpledialog import *
from tkinter.filedialog import *
import os
import math
from PIL import Image

## 함수 선언부

def malloc(h, w, init=0):
    retMemory = [[init for _ in range(w)] for _ in range(h)]
    return retMemory

def openImage():
    # 지역변수인지 전역변수인지 알 수 없기 때문에 global을 붙인다
    global window, canvas, paper, inImage, outImage, inH, inW, outH, outW, fileName
    # 파일 선택하기
    fileName = askopenfilename(parent=window, filetypes=(('칼라파일', '*.png;*.jpg;*.bmp;*.tif'), ('모든 파일', '*.*')))
    ## Pillow를 통해서 읽어오기. (그림의 pic)
    photo = Image.open(fileName)
    # (중요!) 입력영상의 높이, 폭을 알아내기
    inH = photo.height
    inW = photo.width
    # 입력영상의 메모리 할당
    inImage=[]
    for _ in range(3):
        inImage.append(malloc(inH, inW))

    # PILLOW의 도움으로 각 점의 r,g,b 값을 알아내서 메모리에 넣기
    photoRGB = photo.convert('RGB')
    for i in range(inH):
        for k in range(inW):
            r, g, b = photoRGB.getpixel((k, i))
            inImage[0][i][k] = r
            inImage[1][i][k] = g
            inImage[2][i][k] = b

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
            r = outImage[0][i][k]
            g = outImage[1][i][k]
            b = outImage[2][i][k]
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
    outImage = []
    for _ in range(3):
        outImage.append(malloc(outH, outW))
    ## 진짜 영상처리 알고리즘 ##
    for rgb in range(3):
        for i in range(inH):
            for k in range(inW):
                outImage[rgb][i][k] = inImage[rgb][i][k]
    display()


def addImage():  # 영상 덧셈 알고리즘
    # 지역변수인지 전역변수인지 알 수 없기 때문에 global을 붙인다
    global window, canvas, paper, inImage, outImage, inH, inW, outH, outW, fileName
    # (중요!) 출력영상의 크기를 결정 --> 알고리즘에 영향
    outH = inH
    outW = inW
    # 출력영상의 메모리 할당
    outImage = []
    for _ in range(3):
        outImage.append(malloc(outH, outW))
    ## 진짜 영상처리 알고리즘 ##
    value = askinteger("밝게하기", "값 입력 : ", minvalue=1, maxvalue=255)
    for rgb in range(3):
        for i in range(inH):
            for k in range(inW):
                if inImage[rgb][i][k] > (255 - value):
                    outImage[rgb][i][k] = 255
                else:
                    outImage[rgb][i][k] = inImage[rgb][i][k] + value
    display()

def subImage(): # 영상 뺄셈 알고리즘
    global window, canvas, paper, inImage, outImage, inH, inW, outH, outW, fileName
    outH = inH
    outW = inW
    outImage = []
    for _ in range(3):
        outImage.append(malloc(outH, outW))
    value = askinteger("어둡게 하기", "값 입력 : ", minvalue=1, maxvalue=255)
    for rgb in range(3):
        for i in range(inH):
            for k in range(inW):
                if (inImage[rgb][i][k] - value) < 0:
                    outImage[rgb][i][k] = 0
                else:
                    outImage[rgb][i][k] = inImage[rgb][i][k] - value
    display()

def greyImage() : # 회색 변환 알고리즘
    global window, canvas, paper, inImage, outImage, inH, inW, outH, outW, fileName
    outH = inH
    outW = inW
    for _ in range(3):
        outImage.append(malloc(outH, outW))
    for i in range(inH):
        for k in range(inW):
            sum = 0
            for p in range(3):
                sum += inImage[p][i][k]
            avg = int(sum / 3)
            for p in range(3):
                outImage[p][i][k] = avg
    display()


def revImage(): # 영상 반전 알고리즘
    global window, canvas, paper, inImage, outImage, inH, inW, outH, outW, fileName
    outH = inH
    outW = inW
    for _ in range(3):
        outImage.append(malloc(outH, outW))
    for rgb in range(3):
        for i in range(inH):
            for k in range(inW):
                outImage[rgb][i][k] = 255 - inImage[rgb][i][k]
    display()

def bw127Image(): # 127기준으로 흑백처리 알고리즘
    global window, canvas, paper, inImage, outImage, inH, inW, outH, outW, fileName
    outH = inH
    outW = inW
    for _ in range(3):
        outImage.append(malloc(outH, outW))
    for i in range(inH):
        for k in range(inW):
            sum = 0
            for p in range(3):
                sum += inImage[p][i][k]
            avg = int(sum / 3)
            for p in range(3):
                if avg >= 128:
                    outImage[p][i][k] = 255
                else:
                    outImage[p][i][k] = 0
    display()

def bwAvgImage():  # 평균값 기준으로 흑백처리 알고리즘
    global window, canvas, paper, inImage, outImage, inH, inW, outH, outW, fileName
    outH = inH
    outW = inW
    outImage = malloc(outH, outW)
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
    outImage = malloc(outH, outW)
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


def mirImage():  # 영상 미러링 알고리즘
    # 중간값 기준으로 위아래 바꾸기
    pass


def rot90Image():  # 영상 90도 회전 알고리즘
    #
    pass


def movImage():  # 영상 이동 알고리즘
    pass


def smaImage():  # 영상 축소 알고리즘
    global window, canvas, paper, inImage, outImage, inH, inW, outH, outW, fileName
    # 축소배율 입력받기
    scale = askinteger("축소", "축소 배율 : ")
    # //은 소수점 버리고 몫만 구하는 연산
    outH = inH // scale
    outW = inW // scale
    outImage = malloc(outH, outW)
    for i in range(inH):
        for k in range(inW):
            outImage[i//scale][k//scale] = inImage[i][k]
    display()


def larImage():  # 영상 확대 알고리즘
    global window, canvas, paper, inImage, outImage, inH, inW, outH, outW, fileName
    # 확대배율 입력받기
    scale = askinteger("확대", "확대 배율 : ")
    # //은 소수점 버리고 몫만 구하는 연산
    outH = inH * scale
    outW = inW * scale
    outImage = malloc(outH, outW)
    # 해당알고리즘에서 한칸으로 여러칸을 채우는 알고리즘은 복잡하니까 반대로 큰데에서 작은데에 있는 무엇을 가져올지를 선택하는 방법 -> 백워딩
    for i in range(outH):
        for k in range(outW):
            outImage[i][k] = inImage[i//scale][k//scale]
    display()


def rotateSelImage():  # 영상 입력한 각도로 회전 알고리즘
    pass


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
    photoMenu.add_command(label='회색 변환', command=greyImage)
    photoMenu.add_command(label='흑백 처리 (127기준)', command=bw127Image)
    photoMenu.add_command(label='흑백 처리 (평균값 기준)', command=bwAvgImage)
    photoMenu.add_command(label='흑백 처리 (중앙값 기준)', command=bwMidImage)

    editMenu = Menu(mainMenu)
    mainMenu.add_cascade(label='추가', menu=editMenu)
    editMenu.add_command(label='영상 미러링', command=mirImage)
    editMenu.add_command(label='영상 90도 회전', command=rot90Image)
    editMenu.add_command(label='영상 이동', command=movImage)
    editMenu.add_command(label='영상 축소', command=smaImage)
    editMenu.add_command(label='영상 확대', command=larImage)
    editMenu.add_command(label='영상 입력한 각도로 회전', command=rotateSelImage)

    window.mainloop()
