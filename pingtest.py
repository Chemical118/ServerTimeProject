from fake_useragent import UserAgent
from datetime import datetime, timedelta
from time import sleep
from random import uniform
import urllib.request

ua = UserAgent()
tURL = ''
req = urllib.request.Request(tURL, headers={"User-Agent": ua.random})
chk = []

st_b = st = datetime.now()
tar_b = tar = datetime.strptime(urllib.request.urlopen(req).headers['Date'], '%a, %d %b %Y %H:%M:%S %Z')
nd_b = nd = datetime.now()
fins = "pinglog/" + "{:%Y_%m_%d_%H_%M_%S}".format(nd) + ".txt"
with open(fins, "w", encoding='utf-8') as f:
    f.write('Ping target : ' + tURL + '\n')
    f.write(nd.strftime("%Y-%M-%D %H:%M:%S") + '\n')
    f.write('\n----<Check mode>-------\n')

while True:
    st = datetime.now()
    tar = datetime.strptime(urllib.request.urlopen(req).headers['Date'], '%a, %d %b %Y %H:%M:%S %Z')
    nd = datetime.now()
    chk.append((nd - st).total_seconds())
    with open(fins, "a", encoding='utf-8') as f:
        f.write('%d.%d %d %d.%d\n' % (st.second, st.microsecond, tar.second, nd.second, nd.microsecond))
    tar += timedelta(hours=9)  # UTC+9 맞추기
    if (st - st_b).total_seconds() < 0.025 and tar.second != tar_b.second:
        break
    st_b = st
    tar_b = tar
    nd_b = nd

st_b = (tar - st_b).total_seconds()
nd = (tar - nd).total_seconds()
atp = len(chk)
avg_atp = sum(chk) / len(chk)

print('Attempt No. : %d Avg. Ping : %fms' % (atp, avg_atp * 1000))
print('Error : %f ~ %f' % (nd, st_b))
with open(fins, "a", encoding='utf-8') as f:
    f.write('Attempt No. : %d Avg. Ping : %f\n' % (atp, avg_atp * 1000))
    f.write('Error : %f ~ %f\n\n' % (nd, st_b))
    f.write('-----<Accurate mode>-------\n')
ans_int = (st_b < 0) + int(st_b)

ans_f = st_b
ans_b = nd
st_b -= ans_int
chk = []
for _ in range(int(input("반복 횟수를 입력하세요 : "))):
    sleep(2 - st_b - datetime.now().microsecond/1000000 + uniform(-1.2 * avg_atp, 0.2 * avg_atp))
    t_st_b = datetime.now()
    t_tar_b = datetime.strptime(urllib.request.urlopen(req).headers['Date'], '%a, %d %b %Y %H:%M:%S %Z')
    t_nd_b = datetime.now()
    t_st = datetime.now()
    t_tar = datetime.strptime(urllib.request.urlopen(req).headers['Date'], '%a, %d %b %Y %H:%M:%S %Z')
    t_nd = datetime.now()
    t_tar_b += timedelta(hours=9)  # UTC+9 맞추기
    t_tar += timedelta(hours=9)  # UTC+9 맞추기
    with open(fins, "a", encoding='utf-8') as f:
        f.write('%d.%d %d %d.%d\n' % (t_st_b.second, t_st_b.microsecond, t_tar_b.second, t_nd_b.second, t_nd_b.microsecond))
        f.write('%d.%d %d %d.%d\n\n' % (t_st.second, t_st.microsecond, t_tar.second, t_nd.second, t_nd.microsecond))
    # print(t_st_b, t_tar_b, t_nd_b, t_tar, t_nd)
    # print((t_nd_b - t_st_b).total_seconds(), (t_nd - t_st).total_seconds())
    chk.append(0)
    if t_st_b + timedelta(seconds=ans_int) > t_tar_b:
        ans_f = min(ans_f, (t_tar_b - t_st_b).total_seconds() + 1)
        chk[-1] += 1
    else:
        ans_b = max(ans_b, (t_tar_b - t_nd_b).total_seconds())
    if t_st + timedelta(seconds=ans_int) > t_tar:
        ans_f = min(ans_f, (t_tar - t_st).total_seconds() + 1)
        chk[-1] += 1
    else:
        ans_b = max(ans_b, (t_tar - t_nd).total_seconds())

ans = (ans_b + ans_f) / 2
print('\nFinal Error : %f ~ %f' % (ans_b, ans_f))
print('Error : %.2fms' % ((ans_f - ans_b) * 1000))
print('Front : %d times, Middle : %d times, Last : %d times' % (chk.count(2), chk.count(1), chk.count(0)))

with open(fins, "a", encoding='utf-8') as f:
    f.write('\nFinal Error : %f ~ %f\n' % (ans_b, ans_f))
    f.write('Error %.2fms\n' % ((ans_f - ans_b) * 1000))
    f.write('%f' % (ans * 1000))
