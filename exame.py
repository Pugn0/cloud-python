import os

# Definindo a pasta onde os arquivos .txt estão localizados
pasta = 'clouds/exame/'

# Certifique-se de que a pasta /filtro/ existe ou crie-a
filtro_pasta = os.path.join(pasta, "filtro")
os.makedirs(filtro_pasta, exist_ok=True)

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
        'xfire://' 'xmlrpc.beep://' 'xmlrpc.beeps://' 'xmpp://' 'xri://' 'ymsgr://' 'z39.50r://' 'z39.50s://', 'oauth://', 'chrome-extension://', 'file:///', 'mailbox://',
        'moz-proxy://', 'pop://', 'content://'
    ]
# Inicializando um dicionário para contar as ocorrências de cada protocolo
contagem_protocolos = {protocolo: 0 for protocolo in protocolos}

# Percorrendo os arquivos na pasta
for arquivo in os.listdir(pasta):
    if arquivo.endswith('.txt'):
        caminho_completo = os.path.join(pasta, arquivo)
        linhas_para_manter = []

        with open(caminho_completo, 'r', encoding='utf-8', errors='ignore') as f:
            linhas = f.readlines()

        for linha in linhas:
            encontrou_protocolo = False
            for protocolo in protocolos:
                if protocolo in linha:
                    encontrou_protocolo = True
                    contagem_protocolos[protocolo] += linha.count(protocolo)
                    nome_arquivo_protocolo = os.path.join(filtro_pasta, protocolo.split('://')[0] + '.txt')
                    with open(nome_arquivo_protocolo, 'a', encoding='utf-8') as p_file:
                        p_file.write(linha)
                    # Atualiza a contagem em tempo real no console
                    atualizacao = ' '.join([f"{proto.split('://')[0]}: {cont}" for proto, cont in contagem_protocolos.items() if cont > 0])
                    print(f"\r{atualizacao}", end="", flush=True)
                    break  # Assumindo que uma linha vai para um arquivo baseado no primeiro protocolo encontrado
            if not encontrou_protocolo:
                linhas_para_manter.append(linha)

        # Reescrever o arquivo original sem as linhas que contêm protocolos
        with open(caminho_completo, 'w', encoding='utf-8', errors='ignore') as f:
            f.writelines(linhas_para_manter)

print("\nProcessamento concluído.")