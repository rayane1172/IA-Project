from customtkinter import *
from customtkinter import CTk, CTkScrollableFrame  # Assurez-vous que customtkinter est installé

app1 = CTk()
app1.geometry("800x550")
app1.title("Le mouteur d'inference")

t1 = CTkLabel(master=app1,text="Enter la base de faits separer par ','", font=("Helvetica",20))
t1.place(relx=0.05,rely=0.05,anchor="nw")
bfentry = CTkEntry(master=app1, placeholder_text="e.g: A,B,C,D....")
bfentry.place(relx=0.5,rely=0.05,anchor="nw")


t2 = CTkLabel(master=app1,text="Enter le but(Obligatoire dans le chainage Arriere)", font=("Helvetica",20))
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
    regles = [({"a","b"},"f"),({"f","h"},"i"),({"d","h","g"},"a"),({"o","g"},"h"),({"e","h"},"b"),({"g","a"},"b"),({"g","h"},"p"),({"g","h"},"q"),({"d","o","g"},"j")]
    
    # for entry in regles_entries:
    #     regle_value = entry.get() #return regle in string value
    #     if '->' in regle_value:
    #         premisses, conclusion = regle_value.split("->") #todo: returner partie gauche du regle dans premisse et partie droite du regle dans "conclusion"
    #         premisses = set(premisses.split(","))
    #         regles.append((premisses,conclusion)) # charger la list des regles

    
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
                
                for regle in conflit:
                    listConflit = CTkLabel(master=scrollable_frame, text=f"R = {regle}") 
                    listConflit.pack_configure(padx=12, pady=10,anchor="center")
                
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
                cycle = CTkLabel(master=scrollable_frame, text=f"Cycle {i}",font=("Helvetica", 17,"bold"),bg_color="green")
                cycle.pack_configure(padx=12,pady=6,anchor="center")
                i+=1
                
                #afficher list des conflit : 
                for regle in conflit:
                    conflitaff = CTkLabel(master=scrollable_frame, text=f"R = {regle}")
                    conflitaff.pack_configure(padx=12,pady=10,anchor="center")
                
                infere = CTkLabel(master=scrollable_frame,text=f"==>(Appliquer R{reglesCopy.index(regle) + 1}) En ajouter [{conclusion}] dans la base de faits <==",font=("Helvetica", 15,"bold"))
                infere.pack_configure(padx=12, pady=12,anchor="center")
                    
                nvbase = CTkLabel(master=scrollable_frame,text=f"Nouvelle base de faits {base_des_faits}",font=('Helvetica', 18))
                nvbase.pack_configure(padx=14,pady=12,anchor="center")
                
                #add a separator 
                separator = CTkLabel(scrollable_frame, height=0.5,text="", fg_color="gray")
                separator.pack(fill="x", padx=10)  #horizontal
                
                infere1 = CTkLabel(master=scrollable_frame,text=f"On trouver le BUT [{BUT}] , le mouteur d'inference s'arrete ", font=('Helvetica', 22),bg_color="green")

                infere1.pack_configure(padx=16, pady=12,anchor="center")
                ButTrouver = True #? pour quiter la boucle "while"

                break #? pour quiter la boucle "for"

    if len(conflit) == 0 and not ButTrouver:
        cycle = CTkLabel(master=scrollable_frame, text=f"Cycle {i}",font=("Helvetica", 17),bg_color="green")
        cycle.pack_configure(padx=12,pady=6,anchor="center")
        i+=1
        echec = CTkLabel(master=scrollable_frame,text=f"Le Mouteur d'inference S'Arrete, il existe pas des regles applicables !! ", font=('Helvetica', 22),bg_color="red")
        echec.pack_configure(padx=20, pady=15,anchor="center")


    fenAv.mainloop()


# def arAction():
    # pass
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
    # regles = [] # todo:list des regles e.g => (a,b)->e
    regles = [(["a","b"],"f"),(["f","h"],"i"),(["d","h","g"],"a"),(["o","g"],"h"),(["e","h"],"b"),(["g","a"],"b"),(["g","h"],"p"),(["g","h"],"q"),(["d","o","g"],"j")]

    # for entry in regles_entries:
    #     regle_value = entry.get() #return regle in string value
    #     if '->' in regle_value:
    #         premisses, conclusion = regle_value.split("->") #todo: returner partie gauche du regle dans premisse et partie droite du regle dans "conclusion"
    #         premisses = list(premisses.split(","))
    #         regles.append((premisses,conclusion)) # charger la list des regles

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
    # newGoalTable.append(nv_but)

    def chainage_arr(regles, LDP,nv_but, newGoalTable, conflit,list_des_conclusion_deja_prouve,i, base_des_faits,historique):

        echec = False

        while len(LDP) != 0:
            print("\n","-" * 100,end="\n")
            print(f"\nle cycle N'{i}".center(30,"#"))
            LDPcopy = LDP.copy() #souvgarder la valleur avant la modification
            print(f"Print le LDPcopy avant du modifier LDP orginal : {LDPcopy}")

            # oldBut = nv_but #souvgarder la valleur d'entree du but avant faire la boucle
            newGoalTable.append(nv_but)
            nv_but = newGoalTable[len(newGoalTable) - 1]

            if nv_but in base_des_faits:
                print(f"\n-> our but is : {nv_but}")
                # print(f"\n-> our old but is : {oldBut}")

                print(f"LIst LDP avant demarer : {LDP}")
                conflit = filtrage_arr(regles, nv_but)

                LDP.remove(nv_but) #todo: supprimer le but deja prouver d'apres BF

                print(f"---> But [{nv_but}] appartient aux base des faits, on le supprimer")

                print("-" * 20)
                print(f"le list LDP : {LDP}")
                print("-" * 20)

                # if len(LDP) != 0: # verifier est ce que il y a des sous-but a prouver
                #     nv_but = LDP[0]
                #     print(f"Le nouveau But a prouver => {nv_but}".center(60,"_"))
                # else:
                #     break

            elif nv_but in list_des_conclusion_deja_prouve:
                print(f"\n-> our but is : {nv_but}")
                # print(f"\n-> our old but is : {oldBut}")

                print(f"LDP avant supprimer le nv_but precedant -> {LDP}")
                conflit = filtrage_arr(regles, nv_but)
                print(f"Nv-BUt value is : {nv_but}")

                LDP.remove(nv_but) #todo: supprimer le but deja prouver et remplacer par ces premisse
                print(f"---> list des conclusion deja prouve est ==> {list_des_conclusion_deja_prouve}")
                print(f"---> But [{nv_but}] deja prouver dans les cycles precedent")
                print(f"List LDP est : {LDP}",end="\n\n")

                # if len(LDP) != 0:
                #     nv_but = LDP[0]
                #     print(f"Le nouveau But a prouver => {nv_but}".center(60,"_"))
                # else:
                #     break

            else: # else n'est pas prouver precedament
                print(f"\n-> our but is : {nv_but}")
                conflit = filtrage_arr(regles, nv_but)

                if not conflit: # pas de conflit (None)
                    print(f"mon nv_but value is  --------> {nv_but}")
                    # print(f"List LDP dans (if non conflit) : {LDP}")
                    print(f"Je Bloquer de le cycle {i}")
                    print(f"i block with LDP -> {LDP}")
                    echec = True

                    # newGoalTable.remove(newGoalTable[len(newGoalTable) - 1 ]) #todo: supprimer le but precedent qui n'est pas utiliser autrefois

                    del newGoalTable[-1] #supprimer dernier but que n'est pas utiliser (comme "e" dans l'ex)
                    print(f"new goal table is : {newGoalTable}")

                    nv_but = newGoalTable[len(newGoalTable) - 1]
                    print(f"********** = le nv_but value when we break with no conflit => : {nv_but}")

                    # beforeLastCycleLIST_PROUVER = historique[f"{i-2}"][5]
                    historique[f"{i-2}"][5].pop() #todo :supprimer la dern valleur du list des conclusion deja prouve pour retester

                    # print(f"before last cyce -------> {beforeLastCycleLIST_PROUVER}")

                    # list_des_conclusion_deja_prouve.remove(len(list_des_conclusion_deja_prouve) - 1)

                    global last_cycle
                    last_cycle = historique[f"{i-1}"]
                    print(f"-------------------------------------------------------> L'indice pour last_cycle est : >>>>>>> {i-1}")
                    break
                    # chainage_arr(*last_cycle) # passer le tableau "last_cycle" comme paramatre
                else:
                    regle = find_regle(conflit)
                    premisses, conclusion = regle

                    list_des_conclusion_deja_prouve.append(conclusion)

                    print(f"==>(appliquer R{reglesCopy.index(regle) + 1})")

                    print(f"List des conflit is : \n{conflit}")

                    LDP.remove(nv_but) # supprimer le conclusion precedent
                    for p in reversed(premisses):
                        LDP.insert(0,p)

                    # nv_but = LDP[0]

                    print("-" * 20)
                    print(f"le list LDP : {LDP}")
                    print("-" * 20)

                    regles.remove(regles[regles.index(regle)])

                    print(f"\nnew goal table is : {newGoalTable}\n")


            historique.update({f"{i}":[regles, LDPcopy,nv_but, newGoalTable, conflit, list_des_conclusion_deja_prouve,i, base_des_faits,historique]})
            i += 1

            if len(LDP) != 0:
                nv_but = LDP[0]
                print(f"Le nouveau But a prouver => {nv_but}".center(60,"_"))
            else:
                break

        # print("-" * 50)
        # print(f"list LDP donnees  : {last_cycle[1]}")
        # print(f"stop in cycle { last_cycle[0]}\n\n ",end="\n\n")
        # print(f" regles with length : { len(regles)}")
        # print("-" * 50)

        if len(LDP) == 0:
            print("-" * 50)
            print(f"==========> Arret De MI, --> Le But [{BUT}] est Prouvee <=======")
            print("-" * 50)

        if echec:
            print("\n","!" * 50)
            print("-----> Allez en Les cycles Precedent Puis essaye tout les cas du Conflit <---- ")
            print("!" * 50,end="\n\n")
            print(f"apres le break le nv but is   -> {nv_but}")
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