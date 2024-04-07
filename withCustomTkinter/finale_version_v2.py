from customtkinter import *
from customtkinter import CTk, CTkScrollableFrame

app1 = CTk()
app1.geometry("800x550")
app1.title("Le mouteur d'inference")

t1 = CTkLabel(master=app1,text="Enter la base de faits separer par ','", font=("Helvetica",20))
t1.place(relx=0.05,rely=0.05,anchor="nw")
bfentry = CTkEntry(master=app1, placeholder_text="e.g: A,B,C,D....")
bfentry.place(relx=0.5,rely=0.05,anchor="nw")


t2 = CTkLabel(master=app1,text="Enter le but(Obligatoire dans le chainage Arriere)", font=("Helvetica",16))
t2.place(relx=0.05,rely=0.15,anchor="nw")
but = CTkEntry(master=app1, placeholder_text="e.g: A")
but.place(relx=0.5,rely=0.15,anchor="nw")


rg = CTkLabel(master=app1, text="Enter les regles comme ca (a,x->y,z....) :", font=('Helvetica', 22))
rg.place(relx=0.2, rely=0.25,anchor="nw")

regles_entries = []
def ajouter_regle():
    entry = CTkEntry(master=app1)
    entry.pack_configure(padx=20, pady=8,anchor="se")
    regles_entries.append(entry)

btn = CTkButton(master=app1, text="Ajouter Une Règle",command=ajouter_regle)
btn.place(relx=0.4, rely=0.3,anchor="nw")



def filtrage(regles,base_des_faits):
    conflit = [] #list des regles applicable
    for premisse,conclusion in regles:
        if premisse.issubset(base_des_faits) and conclusion not in base_des_faits:
            conflit.append((premisse,conclusion))
    return conflit

def grandNbrPremisse(conflit): #? fonction pour trouver la regle du plus nombre des premisses
    maxLenPremisse = 0
    index = 0
    for i, regle in enumerate(conflit):
        premisse, conclusion = regle
        if maxLenPremisse < len(premisse):
            maxLenPremisse = len(premisse)
            index = i
    # print(f"index trouver dans la fonction ==> {index}")
    return index #? retourner la position dans la list des conflit du la regle ayant le plus de premisses



def avAction():
    BUT = but.get()
    fenAv = CTkToplevel()
    fenAv.geometry("800x800")
    fenAv.title("Chainage Avant")
    scrollable_frame = CTkScrollableFrame(master=fenAv)
    scrollable_frame.pack(fill="both", expand=True)
    fenAv.grab_set()

    base_des_faits = set(bfentry.get().split(","))  # placer la base des faits dans un 'set'

    regles = [] # todo:list des regles e.g => (a,b)->e
    # regles = [({"a","b"},"f"),({"f","h"},"i"),({"d","h","g"},"a"),({"o","g"},"h"),({"e","h"},"b"),({"g","a"},"b"),({"g","h"},"p"),({"g","h"},"q"),({"d","o","g"},"j")]

    for entry in regles_entries:
        regle_value = entry.get() #return regle in string value
        if '->' in regle_value:
            premisses, conclusion = regle_value.split("->") #todo: returner partie gauche du regle dans premisse et partie droite du regle dans "conclusion"
            premisses = set(premisses.split(","))
            regles.append((premisses,conclusion)) # charger la list des regles


    reglesCopy = regles.copy() #? un copie des regles utiliser pour indexer les regles appliquer

    conflit = filtrage(regles, base_des_faits) #? conflit: list des regles applicables
    ButTrouver = False

    #? tanque la list des regles applicable n'est pas vide
    i = 1
    while len(conflit) != 0 and ButTrouver == False:
        for regle in conflit:
            premisse, conclusion = regle
            indice = grandNbrPremisse(conflit) #trouver l'indice du du regle de plus des premisse 
            if conflit[indice] != conflit[conflit.index(regle)]: continue # en passer tout les regles du la boucle "for" , jusqu'a trouver la regle ayant le plus nombre des premisses
            if conclusion != BUT:
                base_des_faits.add(conclusion)

                #ajouter le nombre du cycle
                cycleaff = CTkLabel(master=scrollable_frame, text=f"Cycle {i}",font=("Helvetica", 17,"bold"),bg_color="green")
                cycleaff.pack_configure(padx=12,pady=6,anchor="center")
                i+=1

                #afficher conflit :
                affconflit= CTkLabel(master=scrollable_frame, text="LIST DES CONFLITS :")
                affconflit.pack_configure(padx=12,pady=8,anchor="center")

                for r in conflit:
                    c1= CTkLabel(master=scrollable_frame, text=f"R = {r}")
                    c1.pack_configure(padx=12, pady=10,anchor="center")

                infere = CTkLabel(master=scrollable_frame,text=f"==>(Appliquer R{reglesCopy.index(regle) + 1}) En ajouter [{conclusion}] dans la base de faits <==",font=("Helvetica", 15,"bold"))
                infere.pack_configure(padx=12, pady=12,anchor="center")

                nvbase =CTkLabel(master=scrollable_frame,text=f"Nouvelle base de faits {base_des_faits}", font=('Helvetica', 18))
                nvbase.pack_configure(padx=14,pady=12,anchor="center")

                #add a separator
                separator = CTkLabel(scrollable_frame,text="",height=0.5,fg_color="gray")
                separator.pack(fill="x", padx=10)  #horizontal

                regles.remove(regles[regles.index(regle)])
                #? supprimer la regle apres l'application

                conflit = filtrage(regles, base_des_faits)

            else: # ?dans le cas du trouver le but
                base_des_faits.add(conclusion)  #? ajouter le but dans la bf et quitez l'operation

                #ajouter le nombre du cycle
                cycleaf3 = CTkLabel(master=scrollable_frame, text=f"Cycle {i}",font=("Helvetica", 17,"bold"),bg_color="green")
                cycleaf3.pack_configure(padx=12,pady=6,anchor="center")
                i+=1

                # afficher list des conflit :
                for r in conflit:
                    c2 = CTkLabel(master=scrollable_frame, text=f"R = {r}")
                    c2.pack_configure(padx=12,pady=10,anchor="center")

                infere = CTkLabel(master=scrollable_frame,text=f"==>(Appliquer R{reglesCopy.index(regle) + 1}) En ajouter [{conclusion}] dans la base de faits <==",font=("Helvetica", 15,"bold"))
                infere.pack_configure(padx=12, pady=12,anchor="center")

                nvbase = CTkLabel(master=scrollable_frame,text=f"Nouvelle base de faits {base_des_faits}",font=('Helvetica', 18))
                nvbase.pack_configure(padx=14,pady=12,anchor="center")

                #add a separator
                separator2 = CTkLabel(scrollable_frame, height=0.5,text="", fg_color="gray")
                separator2.pack(fill="x", padx=10)  #horizontal

                infere1 = CTkLabel(master=scrollable_frame,text=f"On trouver le BUT [{BUT}] , le mouteur d'inference s'arrete ", font=('Helvetica', 22),bg_color="green")

                infere1.pack_configure(padx=16, pady=12,anchor="center")
                ButTrouver = True #? pour quiter la boucle "while"

                break #? pour quiter la boucle "for"

    if len(conflit) == 0 and not ButTrouver:
        cyclelbl = CTkLabel(master=scrollable_frame, text=f"Cycle {i}",font=("Helvetica", 17),bg_color="green")
        cyclelbl.pack_configure(padx=12,pady=6,anchor="center")
        i+=1
        echeclbl = CTkLabel(master=scrollable_frame,text=f"Le Mouteur d'inference S'Arrete, il existe pas des regles applicables !! ", font=('Helvetica', 22),bg_color="red")
        echeclbl.pack_configure(padx=20, pady=15,anchor="center")


    fenAv.mainloop()



def arAction():

    BUT = but.get()
    fenAr = CTkToplevel()
    fenAr.geometry("800x800")
    fenAr.title("Chainage Arriere")
    scrollable_frame2 = CTkScrollableFrame(master=fenAr)
    scrollable_frame2.pack(fill="both", expand=True)
    fenAr.grab_set()

    base_des_faits = list(bfentry.get().split(","))  # placer la base des faits dans un 'set'

    def filtrage_arr(regles, but):
        conflit = []
        for premisse, conclusion in regles:
            if conclusion == but:
                conflit.append((premisse,conclusion))
        return conflit

    global regles
    regles = [] # todo:list des regles e.g => (a,b)->e

    #second ligne is just an exemple :
    # regles = [(["a","b"],"f"),(["f","h"],"i"),(["d","h","g"],"a"),(["o","g"],"h"),(["e","h"],"b"),(["g","a"],"b"),(["g","h"],"p"),(["g","h"],"q"),(["d","o","g"],"j")]

    for entry in regles_entries:
        regle_value = entry.get() #return regle in string value
        if '->' in regle_value:
            premisses, conclusion = regle_value.split("->") #todo: returner partie gauche du regle dans premisse et partie droite du regle dans "conclusion"
            premisses = list(premisses.split(","))
            regles.append((premisses,conclusion)) # charger la list des regles

    reglesCopy = regles.copy() #? un copie des regles utiliser pour indexer les regles appliquer

    LDP =[]
    LDP.insert(0,BUT)
    list_des_conclusion_deja_prouve = []
    nv_but = BUT
    i = 1

    def find_regle(conflit): #trouver la regle ayant plus des premisse
        indice = grandNbrPremisse(conflit) #trouver l'indice du regle de plus des premisse
        for regle in conflit:
            if conflit[indice] == conflit[conflit.index(regle)]:
                return regle

    conflit = []
    historique = {} # pour souvgarder l'historique pour chaque cycle
    newGoalTable = []

    def chainage_arr(regles, LDP,nv_but, newGoalTable, conflit,list_des_conclusion_deja_prouve,i, base_des_faits,historique):
        echec = False

        while len(LDP) != 0:

            #todo: ajouter le nombre du cycle
            cycle = CTkLabel(master=scrollable_frame2, text=f"Cycle {i}",font=("Helvetica", 17,"bold"),bg_color="green")
            cycle.pack_configure(padx=12,pady=6,anchor="center")
            LDPcopy = LDP.copy() #souvgarder la valleur avant la modification

            newGoalTable.append(nv_but)
            nv_but = newGoalTable[len(newGoalTable) - 1]

            #todo: afficher le nv but pour prouver
            butaff = CTkLabel(master=scrollable_frame2, text=f"Le nouveau But a prouver => [ {nv_but} ]", font=('Helvetica', 24),bg_color="yellow",fg_color="black")
            butaff.pack_configure(padx=12,pady=12,anchor="center")

            if nv_but in base_des_faits:
                conflit = filtrage_arr(regles, nv_but)

                LDP.remove(nv_but) #todo: supprimer le but deja prouver d'apres BF

                #todo: afficher le but
                butaff = CTkLabel(master=scrollable_frame2, text=f"---> But [{nv_but}] appartient aux base des faits, on le supprimer",font=("Helvetica",17,"bold"))
                butaff.pack_configure(padx=12,pady=8,anchor="center")

                #todo: afficher LDP :
                ldpAff = CTkLabel(master=scrollable_frame2, text=f"LIST LDP : {LDP}",font=('Helvetica', 22,"bold"),fg_color="green")
                ldpAff.pack_configure(padx=12,pady=12,anchor="center")

                #add a separator
                separator = CTkLabel(scrollable_frame2, height=0.5,text="", fg_color="gray")
                separator.pack(fill="x", padx=15)  #horizontal

            elif nv_but in list_des_conclusion_deja_prouve:
                conflit = filtrage_arr(regles, nv_but)

                LDP.remove(nv_but) #todo-> supprimer le but deja prouver et remplacer par ces premisse

                #todo: afficher le but deja prouver
                butaff = CTkLabel(master=scrollable_frame2, text=f"---> But [{nv_but}] deja prouver dans les cycles precedent",font=("Helvetica",17,"bold"))
                butaff.pack_configure(padx=12,pady=8,anchor="center")

                #todo: afficher LDP :
                ldpAff = CTkLabel(master=scrollable_frame2, text=f"LIST LDP : {LDP}",font=('Helvetica', 22,"bold"),fg_color="green")
                ldpAff.pack_configure(padx=12,pady=12,anchor="center")

                #add a separator
                separator = CTkLabel(scrollable_frame2, height=0.5,text="", fg_color="gray")
                separator.pack(fill="x", padx=15)  #horizontal

            else: # else n'est pas prouver precedament

                conflit = filtrage_arr(regles, nv_but)

                if not conflit: # pas de conflit (None)

                    conflitaff = CTkLabel(master=scrollable_frame2, text="LIST DES CONFLITS VIDE ??",font=('Helvetica',23,"bold"),fg_color="red")
                    conflitaff.pack_configure(padx=12,pady=14,anchor="center")

                    echec = True

                    #todo: afficher le blocage
                    butaff = CTkLabel(master=scrollable_frame2, text=f"Je Bloquer dans le cycle {i},--> BACKTRACKING TO CYCLE N-[{i-1}]",font=('Helvetica', 22,"bold"),fg_color="red")
                    butaff.pack_configure(padx=12,pady=8,anchor="center")

                    del newGoalTable[-1] #todo: supprimer dernier but que n'est pas utiliser (comme "e" dans l'ex)
                    nv_but = newGoalTable[len(newGoalTable) - 1] # le nv_but valeur prendre la valleur de nv_but du cycle precedent dans le cas n'est de conflit avec dans le cycle acctuel

                    historique[f"{i-2}"][5].pop() #todo :supprimer le avant dernier valleur du list des conclusion deja prouve pour retester

                    global last_cycle
                    last_cycle = historique[f"{i-1}"]
                    break

                else:
                    regle = find_regle(conflit)
                    premisses, conclusion = regle
                    list_des_conclusion_deja_prouve.append(conclusion)

                    #todo: afficher nbr regle  appliquee
                    infere = CTkLabel(master=scrollable_frame2,text=f"==>(appliquer R{reglesCopy.index(regle) + 1})",font=("Helvetica", 17,"bold"))
                    infere.pack_configure(padx=12, pady=12,anchor="center")

                    #todo: afficher list des conflit
                    conflitaff = CTkLabel(master=scrollable_frame2, text="LIST DES CONFLITS :",font=("Helvetica",17,"bold"))
                    conflitaff.pack_configure(padx=12,pady=14,anchor="center")
                    for r in conflit:
                        listConflit = CTkLabel(master=scrollable_frame2, text=f"R = {r}",font=("Helvetica",15),fg_color="blue")
                        listConflit.pack_configure(padx=12, pady=16,anchor="center")

                    LDP.remove(nv_but) #todo-> supprimer le conclusion precedent pour prouver
                    for p in reversed(premisses):
                        LDP.insert(0,p)

                    #todo: afficher LDP :
                    ldpAff = CTkLabel(master=scrollable_frame2, text=f"LIST LDP : {LDP}",font=('Helvetica', 22),fg_color="green")
                    ldpAff.pack_configure(padx=12,pady=18,anchor="center")

                    regles.remove(regles[regles.index(regle)])

                #add a separator
                separator = CTkLabel(scrollable_frame2, height=0.5,text="", fg_color="gray")
                separator.pack(fill="x", padx=25)  #horizontal

            historique.update({f"{i}":[regles, LDPcopy,nv_but, newGoalTable, conflit, list_des_conclusion_deja_prouve,i, base_des_faits,historique]})
            i += 1
            if len(LDP) != 0:
                # #todo: afficher le nv but pour prouver
                # butaff = CTkLabel(master=scrollable_frame2, text=f"Le nouveau But a prouver => [ {nv_but} ]", font=('Helvetica', 24),bg_color="yellow",fg_color="black")
                # butaff.pack_configure(padx=12,pady=12,anchor="center")
                nv_but = LDP[0]
            else:
                break

        if len(LDP) == 0:
            #todo: afficher l'arret :
            infere1 = CTkLabel(master=scrollable_frame2,text=f"===> Arret De MI, --> Le But [{BUT}] est Prouvee <====", font=('Helvetica', 22),bg_color="green")
            infere1.pack_configure(padx=16, pady=22,anchor="center")

        if echec:
            #todo: afficher l'arret dans le cycle
            arret= CTkLabel(master=scrollable_frame2,text=f"-----> Allez au Cycle Precedent N-[{i - 1}] Puis essayez tout les cas du Conflit <---- ", font=('Helvetica', 22),bg_color="red")
            arret.pack_configure(padx=20, pady=15,anchor="center")

            chainage_arr(*last_cycle) # passer le tableau "last_cycle" comme paramatre


    chainage_arr(regles, LDP,nv_but, newGoalTable, conflit, list_des_conclusion_deja_prouve,i,base_des_faits,historique)
    fenAr.mainloop()




# -----------------------------------------------------------------------------------------
t3 = CTkLabel(master=app1, text="Choisir Le type de Chainage :",font=("Helvetica",22))
t3.place(relx=0.1,rely=0.4,anchor="nw")

t4 = CTkButton(master=app1,text="Chainage AVANT",command=avAction,width=200,height=40,font=("Arial",20))
t4.place(relx=0.2,rely=0.5,anchor="nw")
t5 = CTkButton(master=app1, text="Chainage ARRIERE",command=arAction,width=200,height=40,font=("Arial",20))
t5.place(relx=0.5,rely=0.5,anchor="nw")


app1.mainloop()





















app1.mainloop()