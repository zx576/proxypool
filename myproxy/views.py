from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from django.core.serializers.json import DjangoJSONEncoder

import logging
import json
import datetime
import requests


from .models import Proxy

from .VerifyProxy import  verify
from .SortDt import sort
from .fetch import crwal

# 日志
logger = logging.getLogger(__name__)



# ===========首页==========================================================
def index(request):
    items = Proxy.objects.filter(status='V').order_by('-created_time')[:100]

    contents = {
        'items':items,
    }
    return render(request,'myproxy/index.html',contents)


# ===============管理页====================================================

def manage(request):
    return render(request,'myproxy/new_index.html')

# ===========手动工作 ======================================================
TASKS = [crwal,sort,verify]
def work(request):
    if request.method == 'GET':
        # processes = []
        # for i in TASKS:
        #     p = multiprocessing.Process(target=i)
        #     processes.append(i)
        #
        # for process in processes:
        #     process.start()
        crwal()
        sort()
        verify()

        return JsonResponse({'data':'all works done'})


# ===========提取 IP ======================================================

# 限定每次最多可取 100 个 IP
MAX_REQUIRED_NUM = 100
# VERIFY_STATUS = False

def get(request):
    '''返回 JSON 格式的IP数据
    num - 请求的 ip 数量，
        如果不为数字，返回错误信息 'require a integer'
        如果大于限定的最大数量，则取最大的数
        如果请求的数量大于数据库中总数量，返回数据库所有 ip， 并在 status 中标明 'not enough'

    v - 是否进行验证，默认不进行验证
        如果 v=True 则返回验证过后的 ip，为空或其他则不进行验证

    v_num - times passed verifing

    type - ip type 'O' stands for 其他 ,'G' for 高匿,'T' for 透明

    head - http-head, offer two choices
            head = http or head = https

    location - where these ips' location

    '''
    global VERIFY_STATUS
    if request.method == 'GET':
        valid_ip = Proxy.objects.filter(status='V')
        num = request.GET.get('num',None)
        if num :
            try:
                num = int(num)
                if num > MAX_REQUIRED_NUM:
                    num = MAX_REQUIRED_NUM
            except:
                error = {'error':'require a integer'}
                return JsonResponse(error)
        else:
            error = {'error': 'require a parameter num '}
            return JsonResponse(error)

        v_num = request.GET.get('v_num',None)
        if v_num:
            try:
                v_num = int(v_num)
                valid_ip = valid_ip.filter(Validated_time__gte=v_num)
            except:
                pass
        else:
            pass
        type = request.GET.get('type',None)
        if type and type.upper() in ['O','G','T']:
            # type = type
            # print(type)
            valid_ip = valid_ip.filter(type__iexact=type)
        else:
            pass

        location = request.GET.get('loc',None)
        if location:
            valid_ip = valid_ip.filter(district__contains = location)

        head = request.GET.get('head',None)
        if head and head.lower() in ['http','https']:
            head = head
            valid_ip = valid_ip.filter(head__contains=head)
        else:
            head = 'http'

        v = request.GET.get('v',None)
        if v and v.lower() == 'true':
            v = True
        else:
            v = None

        data = {}
        ip_list = []
        count = 0

        for i in valid_ip:
            if count == num:
                break
            if not i.ip:
                continue
            proxy = {}
            proxy[head] = i.ip + ':' + i.port
            if v and not verify_ip(proxy):
                # print('verifing')
                continue
            count += 1
            ip_list.append(proxy)
        data['proxies'] = ip_list
        return JsonResponse(data)

def verify_ip(dic):
    '''
    :param dic: 字典形式的 IP
    :return: 如果请求成功则返回 True, 反之 False
    '''
    fixed_url = 'http://www.baidu.com/'
    try:
        res = requests.get(fixed_url, proxies=dic, timeout=1)
        assert res.status_code == 200
        return True
    except:
        return False


# ================查看数据库结果=============================================
def chart(request):
    if request.method == 'GET':
        all_proxies = Proxy.objects.all()

        valid_proxies = all_proxies.filter(status='V')
        invalid_proxies = all_proxies.filter(status='I')

        ip181_proxies = valid_proxies.filter(resourse='IP181')
        xici_proxies = valid_proxies.filter(resourse='西刺')
        sixsix_proxies = valid_proxies.filter(resourse='66代理')
        kuai_proxies = valid_proxies.filter(resourse='快代理')

        #=========ip 状态 饼图 ==============
        status = {}

        count_valid = len(valid_proxies)
        count_invalid = len(invalid_proxies)

        status['legend_data'] = ['有效','无效']
        status['series_data'] = [
            {'name':'有效','value':count_valid},
            {'name':'无效','value':count_invalid}
        ]
        status['title_text'] = '数据库内 IP 状态'
        status['title_subtext'] = '截止到 %s'%datetime.date.today()

        status['series_name'] = 'IP 状态'

        status = json.dumps(status,cls=DjangoJSONEncoder)
        #=======================

        #========= 来源 饼图  ===================

        source = {}

        count_ip181 = len(ip181_proxies)
        count_xici = len(xici_proxies)
        count_sixsix = len(sixsix_proxies)
        count_kuai = len(kuai_proxies)

        source['title_text'] = '来源库存'
        source['series_name'] = 'IP 来源'
        source['legend_data'] = ['西刺代理','IP181代理','66代理','快代理']
        source['series_data'] = [
            {'name':'西刺代理','value':count_xici},
            {'name':'IP181代理','value':count_ip181},
            {'name':'66代理','value':count_sixsix},
            {'name':'快代理','value':count_kuai}
        ]

        source = json.dumps(source,cls=DjangoJSONEncoder)
        # ========================================

        content = {
            'status':status,
            'source':source
        }

        return render(request,'myproxy/chart.html',content)


# ============================已=============================================
# =============================弃============================================
# ===============================用==========================================


''' 

def sort(requests):
    对已存入数据做整理，根据传入的参数做相应的去重/删除无效IP 等操作

    :param requests:
    :return:
    
    if requests.method == 'GET':
        print(requests)
        deduplication = requests.GET.get('dd',None)
        delete = requests.GET.get('di',None)

        count_di,count_dd = 0,0

        if deduplication:
            print('正在去重')
            count_dd = deduplicate()
            print('去重结束')
            logging.info('时间：%r,本次去重 %d 条'%(datetime.datetime.now(),count_dd))

        if delete:
            print('正在删除无效')
            count_di = delete_invalid()
            print('删除结束')
            logging.info('时间：%r,本次删除 %d 条' % (datetime.datetime.now(), count_di))

        return HttpResponse('去重 %d 条，删除无效ip %d 条'%(count_dd,count_di))



def deduplicate():
    all_ip = Proxy.objects.filter(status='V')
    list_ip = []
    count = 0
    for ip in all_ip:
        if ip.addr in list_ip:
            count += 1
            ip.delete()
        list_ip.append(ip.addr)

    return count


def delete_invalid():
    invalid_ip = Proxy.objects.filter(status='I')
    count = len(invalid_ip)
    invalid_ip.delete()
    return count


# ===========爬取 IP 事件 ================================================================

SCHEDUAL_STATUS = True
TIME_DELTA = 1

def work(request):
    验证并爬取 IP

    timedelta 为验证爬取间隔时间，默认为 1 小时
    
    global SCHEDUAL_STATUS
    if request.method == 'GET':
        logging.info(request)
        try:
            timedelta = request.GET.get('timedelta')
            timedelta = int(timedelta)
        except:
            timedelta = TIME_DELTA

        schedule.every(timedelta).hours.do(download_ip)

        schedule.run_all()
        while True:
            if not SCHEDUAL_STATUS:
                schedule.clear()
                SCHEDUAL_STATUS = True
                return JsonResponse({'info':'finished post'})
            schedule.run_pending()


def stop_crwal(request):
    global SCHEDUAL_STATUS
    if request.method == 'GET':
        SCHEDUAL_STATUS = False
        return JsonResponse({'info': 'finished get'})


@register.filter
def get_value(dumped_dict,key):
    content = re.sub('\'', '\"', dumped_dict)
    dic = json.loads(content)
    full_addr = list(dic.values())[0].split(':')
    if len(full_addr) == 2:
        addr = full_addr[0]
        port = full_addr[1]
    elif len(full_addr) == 3:
        addr = full_addr[1][2:]
        port = full_addr[2]
    else:
        return None
    addr_type = list(dic.keys())[0]
    if key == 'type':
        return addr_type
    elif key == 'port':
        return port
    elif key == 'addr':
        return addr

@register.filter
def get_addr(dumped_dict):
    content = re.sub('\'', '\"', dumped_dict)
    dic = json.loads(content)



# ====================清除错误 ip ====================

def clear(request):
    if request.method == 'GET':
        all_addr = Proxy.objects.all()

        for addr in all_addr:
            if addr.ip:
                continue
            else:
                addr.delete()

        return HttpResponse('clear')
        
        
# ============登陆 注册===============================================================

def login_(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username,password=password)
        if user and user.is_active:
            login(request,user)
            if request.GET.get('next'):
                return redirect(request.GET['next'])
            else:
                return redirect('/proxy')
        else:
            return redirect('/proxy/login/')
    return render(request,'myproxy/login.html')

def register_(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_ins = User.objects.create_user(
            username = username,
            password = password
        )
        newuser = authenticate(username=username,password=password)
        login(request,newuser)
        return redirect('/proxy')

    return render(request,'myproxy/register.html')

def log_out(request):
    logout(request)
    return redirect('/proxy')
# ===========验证 IP 事件================================================================

VERIFY_TIME_DELTA = 8
VERIFY_OR_NOT = True

def verify(request):
    验证数据库中的 IP 是否可用
    如果通过验证，在字段 Validated_time 的基础上 加一
    未通过验证，字段 status 变为 I 表示 invalid

    
    global VERIFY_OR_NOT
    if request.method == 'GET':
        try:
            timedelta = request.GET.get('timedelta')
            timedelta = int(timedelta)
        except:
            timedelta = VERIFY_TIME_DELTA

        # if ve != 'False':
        schedule.every(timedelta).hours.do(_verify)
        schedule.run_all()
        while True:
            if not VERIFY_OR_NOT:
                schedule.clear()
                VERIFY_OR_NOT = True
                return JsonResponse({'info':'finished post'})
            schedule.run_pending()

        # print('finishing')
    return HttpResponse("验证 IP 完成")

def _verify():
    验证数据库中所有状态为 V 的 IP

    通过验证则 Validated_time + 1
    未通过则修改 status 为 I

    
    print('start verfying')
    all_ip = Proxy.objects.all()
    for ip in all_ip:
        proxy = {}
        proxy[ip.head] = ip.ip + ':' + ip.port
        if not verify_ip(proxy):
            ip.status = 'I'
            ip.failed_time += 1
            # ip.save()
        ip.Validated_time += 1
        ip.status = 'V'
        ip.failed_time = 0
        ip.save()



def stop_verify(request):
    if request.method == 'GET':
        VERIFY_OR_NOT = False
        return HttpResponse('finished')


'''
