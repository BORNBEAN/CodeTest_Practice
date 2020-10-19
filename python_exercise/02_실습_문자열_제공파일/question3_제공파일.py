
def main():
    '''
     아래의 문자열에서 '홀' 과 '짝' 만 출력하라

    string = "홀짝홀짝홀짝"

    출력:
        홀만: 홀홀홀
        짝만: 짝짝짝
    '''
    string = "홀짝홀짝홀짝"

    odd_str = None
    even_str = None
    ####### 구현 시작 ################

    odd_str = string[0::2]
    even_str = string[1::2]

    ########구현 끝 #######################

    print("-------------------------------------------------------------------------------")
    print("홀만: {}".format(odd_str))
    print("짝만: {}".format(even_str))
    print("-------------------------------------------------------------------------------")


# # 메인 함수 호출 ##
if __name__ == "__main__":
    main()
