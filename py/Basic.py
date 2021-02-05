num = int(input('type number: '))
pre = 8
print('**:', pre**num)
print('//: ' + str(pre//num))
print('&: ' + str(pre&num))
print('|: ' + str(pre|num))
print('^: ' + str(pre^num))
print('~: ' + str(~num))
print('<<: ' + str(pre<<num))
print('>>: ' + str(pre>>num))
tmp = 123
print(tmp)
tmp = '321'
print(tmp)
a = 'ABC'
b = a
a = 'XYZ'
print(b)
print(ord('A'))
print(chr(66))
print('\u4e2d\u6587')
c = b'ABC'
print(c)
print('def'.encode('utf-8'))
print(b'\xe4\xb8\xad\xe6\x96\x87'.decode('utf-8'))
print(b'\xe4\xb8\xad\xff'.decode('utf-8', errors='ignore'))