# 재귀함수
# 자기자신을 호출

# # 반복문
# for i in range(1, 6):
#     print(i)
#     if i == 5:
#         print("번호 끝")

# count_1 실행 print 1 그담 count_2 완료되고나서 1끝 출력
# # 첫 번째
# def count_1():
#     print(1)
#     count_2()
#     print("1 끝")

# # 두번째
# def count_2():
#     print(2)
#     count_3()
#     print("2 끝")
# # 세번째
# def count_3():
#     print(3)
#     count_4()
#     print("3 끝")
# # 네번째
# def count_4():
#     print(4)
#     count_5()
#     print("4 끝")
# # 다섯번째
# def count_5():
#     print(5)
#     print("5 끝")

# count_1()

# result
# 1
# 2
# 3
# 4
# 5
# 5 끝
# 4 끝
# 3 끝
# 2 끝
# 1 끝

# 하나로 합침
def count(num=1):
    print(num)
    if num == 5:
        print("번호 끝")
    else:
        count(num + 1)
    print(num, "끝")    

count(0)