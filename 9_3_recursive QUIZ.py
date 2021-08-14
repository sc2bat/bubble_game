# 팩토리얼을 구하는 재귀함수를 작성하시오.
# -팩토리얼 : 주어진 수보다 작거나 같은 모든 양의 정수의 곱
# n! = n * (n - 1) * (n - 2) * ... 1

# ex) 3! = 3 * 2 * 1


# Hint)
# 1) n! = n * (n - 1)! 과 같다
# 2) 4! = 4 * (4 - 1)! 과 같다
# 3) 1!, 0! 은 1 이다.

def factorial(n):
    # pass
    if n > 1:
        return n * factorial(n - 1)
    else:
        return 1

result = factorial(4)
print(result)