import tkinter as t 
from tkinter import ttk


fen = t.Tk()
fen.title("Le moteur d'inference ")
fen.geometry("500x300")

t1 = t.Label(fen,text="Enter la base de faits separer par ',' => a,x,....", font=('Helvetica', 10))
t1.place(x = 10, y = 20)
bfentry = t.Entry(fen)
bfentry.place(x = 300,y = 25)

bt = t.Label(fen,text="Enter le but(Obligatoire dans le chainage Arriere)", font=('Helvetica', 8))
bt.place(x=10,y=90)
btEntry =t.Entry(fen) 
btEntry.place(x=250,y=90)
global BUT

def avAction():
    BUT =btEntry.get() #todo: retourner la valeur 'str' du but entree par user
    fenAV = t.Tk() # ajouter un nv fenetre pour chainage avant
    fenAV.title("Chainage Avant")
    fenAV.geometry("800x800")
    
    #create main frame:
    main_frame = t.Frame(fenAV)
    main_frame.pack(fill="both",expand=1)
    
    #create a canvas:
    my_canvas =t.Canvas(main_frame)
    my_canvas.pack(side="left",fill="both",expand=1)
    
    #add a scrollbar to the canvas:
    my_scrollbar =ttk.Scrollbar(main_frame, orient="vertical",command=my_canvas.yview)
    my_scrollbar.pack(side="right", fill="y")
    
    #configure the canvas:
    my_canvas.configure(yscrollcommand=my_scrollbar.set)
    my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion= my_canvas.bbox("all")))
    #create another frame inside
    second_frame = t.Frame(my_canvas)
    #add that new frame to a window in the canvas:
    my_canvas.create_window((0,0),window=second_frame,anchor="nw")
    
    
    
    regle = t.Label(second_frame,text="Enter les regles comme ca (a,x->y,z....) ", font=('Helvetica', 14))
    regle.pack(padx=10, pady=20, anchor='w')
    
    regles_entries = [] 
    def ajouter_regle():
        entry = t.Entry(second_frame)
        entry.pack(padx=10, pady=2)
        regles_entries.append(entry) # retourner une list des valeur d'entrees de l'utilisateur
        

    def demarer_chainage_avant():
        def grandNbrPremisse(LRD): #? fonction pour trouver la regle du plus nombre des premisses
            maxLenPremisse = 0
            for regle in LRD:
                premisse, conclusion = regle
                if maxLenPremisse < len(premisse):
                    maxLenPremisse = len(premisse)
                    index = LRD.index(regle)
            return index #? retourner la position du la regle ayant le plus de premisses
        
        #? Masquer chaque place d'ecriture apres l'execution du ch avant
        # for r in regles_entries:
        #     r.pack_forget()
        
        base_des_faits = set(bfentry.get().split(","))  # placer la base des faits dans un 'set'
        
        global regles 
        regles = [] # todo:list des regles e.g => (a,b)->e
        
        regles = [({"a","b"},"f"),({"f","h"},"i"),({"d","h","g"},"a"),({"o","g"},"h"),({"e","h"},"b"),({"g","a"},"b"),({"g","h"},"p"),({"g","h"},"q"),({"d","o","g"},"j")]
        # for entry in regles_entries:
        #     regle_value = entry.get() #return regle in string value
        #     if '->' in regle_value:
        #         premisses, conclusion = regle_value.split("->") #todo: returner partie gauche du regle dans premisse et partie droite du regle dans "conclusion"
        #         premisses = set(premisses.split(","))
        #         regles.append((premisses,conclusion)) # charger la list des regles
                
                
        reglesCopy = regles.copy() #? un copie des regles utiliser pour indexer les regles appliquer
        
        LRD = filtrage(regles, base_des_faits) #? LRD: list des regles applicables
        ButTrouver = False

        #? tanque la list des regles applicable n'est pas vide 
        while len(LRD) != 0 and ButTrouver == False:
            for regle in LRD:
                premisse, conclusion = regle
                
                indice = grandNbrPremisse(LRD) #trouver l'indice du du regle de plus des premisse 
                if LRD[indice] != LRD[LRD.index(regle)]: continue # en passer tout les regles du la boucle "for" , jusqu'a trouver la regle ayant le plus nombre des premisses
                if conclusion != BUT:
                    base_des_faits.add(conclusion)
                    infere = t.Label(second_frame,text=f"==>(appliquer R{reglesCopy.index(regle) + 1}) En ajouter [{conclusion}] dans la base de faits <==",    font=('Helvetica', 14))
                    infere.pack(padx=12, pady=12)
                    
                    nvbase = t.Label(second_frame,text=f"Nouvelle base de faits {base_des_faits}", font=('Helvetica', 15),bg="white").pack(padx=14,pady=12)
                    
                    regles.remove(regles[regles.index(regle)]) 
                    #? supprimer la regle apres l'application
                    
                    LRD = filtrage(regles, base_des_faits)
                    
                else: # ?dans le cas du trouver le but 
                    base_des_faits.add(conclusion)  #? ajouter le but dans la bf et quitez l'operation
                    infere = t.Label(second_frame,text=f"==>(appliquer R{reglesCopy.index(regle) + 1}) En ajouter [{conclusion}] dans la base de faits <==",    font=('Helvetica', 14))
                    infere.pack(padx=12, pady=12)
                    
                    nvbase = t.Label(second_frame,text=f"Nouvelle base de faits {base_des_faits}", font=('Helvetica', 15),bg="white").pack(padx=14,pady=12)
                    
                    infere1 = t.Label(second_frame,text=f"On trouver le BUT [{BUT}] , le mouteur d'inference s'arrete ", font=('Helvetica', 12),fg="white",bg='blue')
                    
                    infere1.pack(padx=16, pady=12)
                    ButTrouver = True #? pour quiter la boucle "while"
                    
                    break #? pour quiter la boucle "for"
        
        if len(LRD) == 0 and not ButTrouver:
            echec = t.Label(second_frame,text=f"le mouteur d'inference s'arrete, il existe pas des regles applicables !! ", font=('Helvetica', 12),fg="white",bg="red") 
            echec.pack(padx=20, pady=15)
        
    def filtrage(regles,base_des_faits):
        LRD = [] #list des regles applicable
        for premisse,conclusion in regles:
            if premisse.issubset(base_des_faits) and conclusion not in base_des_faits:
                LRD.append((premisse,conclusion))
        return LRD
    
    t.Button(second_frame, text="Ajouter une règle", command=ajouter_regle).pack(padx=10, pady=5)
    t.Button(second_frame,text="Démarrer le chaînage avant", command=demarer_chainage_avant).pack(padx=10, pady=10)



def arAction():
    # BUT =btEntry.get() #todo: retourner la valeur 'str' du but entree par user
    # print("wait for testing")
    fenAr = t.Tk() # ajouter un nv fenetre pour chainage avant
    fenAr.title("Chainage Arriere")
    fenAr.geometry("500x250")
    
    def irrevocable():
        pass        
    def parTentative():
        pass
    
    
    
    
    
    choix = t.Label(fenAr,text="Choisir le type de Chainage Arriere :", font=('Helvetica', 22),fg="white",bg='red')
    choix.place(x=10, y=25)
    btn1= t.Button(fenAr,text='regime irrevocable',command=irrevocable,font=('Helvetica',14))
    btn1.place(x=50, y=150)
    btn2 = t.Button(fenAr,text='regime par tentative',command=parTentative,font=('Helvetica',14))
    btn2.place(x=240, y=150)


choix = t.Label(fen,text="Choisir le type de Chainage :", font=('Helvetica', 22),fg="white",bg='blue')
choix.place(x=10, y=125)
ChainageAvantBtn = t.Button(fen,text='Chainage Avant',command=avAction,font=('Helvetica',14))
ChainageAvantBtn.place(x=50, y=200)
ChainageArrBtn = t.Button(fen,text='Chainage Arriere',command=arAction,font=('Helvetica',14))
ChainageArrBtn.place(x=240, y=200)



fen.mainloop()