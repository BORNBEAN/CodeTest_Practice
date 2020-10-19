
def main():
    '''
       사용자로부터 값을 입력받은 후 해당 값에 +20을 더한 값을 출력하라.
        단 값의 범위는 0~255로 가정한다. 255를 초과하는 경우 255를 출력해야 한다.

        >>  입력값: 200
        	출력값: 220
	    >>  입력값: 240
	        출력값: 255
    '''
    
    s = input("입력:")
    ####### 구현 시작 ################

    s = int(s)
    if s >= 235:
        s = 255
    else:
        s += 20

    ########구현 끝 #######################

    print("-------------------------------------------------------------------------------")
    print("출력값: ", s)
    print("-------------------------------------------------------------------------------")


# # 메인 함수 호출 ##
if __name__ == "__main__":
    main()
