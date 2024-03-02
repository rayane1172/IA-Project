import tkinter as t 
#* en utiliser la bib tkinter,=> integrer automatiquement dans python 

fen = t.Tk()
fen.title("Le moteur d'inference ")
fen.geometry("500x300")

t1 = t.Label(fen,text="Enter la base de faits separer par ',' => a,x,....", font=('Helvetica', 10))
t1.place(x = 10, y = 20)
bfentry = t.Entry(fen)
bfentry.place(x = 300,y = 25)

bt = t.Label(fen,text="Enter le but", font=('Helvetica', 10))
bt.place(x=10,y=90)
btEntry =t.Entry(fen) 
btEntry.place(x=250,y=90)
global BUT

def avAction():
    BUT =btEntry.get() #todo: retourner la valeur 'str' du but entree par user
    fenAV = t.Toplevel() # ajouter un nv fenetre pour chainage avant
    fenAV.title("Chainage Avant")
    fenAV.geometry("800x800")
    regle = t.Label(fenAV,text="Enter les regles comme ca (a,x->y,z....) ", font=('Helvetica', 14))
    regle.pack(padx=10, pady=20)
    
    regles_entries = [] 
    def ajouter_regle():
        entry = t.Entry(fenAV)
        entry.pack(padx=10, pady=2)
        regles_entries.append(entry) # retourner une list des valeur d'entrees de l'utilisateur
        

    def demarer_chainage_avant():
        #todo: Masquer chaque place d'ecriture
        for r in regles_entries:
            r.pack_forget()
        
        base_des_faits = set(bfentry.get().split(","))  # placer la base des faits dans un 'set'
        global regles 
        regles = [] # list des regles e.g => (a,b)->e
        for entry in regles_entries:
            regle_value = entry.get() #return regle in string value
            if '->' in regle_value:
                premisses, conclusion = regle_value.split("->") # returner partie gauche du regle dans premisse et partie droite du regle dans "conclusion"
                premisses = set(premisses.split(","))
                regles.append((premisses,conclusion)) # charger la list des regles
        reglesCopy = regles.copy() #todo: un copie utiliser pour indexer les regles appliquer
        
        LRD = filtrage(regles, base_des_faits) #LRD: list des regles applicables
        ButTrouver = False
        def grandPremisse(LRD):
            maxLenPremisse = 0
            for regle in LRD:
                premisse, conclusion = regle
                if maxLenPremisse < len(premisse):
                    maxLenPremisse = len(premisse)
                    index = LRD.index(regle)
            return index #todo: retourner la position du la regle ayant le plus de premisses
        i = 0
        while len(LRD) != 0 and ButTrouver == False:
            for regle in LRD:
                
                # i=grandPremisse(LRD)
                # if LRD[i] != regle: continue 
                # #todo: passer les autres regle, jusqu'a ont trouver la regle specifique (le plus de premisses)
                premisse, conclusion = regle
                # if conclusion != BUT and LRD[i] == regle:
                if conclusion != BUT:
                    base_des_faits.add(conclusion)
                    infere = t.Label(fenAV,text=f"==>(appliquer R{reglesCopy.index(regle) + 1}) En ajouter [{conclusion}] dans la base de faits <==",    font=('Helvetica', 12))
                    infere.pack(padx=12, pady=12)
                    nvbase = t.Label(fenAV,text=f"Nouvelle base de faits {base_des_faits}", font=('Helvetica', 10)).pack(padx=14,pady=12)
                    
                    regles.remove(regles[regles.index(regle)]) 
                    #todo: supprimer la regle apres l'application
                else:
                    infere1 = t.Label(fenAV,text=f"On trouver le BUT [{BUT}] , le mouteur d'inference s'arrete ", font=('Helvetica', 12),fg="white",bg='red')
                    infere1.pack(padx=16, pady=12)
                    ButTrouver = True # pour quiter la boucle "while"
                    break #pour quiter la boucle "for"

            LRD = filtrage(regles, base_des_faits)
            if len(LRD) == 0:
                echec = t.Label(fenAV,text=f"le mouteur d'inference s'arrete, il existe pas des regles applicables !! ", font=('Helvetica', 12)) 
                echec.pack(padx=20, pady=15)
        
    def filtrage(regles,base_des_faits):
        LRD = []
        for premisse,conclusion in regles:
            if premisse.issubset(base_des_faits) and conclusion not in base_des_faits:
                LRD.append((premisse,conclusion))
        return LRD
    
    t.Button(fenAV, text="Ajouter une règle", command=ajouter_regle).pack(padx=10, pady=5)
    t.Button(fenAV,text="Démarrer le chaînage avant", command=demarer_chainage_avant).pack(padx=10, pady=10)



def arAction():
    # BUT =btEntry.get() #todo: retourner la valeur 'str' du but entree par user
    print("wait for finishing")


choix = t.Label(fen,text="Choisir le type de Chainage :", font=('Helvetica', 22),fg="white",bg='blue')
choix.place(x=10, y=125)
ChainageAvantBtn = t.Button(fen,text='Chainage Avant',command=avAction,font=('Helvetica',14))
ChainageAvantBtn.place(x=50, y=200)
ChainageArrBtn = t.Button(fen,text='Chainage Arriere',command=arAction,font=('Helvetica',14))
ChainageArrBtn.place(x=240, y=200)



fen.mainloop()