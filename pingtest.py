from fake_useragent import UserAgent
from datetime import datetime, timedelta
from time import sleep
import urllib.request

ua = UserAgent()
tURL = ''
req = urllib.request.Request(tURL, headers={"User-Agent": ua.random})
chk = []

st_b = st = datetime.now()
tar_b = tar = datetime.strptime(urllib.request.urlopen(req).headers['Date'], '%a, %d %b %Y %H:%M:%S %Z')
nd_b = nd = datetime.now()
with open("pinglog.txt", "w", encoding='utf-8') as f:
    f.write('Ping target : ' + tURL + '\n')
    f.write(datetime.now().strftime("%Y-%M-%D %H:%M:%S") + '\n')
    f.write('-----<Check mode>-------\n')

while True:
    st = datetime.now()
    tar = datetime.strptime(urllib.request.urlopen(req).headers['Date'], '%a, %d %b %Y %H:%M:%S %Z')
    nd = datetime.now()
    chk.append((nd - st).microseconds)
    with open("pinglog.txt", "a", encoding='utf-8') as f:
        f.write('%d.%d %d %d.%d\n' % (st.second, st.microsecond, tar.second, nd.second, nd.microsecond))
    tar += timedelta(hours=9)  # UTC+9 맞추기
    if (st - st_b).microseconds < 25000 and tar.second != tar_b.second:
        break
    st_b = st
    tar_b = tar
    nd_b = nd

st_b = (tar - st_b).total_seconds()
nd = (tar - nd).total_seconds()
atp = len(chk)
avg_atp = sum(chk) / len(chk) / 1000

print('Attempt No. : %d Avg. Ping : %fms' % (atp, avg_atp))
print('Error : %f ~ %f\n' % (nd, st_b))
with open("pinglog.txt", "a", encoding='utf-8') as f:
    f.write('Attempt No. : %d Avg. Ping : %f\n' % (atp, avg_atp))
    f.write('Error : %f ~ %f\n\n' % (nd, st_b))
    f.write('-----<Accurate mode>-------\n')
ans_int = (st_b < 0) + int(st_b)
st_b -= ans_int

acnt = 0
ans_b = False
while True:
    sleep(2 - st_b - datetime.now().microsecond/1000000)
    t_st_b = datetime.now()
    t_tar_b = datetime.strptime(urllib.request.urlopen(req).headers['Date'], '%a, %d %b %Y %H:%M:%S %Z')
    t_nd_b = datetime.now()
    t_st = datetime.now()
    t_tar = datetime.strptime(urllib.request.urlopen(req).headers['Date'], '%a, %d %b %Y %H:%M:%S %Z')
    t_nd = datetime.now()
    t_tar_b += timedelta(hours=9)  # UTC+9 맞추기
    t_tar += timedelta(hours=9)  # UTC+9 맞추기
    with open("pinglog.txt", "a", encoding='utf-8') as f:
        f.write('%d.%d %d %d.%d\n' % (t_st_b.second, t_st_b.microsecond, t_tar_b.second, t_nd_b.second, t_nd_b.microsecond))
        f.write('%d.%d %d %d.%d\n\n' % (t_st.second, t_st.microsecond, t_tar.second, t_nd.second, t_nd.microsecond))
    # print(t_st_b, t_tar_b, t_nd_b, t_tar, t_nd)
    # print((t_nd_b - t_st_b).total_seconds(), (t_nd - t_st).total_seconds())
    if t_tar_b.second == t_tar.second and (t_nd_b - t_st_b).total_seconds() < 0.032 and (t_nd - t_st).total_seconds() < 0.032 and t_st + timedelta(seconds=ans_int) < t_tar:
        acnt += 1
        print((t_tar_b - t_nd_b).total_seconds())
        if ans_b:
            ans_b = max(ans_b, (t_tar_b - t_nd_b).total_seconds())
        else:
            ans_b = (t_tar_b - t_nd_b).total_seconds()
        if acnt == 10:
            break
st_b += ans_int
ans = (ans_b + st_b) / 2
print('\nFinal Error : %f ~ %f' % (ans_b, st_b))
print('Error %.2fms' % ((st_b - ans_b) * 1000))
print(ans, end='')
with open("pinglog.txt", "a", encoding='utf-8') as f:
    f.write('\nFinal Error : %f ~ %f\n' % (ans_b, st_b))
    f.write('Error %.2fms\n' % ((st_b - ans_b) * 1000))
    f.write('%f' % ans)
