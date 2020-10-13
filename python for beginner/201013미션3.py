'''
미션3. RAW 파일을 읽어서 inImage 배열에 저장한 후, 원 영상을 10x10 출력한다.

다음처리 결과를 outImage 배열에 저장한 후, 결과 영상을 10x10 출력한다.
- 화면을 100 밝게 한다. (오버플로 처리)
- 화면을 100 어둡게 한다. (언더플로 처리)
- 화면을 반전한다
- 화면을 흑백 처리한다. (127 기준)
- 화면을 흑백 처리한다. (평균값 기준)
- 화면을 흑백 처리한다. (중앙값 기준)
'''

fileName = 'RAW/lotus512.raw'

rfp = open(fileName, 'rb')

ROW=COL=512

inImage = []
inImage = [ [0 for _ in range(COL)] for _ in range(ROW) ]

imageList = []
for i in range(ROW):
    for k in range(COL):
        pixel = int(ord(rfp.read(1)))
        inImage[i][k] = pixel
        imageList.append(inImage[i][k])

rfp.close()

for i in range(10):
    for k in range(10):
        print("%3d " % inImage[i][k], end='')
    print()

print()
# - 화면을 100 밝게 한다. (오버플로 처리)
outImage1 = [ [0 for _ in range(COL)] for _ in range(ROW) ]

for i in range(ROW):
    for k in range(COL):
        if inImage[i][k] >= 155:
            outImage1[i][k] = 255
        else:
            outImage1[i][k] = outImage1[i][k] + 100

for i in range(10):
    for k in range(10):
        print("%3d " % outImage1[i][k], end='')
    print()

print()
# - 화면을 100 어둡게 한다. (언더플로 처리)
outImage2 = [ [0 for _ in range(COL)] for _ in range(ROW) ]

for i in range(ROW):
    for k in range(COL):
        if inImage[i][k] <= 100:
            outImage2[i][k] = 0
        else:
            outImage2[i][k] -= 100

for i in range(10):
    for k in range(10):
        print("%3d " % outImage2[i][k], end='')
    print()

print()
# - 화면을 반전한다
outImage3 = [ [0 for _ in range(COL)] for _ in range(ROW) ]

for i in range(ROW):
    for k in range(COL):
        outImage3[i][k] = 255 - inImage[i][k]

for i in range(10):
    for k in range(10):
        print("%3d " % outImage3[i][k], end='')
    print()

print()
# - 화면을 흑백 처리한다. (127 기준)
outImage4 = [ [0 for _ in range(COL)] for _ in range(ROW) ]

for i in range(ROW):
    for k in range(COL):
        if inImage[i][k] >= 128:
            outImage4[i][k] = 255
        else:
            outImage4[i][k] = 0

for i in range(10):
    for k in range(10):
        print("%3d " % outImage4[i][k], end='')
    print()

print()
# - 화면을 흑백 처리한다. (평균값 기준)
avg = sum(imageList) / (COL*ROW)
outImage5 = [ [0 for _ in range(COL)] for _ in range(ROW) ]

for i in range(ROW):
    for k in range(COL):
        if inImage[i][k] >= avg:
            outImage5[i][k] = 255
        else:
            outImage5[i][k] = 0

for i in range(10):
    for k in range(10):
        print("%3d " % outImage5[i][k], end='')
    print()

print()
# - 화면을 흑백 처리한다. (중앙값 기준)
imageList.sort()
midIndex = int((COL*ROW)/2)
mid = imageList[midIndex]
print(imageList)
print(mid)

outImage6 = [ [0 for _ in range(COL)] for _ in range(ROW) ]

for i in range(ROW):
    for k in range(COL):
        if inImage[i][k] >= mid:
            outImage6[i][k] = 255
        else:
            outImage6[i][k] = 0

for i in range(10):
    for k in range(10):
        print("%3d " % outImage6[i][k], end='')
    print()