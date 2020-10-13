'''
미션1. 인터넷에서 적당한 소설이나 시를 텍스트 파일로 저장한 후,

그 파일을 다음과 같이 처리하고 출력한다.

- 행 숫자 세기

- 전체 한글 글자 수 세기

- 전체 특수 문자의 숫자 세기

- 전체 단어 세기 (공백으로 분리된 것을 단어로 취급)

(심화) 가장 많이 나온 글자는? 가장 많이 나온 단어는?
'''

# 행 숫자 세기
fileName = 'you.txt'
rfp = open(fileName, 'r')

count = 0
while True:
    line = rfp.readline()
    if line == None or line == '':
        break
    count = count + 1
print(count)

rfp.close()

# 전체 한글 글자 수 세기
fileName = 'you.txt'
rfp = open(fileName, 'r')

count = 0
while True:
    line = rfp.readline()
    if line == None or line == '':
        break
    for cha in line:
       if 'ㄱ' <= cha <= '힣':
           count += 1
print(count)
rfp.close()

# 전체 특수 문자의 숫자 세기
# ascii code 에서 특수문자는 33~47 / 58~64 / 91~96 / 123~126
fileName = 'you.txt'
rfp = open(fileName, 'r')

count = 0
while True:
    line = rfp.readline()
    if line == None or line == '':
        break
    for cha in line:
       chap = ord(cha)
       if 33<= chap <=47 or 58 <= chap <= 64 or 91 <= chap <= 96 or 123 <= chap <= 126:
           count += 1
print(count)
rfp.close()

# 전체 단어 세기 (공백으로 분리된 것을 단어로 취급)
fileName = 'you.txt'
rfp = open(fileName, 'r')

count = 0
while True:
    line = rfp.readline()
    if line == None or line == '':
        break
    lineList = line.split(" ")
    count = count + len(lineList)
print(count)
rfp.close()

# (심화) 가장 많이 나온 글자는? 가장 많이 나온 단어는?