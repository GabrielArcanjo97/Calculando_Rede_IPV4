import re


class CalcIPv4:
    def __init__(self, ip, mascara=None, prefixo=None):
        self.ip = ip
        self.mascara = mascara
        self.prefixo = prefixo

        self._set_broadcast()
        self._set_rede()

    @property
    def rede(self):
        return self._rede

    @property
    def broadcast(self):
        return self._broadcast

    @property
    def numero_ips(self):
        return self._get_numero_ips()

    @property
    def ip(self):
        return self._ip

    @ip.setter
    def ip(self, valor):
        # validando ip
        if not self._valida_ip(valor):
            raise ValueError('IP inválido.')

        self._ip = valor
        self._ip_bin = self._ip_to_bin(valor) # tranformando ip em binário

    @property
    def mascara(self):
        return self._mascara

    @mascara.setter
    def mascara(self, valor):
        if not valor:
            return
        #validando a mascara
        if not self._valida_ip(valor):
            raise ValueError('Mascara inválida.')

        self._mascara = valor
        self._mascara_bin = self._ip_to_bin(valor)

        if not hasattr(self, 'prefixo'): # se não foi configurado o prefixo, configure
            self.prefixo = self._mascara_bin.count('1') # pegando todos os valores 1

    @property
    def prefixo(self):
        return self._prefixo

    @prefixo.setter
    def prefixo(self, valor):
        if not valor:
            return

        if not isinstance(valor, int):
            raise TypeError('Prefixo precisa ser inteiro.')

        if valor > 32:
            raise TypeError('Prefixo precisa ter 32Bits')

        self._prefixo = valor

        #convertendo prefixo em binário, .ljust(32, '0') está colocando a linha a esquerda e mandando a largura que é 32 e 0 para preencher o restante
        self._mascara_bin = (valor * '1').ljust(32, '0')

        if not hasattr(self, 'mascara'): # se não foi configurado a mascara, configure
            self. mascara = self._bin_to_ip(self._mascara_bin) # pegando todos os valores 1

    #validando se é um bloco de 4 número, e cada bloco pode ter 3 números, utilizando a bibli re
    @staticmethod
    def _valida_ip(ip): #um método static para validação.
        regexp = re.compile(
            r'^([0-9]{1,3}).([0-9]{1,3}).([0-9]{1,3}).([0-9]{1,3})$'
        )
        if regexp.search(ip):
            return True

    #função para tranformar a mascara em binário
        #tranformando IP em binário
    @staticmethod
    def _ip_to_bin(ip):
        # separando o ip em partes, a partir do ponto
        blocos = ip.split('.')
        # transformando minha mascara em binário, [2:].zfill(8) começando da posição 2 e transformando de octetos
        blocos_binarios = [bin(int(x))[2:].zfill(8) for x in blocos]
        return ''.join(blocos_binarios)

    #converter a mascara, quando configurar o prefixo, converter a mascara em IP, ao invez de ip_to_bin vai ser bin_to_ip
    @staticmethod
    def _bin_to_ip(ip):
        n = 8
        blocos = [str(int(ip[i:n+i], 2)) for i in range(0, 32, n)]
        return '.'.join(blocos)

    #calculando o broadcast e a rede
    def _set_broadcast(self):
        host_bits = 32 - self.prefixo # pegando a quantidade de bits usada para hosts
        self._broadcast_bin = self._ip_bin[:self.prefixo] + (host_bits * '1')#fatiado de zero ao numero do meu prefixo, convertendo o final em 1
        self._broadcast = self._bin_to_ip(self._broadcast_bin)
        return self._broadcast

    def _set_rede(self):
        host_bits = 32 - self.prefixo
        self._rede_bin = self._ip_bin[:self.prefixo] + (host_bits * '0')
        self._rede = self._bin_to_ip(self._rede_bin)
        return self._rede

    def _get_numero_ips(self):
        return 2 ** (32 - self.prefixo)