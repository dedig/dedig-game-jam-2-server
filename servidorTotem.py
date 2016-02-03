from bottle import *
import sys



#-------------------------------------------------------------------------------------------------------------------------------------------------------#
#1-minion
#2-guard
#3-boss
#4-mage
minions=["soldado","capitao","General","Sacerdote","Slow"]
fila=[]


users = []
shake = False
endGame = False

#------------------------------------------------------------------------------------------------------------------------------------------------------#

def CORS(req,code=200,data=""):
    '''
    Funcao para implementacao do CORS (Cross-Origin Resource Sharing).
    Deve ser usado para retornar a resposta ao cliente, se ele for web ou nao.
    req - Response da funcao
    code - codigo de retorno baseado HTTP
    data - informacao a ser retornada
    pode ser utilizado diretamente no return da funcao.
    '''
    req.set_header("Access-Control-Allow-Credentials", "true")
    req.set_header("Access-Control-Allow-Headers", "Accept, X-Access-Token, X-Application-Name, X-Request-Sent-Time")
    req.set_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
    req.set_header("Access-Control-Allow-Origin", "*")
    
    req.body = data
    req.status = code
    
    return req

def conversorDeFila():
    final = str(fila).replace("[","").replace("]","")
    final+= ",*"+str(str(len(users)))+"*"
    return final
#------------------------------------------------------------------------------------------------------------------------------------------------------#
#parte do pc
@post('/pc')
def pc():
    global fila
    if(endGame):
        return CORS(response,200,"endGame")
    resposta = conversorDeFila()
    fila = []
    return CORS(response,200,resposta)


@post('/shake')
def shake():
    print "Shake!"
    return CORS(response,200,"mexecacoisa")

@post('/endGame')
def end():
    endGame = True
    print "Fim de jogo"
    return CORS(response,200,"cabou")


@post('/kill')
def kill():
    print "Good Tchau!"
    sys.exit(0)
    return CORS(response,200,"cabou")
#------------------------------------------------------------------------------------------------------------------------------------------------------#
#parte do mobile
@post('/connect')
def connect():
    ip = request.remote_addr
    
    if(ip not in users):
        users.append(ip)
        print "Jogador \""+ip+"\" Conectou!"
        print "usuarios conectados: "+str(len(users))
        return CORS(response,200)

@post('/minion')
def minion():
    try:
        m = int(request.forms.get('minion'))
        fila.append(m)
        print "Minion '"+str(minions[m])+"' criado pelo: "+request.remote_addr
    except:
        pass
    return CORS(response,200)

@post('/mobile')
def mobile():
    var = ""
    if(endGame):
        return CORS(response,200,"endGame")
    if(shake):
        var = "shake"
    return CORS(response,200,var)

#------------------------------------------------------------------------------------------------------------------------------------------------------#
motd = "*Bem vindo ao Servidor de Totem 1.0*"

print motd
run(host='0.0.0.0',quiet=True, port=46370)
