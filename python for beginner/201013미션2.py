'''
미션2. RAW 파일을 읽어서 inImage 배열에 저장한 후, 다음을 처리하고 출력한다.

- 픽셀값의 평균은?

- 픽셀값 중 최대/최소 값과 그 행/열의 위치는?

- 픽셀값의 중위수는?
'''

fileName = 'RAW/night512.raw'

rfp = open(fileName, 'rb')

ROW=COL=512

inImage = []
inImage = [ [0 for _ in range(COL)] for _ in range(ROW) ]

for i in range(ROW):
    for k in range(COL):
        pixel = int(ord(rfp.read(1)))
        inImage[i][k] = pixel

rfp.close()

max = [0,0,0]
min = [255,0,0]
imageList = []
for i in range(ROW):
    for k in range(COL):
        imageList.append(inImage[i][k])
        if inImage[i][k] >= max[0]:
            max[0] = inImage[i][k]
            max[1] = i
            max[2] = k
        if inImage[i][k] <= min[0]:
            min[0] = inImage[i][k]
            min[1] = i
            min[2] = k

imageList = list(map(int, imageList))
print(imageList)
avg = sum(imageList) / (COL*ROW)
print(avg)

print("최대값 : "+ str(max[0]) + " 위치 : " + str(max[1]) + "," + str(max[2]))
print("최소값 : "+ str(min[0]) + " 위치 : " + str(min[1]) + "," + str(min[2]))

imageList.sort()
mid = int((COL*ROW)/2)
print(imageList[mid])
