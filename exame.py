import os

# Definindo a pasta onde os arquivos .txt estão localizados
pasta = 'clouds/exame/'

# Lista expandida de protocolos para procurar
# Padrões de Internet e Redes (URI com base IANA)
protocolos = [
        'http://', 'https://', 'ftp://', 'ssh://', 
        'smtp://', 'imap://', 'telnet://', 'sftp://', 
        'ldap://', 'ldaps://', 'tftp://', 'dhcp://', 
        'dns://', 'snmp://', 'ntp://', 'sip://', 'smtps://', 
        'pop3://', 'pop3s://', 'imap://', 'imaps://', 'android://',
        'http://' 'https://' 'ftp://' 'ftps://' 'sftp://' 'ldap://' 'ldaps://' 'mailto://' 'telnet://'
        'sip://' 'ssh://' 'xmpp://' 'ws://' 'wss://' 'rtmp://' 'mms://' 'irc://' 'ircs://' 'nfs://'
        'smb://' 'smtp://' 'imap://' 'pop://' 'dns://' 'dhcp://' 'file://' 'git://' 'svn://' 'data://'
        'chrome://' 'view-source://' 'cvs://' 'gopher://' 'mid://' 'cid://' 'news://' 'nntp://'
        'prospero://' 'tel://' 'urn://' 'dvb://' 'fax://' 'modem://' 'packet://' 'soap.beep://'
        'soap.beeps://' 'xmlrpc.beep://' 'xmlrpc.beeps://' 'ni://' 'nih://' 'tag://' 'dns://'
        'example://' 'geo://' 'go://' 'gopher://' 'h323://' 'iax://' 'icap://' 'jar://' 'jms://'
        'keyparc://' 'lastfm://' 'ldaps://' 'magnet://' 'maps://' 'market://' 'message://' 'msrp://'
        'msrps://' 'mtqp://' 'mupdate://' 'mvn://' 'news://' 'nfs://' 'ni://' 'nih://' 'nntp://'
        'opaquelocktoken://' 'pop://' 'pres://' 'reload://' 'rtsp://' 'rtsps://' 'rtspu://' 'service://'
        'session://' 'shttp://' 'sieve://' 'sms://' 'snmp://' 'soap.beep://' 'soap.beeps://' 'soldat://'
        'spotify://' 'ssdp://' 'steam://' 'stun://' 'stuns://' 'submit://' 'svn://' 'tag://' 'teamspeak://'
        'teliaeid://' 'things://' 'thismessage://' 'tip://' 'tn3270://' 'tool://' 'turn://' 'turns://'
        'tv://' 'udp://' 'unreal://' 'urn://' 'ut2004://' 'vemmi://' 'ventrilo://' 'videotex://' 'view-source://'
        'wais://' 'webcal://' 'wpid://' 'ws://' 'wss://' 'wtai://' 'wyciwyg://' 'xcon://' 'xcon-userid://'
        'xfire://' 'xmlrpc.beep://' 'xmlrpc.beeps://' 'xmpp://' 'xri://' 'ymsgr://' 'z39.50r://' 'z39.50s://'
    ]
# Inicializando um dicionário para contar as ocorrências de cada protocolo
contagem_protocolos = {protocolo: 0 for protocolo in protocolos}

# Percorrendo os arquivos na pasta
for arquivo in os.listdir(pasta):
    if arquivo.endswith('.txt'):
        caminho_completo = os.path.join(pasta, arquivo)
        with open(caminho_completo, 'r', encoding='utf-8', errors='ignore') as f:
            for linha in f:
                for protocolo in protocolos:
                    ocorrencias = linha.count(protocolo)
                    if ocorrencias:
                        contagem_protocolos[protocolo] += ocorrencias
                        # Atualizando a contagem em tempo real
                        atualizacao = ' '.join([f"{proto}: {cont}" for proto, cont in contagem_protocolos.items() if cont > 0])
                        print(f"\r{atualizacao}", end="", flush=True)
                        

print("\n\nFinalizado:")
