def qsort(array, left, right):
    middle = (left + right) // 2
    p = array[middle]
    i, j = left, right
    while i <= j:
        while array[i] < p:
            i += 1
        while array[j] > p:
            j -= 1
        if i <= j:
            array[i], array[j] = array[j], array[i]
            i += 1
            j -= 1
    if j > left:
        qsort(array, left, j)
    if right > i:
        qsort(array, i, right)

def search(array, element, left, right):
    if left > right:
        return False
    middle = (right + left) // 2
    if (array[middle] < element) and (array[middle+1] >= element):
        return middle
    elif element <= array[middle]:
        return search(array, element, left, middle - 1)
    else:
        return search(array, element, middle + 1, right)

L = list(map(int, input('Введите список чисел через пробел:\n').split()))
num = int(input('Введите число:\n'))
position = None

print('До сортировки:\n', L)
qsort(L, 0, len(L)-1)
print('После сортировки:\n', L)

if (num <= L[0]) or (num > L[len(L)-1]):
    print('Искомый элемент в списке не найден')
else:
    position = search(L, num, 0, len(L)-1)
    if position:
        print('Искомый элемент находится под номером', position+1, '\n' 'Его значение равно', L[position])
    else:
        print('Искомый элемент в списке не найден')
