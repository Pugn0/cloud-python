import os
import sqlite3

# Definições iniciais
pasta = 'clouds/exame/'
filtro_pasta = os.path.join(pasta, "filtro")
os.makedirs(filtro_pasta, exist_ok=True)
conn = sqlite3.connect('protocolos.db')
cursor = conn.cursor()

# Otimizações do SQLite
cursor.execute('PRAGMA journal_mode=WAL')  # Melhora concorrência e performance de escrita
cursor.execute('PRAGMA cache_size=-10000')  # Aumenta cache para reduzir I/O de disco
cursor.execute('PRAGMA synchronous=OFF')  # Desativa sincronização de disco (cuidado com perda de dados)

# Criação da tabela e índices
cursor.execute('''
CREATE TABLE IF NOT EXISTS urls (
    id INTEGER PRIMARY KEY,
    protocolo TEXT,
    url TEXT UNIQUE,
    dado TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)''')
cursor.execute('CREATE INDEX IF NOT EXISTS idx_protocolo ON urls(protocolo)')
cursor.execute('CREATE INDEX IF NOT EXISTS idx_url ON urls(url)')

def atualizar_display(contagens_protocolos, linhas_ignoradas):
    display = ' '.join([f"{proto}: {cont}" for proto, cont in contagens_protocolos.items() if cont > 0])
    print(f"\r{display} | Linhas ignoradas: {linhas_ignoradas}", end="", flush=True)


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

# Inicializa contagens de protocolos
contagens_protocolos = {protocolo: 0 for protocolo in protocolos}

# Criando/conectando ao banco de dados SQLite
conn = sqlite3.connect('protocolos.db')
cursor = conn.cursor()

# Criando a tabela se não existir
cursor.execute('''
CREATE TABLE IF NOT EXISTS urls (
    id INTEGER PRIMARY KEY,
    protocolo TEXT,
    url TEXT UNIQUE,
    dado TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
''')

# Criando índice para acelerar as consultas por protocolo
cursor.execute('CREATE INDEX IF NOT EXISTS idx_protocolo ON urls(protocolo)')
cursor.execute('CREATE INDEX IF NOT EXISTS idx_url ON urls(url)')

linhas_ignoradas = 0  # Contador para linhas ignoradas devido a duplicação

# Função para inserir dados no banco de dados
def inserir_protocolo(protocolo, linha):
    global linhas_ignoradas, contagens_protocolos
    try:
        cursor.execute('INSERT INTO urls (protocolo, url, dado) VALUES (?, ?, ?)', (protocolo, linha, None))
        conn.commit()
        contagens_protocolos[protocolo] += 1
        atualizar_display(contagens_protocolos, linhas_ignoradas)
    except sqlite3.IntegrityError:
        # Linha já existe no banco de dados, ignorando...
        linhas_ignoradas += 1
        atualizar_display(contagens_protocolos, linhas_ignoradas)

# Lendo arquivos e processando linhas
for arquivo in os.listdir(pasta):
    if arquivo.endswith('.txt'):
        caminho_completo = os.path.join(pasta, arquivo)
        
        with open(caminho_completo, 'r', encoding='utf-8', errors='ignore') as f:
            linhas = f.readlines()

        for linha in linhas:
            for protocolo in protocolos:
                if protocolo in linha:
                    inserir_protocolo(protocolo, linha.strip())
                    break  # Assumindo que uma linha vai para um arquivo baseado no primeiro protocolo encontrado

# Fechando a conexão com o banco de dados
conn.close()

print("\nProcessamento concluído.")
contagens_protocolos = {protocolo: 0 for protocolo in protocolos}
linhas_ignoradas = 0

# Função para inserir dados no banco de dados utilizando inserção em massa dentro de uma transação
def inserir_protocolo_em_massa(dados_para_inserir):
    global linhas_ignoradas
    try:
        cursor.execute('BEGIN')
        cursor.executemany('INSERT INTO urls (protocolo, url, dado) VALUES (?, ?, ?)', dados_para_inserir)
        cursor.execute('COMMIT')
    except sqlite3.IntegrityError:
        linhas_ignoradas += len(dados_para_inserir)  # Ajustar de acordo com o comportamento esperado para duplicatas
        cursor.execute('ROLLBACK')

# Processamento de arquivos
for arquivo in os.listdir(pasta):
    if arquivo.endswith('.txt'):
        caminho_completo = os.path.join(pasta, arquivo)
        dados_para_inserir = []

        with open(caminho_completo, 'r', encoding='utf-8', errors='ignore') as f:
            for linha in f:
                for protocolo in protocolos:
                    if protocolo in linha:
                        dados_para_inserir.append((protocolo, linha.strip(), None))
                        contagens_protocolos[protocolo] += 1
                        break

        # Insere dados acumulados em massa
        if dados_para_inserir:
            inserir_protocolo_em_massa(dados_para_inserir)
            atualizar_display(contagens_protocolos, linhas_ignoradas)

conn.close()  # Fecha a conexão com o banco de dados ao final do processamento
print("\nProcessamento concluído.")