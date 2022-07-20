from calcipv4 import CalcIPv4

calc_ipv4 = CalcIPv4(ip='192.168.1.15', prefixo=24)

print(f'IP: {calc_ipv4.ip}')
print(f'Máscara: {calc_ipv4.mascara}')
print(f'Rede: {calc_ipv4.rede}')
print(f'Broadcast: {calc_ipv4.broadcast}')
print(f'Prefixo: {calc_ipv4.prefixo}')
print(f'Número de IPs na Rede: {calc_ipv4.numero_ips}')