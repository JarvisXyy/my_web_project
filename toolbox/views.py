from django.shortcuts import render
import socket
import requests
import ipaddress

#IP地址判断及查询
def ip_address(request):
    location = None
    is_reserved = False
    office_location = None
    office_dns = None
    public_ip = get_public_ip()
    private_ip = get_local_ip()
    #办公职场判定
    OFFICE_LOCATIONS = {
        "上海复兴": [ipaddress.ip_network("101.52.223.0/28")],
        "上海杨浦": [ipaddress.ip_network("222.71.190.224/29"), ipaddress.ip_network("112.64.123.72/29")],
        "北京中海": [ipaddress.ip_network("111.207.229.96/29"), ipaddress.ip_network("219.142.253.88/30"),
                     ipaddress.ip_network("124.127.48.64/27"), ipaddress.ip_network("123.127.218.192/27"),
                     ipaddress.ip_network("111.207.229.192/27")],
        "广州": [ipaddress.ip_network("14.23.41.48/29"), ipaddress.ip_network("210.21.27.0/29")],
        "海南": [ipaddress.ip_network("153.0.157.192/27"), ipaddress.ip_network("59.49.203.0/24")],
        "武汉世贸": [ipaddress.ip_network("220.249.113.180/30"), ipaddress.ip_network("113.57.132.96/29"),
                     ipaddress.ip_network("220.249.113.176/30"), ipaddress.ip_network("113.57.132.184/29"),
                     ipaddress.ip_network("220.249.90.220/30"), ipaddress.ip_network("119.97.214.222/32"),
                     ipaddress.ip_network("59.173.243.74/32"), ipaddress.ip_network("59.175.227.210/32")],
        "武汉APP": [ipaddress.ip_network("111.46.57.189/32"), ipaddress.ip_network("111.46.57.240/29"),
                    ipaddress.ip_network("58.19.35.0/26")],
        "武汉保利": [ipaddress.ip_network("58.49.45.8/30"), ipaddress.ip_network("220.249.92.152/29")],
        "浦东仓库": [ipaddress.ip_network("61.169.21.168/32"), ipaddress.ip_network("61.169.21.170/31"),
                     ipaddress.ip_network("61.169.21.172/30")],
        "海外翻墙（自有）": [ipaddress.ip_network("209.9.115.64/28")],
        "REDpass": [ipaddress.ip_network("175.24.248.42/32"), ipaddress.ip_network("175.24.248.82/32")],
        "PA": [ipaddress.ip_network("175.24.248.214/32"), ipaddress.ip_network("175.24.248.13/32")]
    }

    # 检查是否在办公网
    def get_office_location(ip_str):
        try:
            ip_obj = ipaddress.ip_address(ip_str)

            #判断IP是否为内网IP
            if ip_obj.is_private:
                #判断IP是否为办公网IP
                if ip_obj in ipaddress.ip_network("10.16.0.0/12"):
                    return "办公网"
                else:
                    return "非办公网"
            else:
                #判断IP是否在职场内
                for location, ip_ranges in OFFICE_LOCATIONS.items():
                    for ip_range in ip_ranges:
                        if ip_obj in ip_range:
                            return location

                #若IP不在职场范围，则显示IP的物理位置
                response = requests.get(f"https://ipinfo.io/{ip_str}/json")
                return response.json().get('city', '') + ", " + response.json().get('region','') + ", " + response.json().get('country', '')

        except ValueError:
            return "无效 IP 地址"


    if request.method == 'POST':
        ip = request.POST.get('ip')
        location = get_office_location(ip)

    return render(request, 'toolbox/ip_address.html', {
        'location': location,
        'is_reserved': is_reserved,
        'office_location': office_location,
        'office_dns': office_dns,
        'public_ip': public_ip,
        'private_ip': private_ip
    })

#获取本机公网IP
def get_public_ip():
    try:
        return requests.get("https://httpbin.org/ip").json()["origin"]
    except:
        return "Unknown"

#获取本机私网IP
def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.254.254.254', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP


#DNS解析
def dns_lookup(request):
    ip_address = None
    domain = None

    if request.method == 'POST':
        domain = request.POST.get('domain')
        try:
            ip_address = socket.gethostbyname(domain)
        except socket.gaierror:
            ip_address = "Unable to resolve domain."

    return render(request, 'toolbox/dns_lookup.html', {'ip_address': ip_address, 'domain': domain})
