
list_key = dict()
result = ''
error = []

def keyFormat(item):
    if '|' in item:
        m = item.split('|')
        return m[0]
    return item

with open('a.txt','r') as f:
    s = f.readlines()

# s = [
#     'http://www.luobojianzhan.com<@>baidu<@>7bada4670dd46980ee0ed9b3b29e11bd',
#     'http://www.shangyouw.cn<@>51la<@>19392680',
#     'http://www.dngswin10.com<@>cnzz<@>1272901064|z7.cnzz.com',
#     'http://www.dngswin10.com<@>cnzz<@>1272901064|z7.cnzz.com',
#     'http://zzhxjx.com<@>cnzz<@>1000152692|z2.cnzz.com'
# ]

for item in s:
    t = item.split("<@>")
    if len(t) <= 1:
        error.append(t)
        continue
    r = keyFormat(t[-1])
    p = []
    if r in list_key.keys():
        if t[1] == list_key[r]:
            continue
    list_key[r] = t[1]
    result = result + item.rstrip('\n') + '\n'


s = ''
with open('f.txt','w') as f:
    f.write(result)

print('success')
print(error)