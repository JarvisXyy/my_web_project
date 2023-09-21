from django.shortcuts import render
import socket
import requests
import ipaddress
import time

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
def get_common_context():
    public_ip = get_public_ip()
    private_ip = get_local_ip()
    return {
        'public_ip': public_ip,
        'private_ip': private_ip
    }
#判断是否在办公网、在哪个职场，若不在职场则显示IP物理位置
def get_office_location(ip_str):
    try:
        ip_obj = ipaddress.ip_address(ip_str)
        if ip_obj.is_private:
            if ip_obj in ipaddress.ip_network("10.16.0.0/12"):
                return "办公网"
            else:
                return "非办公网"
        else:
            for location, ip_ranges in OFFICE_LOCATIONS.items():
                for ip_range in ip_ranges:
                    if ip_obj in ip_range:
                        return location
            start_time = time.time()
            response = requests.get(f"https://ipinfo.io/{ip_str}/json")
            end_time = time.time()
            print(f"Time taken for ipinfo.io request: {end_time - start_time:.2f} seconds")
            return response.json().get('city', '') + ", " + response.json().get('region','') + ", " + response.json().get('country', '')
    except ValueError:
        return "无效 IP 地址"

#获取公网IP
def get_public_ip():
    try:
        start_time = time.time()
        response = requests.get("https://api.ipify.org?format=json").json()["ip"]
        end_time = time.time()
        print(f"Time taken for api64.ipify.org request: {end_time - start_time:.2f} seconds")
        return response
    except:
        return "Unknown"

#获取内网IP
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

def ip_tools(request):
    context = get_common_context()

    if request.method == 'GET':
        if 'ip' in request.GET:
            ip = request.GET.get('ip')
            location = get_office_location(ip)
            context['location'] = location
        elif 'domain' in request.GET:
            domain = request.GET.get('domain')
            try:
                ip_address = socket.gethostbyname(domain)
            except socket.gaierror:
                ip_address = "Unable to resolve domain."
            context['ip_address'] = ip_address
            context['domain'] = domain

    return render(request, 'toolbox/ip_tools.html', context)

