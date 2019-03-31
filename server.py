


from socket import AF_INET, socket, SOCK_STREAM
from threading import *


def accepter_connection():
    """Attendre les connections."""
    ID=0

    while True:
        client, client_address = SERVER.accept()
        
        addresses[client] = client_address
        print("Nouvelle demande de connexion ",addresses[client])    
        ID+=1    
        Thread(target=traitement_client, args=(client,ID,)).start()


def traitement_client(client,ID):  # prends client socket comme argument.
    global nb_msg
    reporting[ID]=[0,0,0]
    while True:
        client.send(bytes("Pour connecter envoyer 'JOIN' !", "utf8"))
        join = client.recv(BUFSIZ).decode("utf8")
        while (join !="JOIN"):
            client.send(bytes("Pour connecter envoyer 'JOIN' !", "utf8"))
            join = client.recv(BUFSIZ).decode("utf8")
        L1.acquire() # protection de la variable partagé(fichier histo)
        Ecrire_les_histo(nb_msg,"JOIN",ID,0)
        nb_msg+=1
        L1.release()
        L=reporting[ID]
        L[0]+=1
        L2.acquire()
        Ecrire_reporting(reporting)
        L2.release()
        
        client.send(bytes("Bonjour vous êtes connecté ! Ecrivez votre nom et faire entrer !", "utf8"))
        name = client.recv(BUFSIZ).decode("utf8")
        etats[ID]="connecté"
        L3.acquire()
        Ecrire_les_etats(etats)
        L3.release()
        welcome = "Bienvenue %s! Si vous voulez Deconnecter, tapez 'QUIT' !" % name
        client.send(bytes(welcome, "utf8"))
        forme = " Le message sera de la forme ** votre message ici //id_destinataire  ** "
        client.send(bytes(forme, "utf8"))
        msg = "{} a joint le chat et son ID est {}".format(name,ID)
        clients[client] = [ID,name]
        broadcast(bytes(msg, "utf8"))
        

        while True:
            msg = client.recv(BUFSIZ).decode("utf8")
            if msg != "QUIT":
                
                L=msg.split('//')
                if ((len(L)==2) and (L[1].isdigit())):
                    x=int(L[1])
                    if verifier_connecter(x)==True:
                        msg = bytes(L[0], "utf8")
                        Envoyer(msg,x, name+": ")
                        L1.acquire()
                        Ecrire_les_histo(nb_msg,"RECV",ID,x)
                        nb_msg+=1
                        L1.release()
                        LR=reporting[x]
                        LR[2]+=1
                        L2.acquire()
                        Ecrire_reporting(reporting)
                        L2.release()
                        L1.acquire()
                        Ecrire_les_histo(nb_msg,"SEND",ID,x)
                        nb_msg+=1
                        L1.release()
                        LR=reporting[ID]
                        LR[1]+=1
                        L2.acquire()
                        Ecrire_reporting(reporting)
                        L2.release()
                    else:
                        client.send(bytes("Message non transmis car le destinataire est deconnecté !", "utf8"))
                else:
                    client.send(bytes("Format message est invalide !", "utf8"))
                
            
                    
                
                    
            else:
                etats[ID]="déconnecté"
                L3.acquire()
                Ecrire_les_etats(etats)
                L3.release()
                L1.acquire()
                Ecrire_les_histo(nb_msg,"QUIT",ID,0)
                nb_msg+=1
                L1.release()
                LR=reporting[ID]
                client.send(bytes("Votre Statistisues: nombre de session: "+str(LR[0])+" nombre de message envoyés: "+str(LR[1])+" nombre de messages reçu: "+str(LR[2]), "utf8"))
                broadcast(bytes("%s a quitté le chat." % name, "utf8"))
                break





def Ecrire_les_etats(dic):
    fout = "participant.txt"
    fo = open(fout, "w")
    for k, v in dic.items():
        fo.write(str(k) + '         '+ str(v) + '\n\n')
    fo.close()

def Ecrire_les_histo(nb,Type,src,dest):
   
    fout = "histo.txt"
    fo = open(fout, "a")
    fo.write(str(nb) + '         '+ Type + '           '+str(src)+'            '+str(dest)+'\n\n')
    fo.close()

def Ecrire_reporting(dic):
    fout = "reporting.txt"
    fo = open(fout, "w")
    for k, v in dic.items():
        fo.write(str(k) + '         '+ str(v[0]) +'         '+str(v[1])+'         '+'         '+str(v[2])+ '\n\n')
    fo.close()


def broadcast(msg, prefix=""):  
    """Broadcasts le message à tous les clients."""
    for sock in clients:
        sock.send(bytes(prefix, "utf8")+msg)


def Envoyer(msg,x, prefix=""): 
    """Envoyer le message à un client."""
    for sock, value in clients.items():
        if value[0]==x:
            sock.send(bytes(prefix, "utf8")+msg)
    
            



def verifier_connecter(x):
    if x in etats:
        if etats[x]=="connecté":
                 return True
    return False

def aff_fichier(nom):
    fout = nom
    fo = open(fout, "r")
    fich=fo.read()
    print(fich)
    fo.close()

def calc_nbmsg(dic):
    s=0
    for v in dic.values():
       s+=v[1]
    return s


    
def affichage_fichiers():
    while True:
        x=input("Pour afficher le fichier historique tapez 1 \nPour afficher le fichier reporting tapez 2 \nPour consulter les etats des participant tapez 3 \n")
        if (x=='1'):
            aff_fichier("histo.txt")
        elif (x=='2'):
            print("Le nombre total de messages echangés: "+str(calc_nbmsg(reporting)))
            x=int(input("Donner ID du participant pour savoir son nombre de session: "))
            if x in reporting:
                print(reporting[x][0])
            else:
                print("ce participant n'existe pas!")
        elif (x=='3'):
            x=int(input("Donner ID du participant: "))
            if x in etats:
                print("\n "+etats[x])
            else:
                print("ce participant n'existe pas!")
                  
        else:
            print("choix invalide !")
        
clients = {}
addresses = {}
etats={}
reporting={}

nb_msg=1
L1=Lock()
L2=Lock()
L3=Lock()

HOST = ''
PORT = 33000
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)


if __name__ == "__main__":
    SERVER.listen(5)
    print("Attente d'une connexion...")
    ACCEPT_THREAD = Thread(target=accepter_connection)
    AFFICHAGE_THREAD= Thread(target=affichage_fichiers)
    ACCEPT_THREAD.start()
    AFFICHAGE_THREAD.start()       
    ACCEPT_THREAD.join()
    AFFICHAGE_THREAD.join()
    SERVER.close()
