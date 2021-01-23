class BinOp:
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right
    def __repr__(self):
        return f"BinOp({self.left}, {self.right},{self.op})"
    
def BinOp_f(source): #создаем биноп для рисовки дерева
    key = False
    j = -1
    operation = ['+','-','*','/','^']
    while not key:
        j += 1
        for i in operation:
            if source[j] == i:
                key = True
                break
    op = source[j]
    num1 = source[j-2]
    num2 = source[j-1]
    del source[j], source[j-1], source[j-2]
    source.insert(j-2, BinOp(op, num1, num2))
    return source

def coordinate(source, renderpipe, x, y): #каждому элементу даем определенную координату
    size = diff(source)
    if isinstance(source, BinOp):
        renderpipe.append([source.op, x, y])
        for shift in range(1,size+1):
            renderpipe.append(['/', x-shift, y-shift])
            renderpipe.append(['\\', x+shift, y-shift])
        coordinate(source.left, renderpipe, x-size-1, y-size-1)
        coordinate(source.right, renderpipe, x+size+1, y-size-1)                   
    else:
        renderpipe.append([source, x - len(source) + 1, y])

def diff(source): #количество/длина палочек
    if isinstance(source, BinOp):
        return min(diff(source.left),diff(source.right))*2
    else:
        if len(source) == 1:
            return 1
    return len(source) // 2

def render(renderpipe): #рисуем
    max = -1
    shift_s = []
    high = abs(renderpipe[len(renderpipe)-1][2])
    for i in renderpipe:
        if abs(i[1]) > abs(max):
            max = abs(i[1])
    for i in renderpipe:
        i[1] += max + 1
    for j in range(high+1):
        shift = 0
        lenth = 0
        for i in renderpipe:
            if abs(i[2]) == j:
                print(' '*(i[1] - shift- lenth), end='')
                print(i[0], end='')
                shift = i[1]
                lenth = len(i[0])
        print()

def sort(renderpipe): #сортировка по |y|
    return sorted(renderpipe, key=lambda i: abs(i[2]))

def calc(output): #вычисление результата
    key = False
    j = -1
    operation = ['+','-','*','/','^']
    while not key:
        j += 1
        for i in operation:
            if output[j] == i:
                key = True
                break
    num1 = float(output[j-2])
    num2 = float(output[j-1])
    if output[j] == '+':
        temp = num1 + num2
    if output[j] == '-':
        temp = num1 - num2
    if output[j] == '*':
        temp = num1 * num2
    if output[j] == '/':
        temp = num1 / num2
    if output[j] == '^':
        temp = num1 ** num2
    del output[j], output[j-1], output[j-2]
    output.insert(j-2,temp)
    return output

fun = input()
argu = input()
output = []
stack = []


print("Alisher is a good man!")
key = True
for i in fun: #выводим обратную польскую нотацию
    last = len(stack)-1
    if i.isdigit() or i == 'x':
        if key:
            output.append(i)
            key = False
        else:
            output[len(output)-1] += i
    else:
        key = True
        if i == '(':
            stack.append(i)
        elif i == ')':
            j = len(stack)-1
            while stack[j] != '(':
                output.append(stack.pop())
                j -= 1
            else:
                stack.pop()
        elif stack == []:
            stack.append(i)
        else:
            while last >= 0 and op[stack[last]] >= op[i]:
                output.append(stack.pop())
                last = len(stack)-1
            stack.append(i)

for i in range(len(stack)): 
    output.append(stack.pop())
for i in output:
    if i != '(':
        print(i, end=' ')
print()

source = output.copy()
while len(source) != 1:
    BinOp_f(source)

renderpipe = []
x, y = 0,0
coordinate(source[0], renderpipe, x, y)

render(sort(renderpipe))
for i in range(len(output)):
    if output[i] == 'x':
        output[i] = argu
while len(output) != 1:
    calc(output)
print(output)
        
        

