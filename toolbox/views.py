from django.shortcuts import render
import socket
import requests
import ipaddress
import asyncio
import aiohttp
from django.http import JsonResponse

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
    "REDpass": [ipaddress.ip_network("175.24.248.42/32"), ipaddress.ip_network("175.24.248.82/32"),ipaddress.ip_network("175.24.248.125/32"),ipaddress.ip_network("175.24.248.228/32"),ipaddress.ip_network("124.220.29.168/32"),ipaddress.ip_network("115.159.226.104/32")],
    "PA": [ipaddress.ip_network("175.24.248.214/32"), ipaddress.ip_network("175.24.248.13/32")]
}
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
            response = requests.get(f"http://ipinfo.io/{ip_str}/json")
            return response.json().get('city', '') + ", " + response.json().get('region','') + ", " + response.json().get('country', '')
    except ValueError:
        return "无效 IP 地址"

#IP检测与域名解析
def ip_tools(request):
    context = {}

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

#端口扫描功能
async def check_port(ip, port, timeout=1):
    conn = asyncio.open_connection(ip, port)
    try:
        _, writer = await asyncio.wait_for(conn, timeout)
        writer.close()
        await writer.wait_closed()
        return port  # 返回开放的端口号
    except:
        return None
async def scan_ports(ip, start_port, end_port):
    ports = range(start_port, end_port + 1)
    results = await asyncio.gather(*(check_port(ip, port) for port in ports))
    return [port for port in results if port is not None]  # 过滤掉None的值

def port_scan_view(request):
    context = {}
    ip = request.GET.get('ip')
    start_port = request.GET.get('start_port')
    end_port = request.GET.get('end_port')
    # 只有当所有的参数都提供了，才进行端口扫描
    if ip and start_port and end_port:
        start_port = int(start_port)
        end_port = int(end_port)
        open_ports = asyncio.run(scan_ports(ip, start_port, end_port))
        context['open_ports'] = open_ports
        context['ip'] = ip
    return render(request, 'toolbox/port_scan.html',context)

#目录扫描功能
async def check_dir(url, dir_name):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'{url}/{dir_name}') as resp:
            if resp.status == 200:#响应200就返回目录名
                return dir_name

async def scan_dirs(url):
    with open ('../data/fuzzDicts/directoryDicts/top7000.txt','r') as f:
        lines = f.readline()
        # 去除每个目录名的尾部换行符
        dirs = [line.strip() for line in lines]
        # 异步执行
        tasks = [check_dir(url, dir_name) for dir_name in dirs]
        # 等待所有任务完成并获取结果
        results = await asyncio.gather(*tasks)
        # 过滤出存在的目录
        return [dir_name for dir_name in results if dir_name]
def dir_scan_view(request):
    context = {}
    if request.method == 'GET':
        url = request.GET.get('url')
        if url:
            found_dirs = asyncio.run(scan_dirs(url))
            context['found_dirs'] = found_dirs
    return render(request, 'toolbox/dir_scan.html', context)