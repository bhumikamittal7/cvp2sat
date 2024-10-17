a = [1, -99, 43, -95]
b = [0,1,54, -75]
c = [0,0,1,32]
d = [0,0,0,1]
t = [4, -96, 47, -60]

def sumvec(x,y):
    return [x[i]+y[i] for i in range(len(x))]

def sub(x,y):
    return [x[i]-y[i] for i in range(len(x))]

def inner_product(a,b):
    return sum([a[i]*b[i] for i in range(len(a))])

def mainfunc(x,y, target):
    temp = sumvec(x,y)
    # print(x,y,temp)
    temp2 = sub(temp,target)
    # print(temp2)
    return inner_product(temp2, temp2)

def find_min(lst):
    min = lst[0]
    for i in range(len(lst)):
        if lst[i] < min:
            min = lst[i]
    return min

def make_lst(a,b,c,d,t):
    return [mainfunc(a,b,t), mainfunc(a,c,t), mainfunc(a,d,t), mainfunc(b,c,t), mainfunc(b,d,t), mainfunc(c,d,t)]

print(make_lst(a,b,c,d,t))
print(find_min(make_lst(a,b,c,d,t)))


blah = [[5, 0], [1, -13782], [2, -5342], [6, -428], [-6, 2, 0], [-6, 1, 0], [6, -1, -2, 0], [1, -13782], [3, 4771], [7, -15005], [-7, 3, 0], [-7, 1, 0], [7, -1, -3, 0], [1, -13782], [4, 121], [8, -13851], [-8, 4, 0], [-8, 1, 0], [8, -1, -4, 0], [1, -13782], [9, 5635], [-9, 5, 0], [-9, 1, 0], [9, -1, -5, 0], [2, -5342], [3, 4771], [10, -5263], [-10, 3, 0], [-10, 2, 0], [10, -2, -3, 0], [2, -5342], [4, 121], [11, -5371], [-11, 4, 0], [-11, 2, 0], [11, -2, -4, 0], [2, -5342], [12, -6499], [-12, 5, 0], [-12, 2, 0], [12, -2, -5, 0], [3, 4771], [4, 121], [13, 4956], [-13, 4, 0], [-13, 3, 0], [13, -3, -4, 0], [3, 4771], [14, -14016], [-14, 5, 0], [-14, 3, 0], [14, -3, -5, 0], [4, 121], [15, -15040], [-15, 5, 0], [-15, 4, 0], [15, -4, -5, 0]]

print(len(blah))