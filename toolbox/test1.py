import asyncio

async def check_port(ip, port,timeout=3):
    conn = asyncio.open_connection(ip, port)
    try:
        _, writer = await asyncio.wait_for(conn, timeout)
        writer.close()
        await writer.wait_closed()
        print(f"Port {port} is open")
    except:
        pass

async def scan_ports(ip, ports, timeout=3):
    tasks = [check_port(ip, port,timeout) for port in ports]
    await asyncio.gather(*tasks)

def main():
    ip = input("Enter the target IP: ")
    start_port = int(input("Enter the start port (e.g., 1): "))
    end_port = int(input("Enter the end port (e.g., 1024): "))

    ports = list(range(start_port, end_port + 1))
    asyncio.run(scan_ports(ip, ports))

if __name__ == "__main__":
    main()
