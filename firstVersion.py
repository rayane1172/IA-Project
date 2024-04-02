import tkinter as tk


fen =tk.Tk()
fen.title("Chainage Avant et Arriere")
fen.geometry("500x300")


bf = tk.Label(fen,text="Enter la base de faits separer par ',' => a,x,....", font=('Helvetica', 10))
bf.place(x = 10,y=20)

bfEntry =tk.Entry(fen) 
bfEntry.place(x = 300,y =25)

bt = tk.Label(fen,text="Enter le but", font=('Helvetica', 10))
bt.place(x=10,y=90)
btEntry =tk.Entry(fen) 
btEntry.place(x=250,y=90)

but =btEntry.get()

def avAction():
    fenAV = tk.Toplevel()
    fenAV.title("Chainage Avant")
    fenAV.geometry("800x800")

    regle = tk.Label(fenAV,text="Enter les regles comme ca (a,x->y,z....) ", font=('Helvetica', 14))
    regle.pack(padx=10,pady=20)
    
    regles_entries = []
    def ajouter_regle():
        entry = tk.Entry(fenAV)
        entry.pack(padx=10,pady=5)
        regles_entries.append(entry)
        
    
    def demarrer_chainage_avant():
        base_des_faits = set(bfEntry.get().split(","))
        
        regles = []
        for entry in regles_entries:
            regle_txt = entry.get()
            
            if '->' in regle_txt:
                premisses ,conclusion = regle_txt.split('->')
                premisses = set(premisses.split(","))
                
                regles.append((premisses,conclusion))
        
        # while True:
            if but not in base_des_faits:
                nouvelle_base = chainage_avant(base_des_faits, regles,but)
                nvbase = tk.Label(fenAV,text=f"nouvelle base de faits {nouvelle_base}", font=('Helvetica', 10)).pack(padx=10,pady=12)
                base_des_faits = nouvelle_base
            else:
                infere = tk.Label(fenAV,text=f"On trouver le but , le mouteur d'inference s'arrete ", font=('Helvetica', 12))
                infere.pack(padx=16, pady=12)
                break
            
            
        # print(regles)
    
    
    def chainage_avant(base_des_faits,regles,but):
        nouveaux_faits = True
        while nouveaux_faits:
            nouveaux_faits = False
            
            for premisses,conclusion in regles:
                
                    if premisses.issubset(base_des_faits) and conclusion not in base_des_faits:
                        nouveaux_faits = True
                        
                        if conclusion != but:
                            base_des_faits.add(conclusion)
                            infere = tk.Label(fenAV,text=f"en ajouter [{conclusion}] dans la base de faits",    font=('Helvetica', 12))
                            infere.pack(padx=10,pady=12)
                        
                        else: # quand je trouve  le but attendre le mouteur 
                            infere = tk.Label(fenAV,text=f"On trouver le but , le mouteur d'inference s'arrete ", font=('Helvetica', 12))
                            infere.pack(padx=16, pady=12)
                            
                            nouveaux_faits = False #pour bloquer la boucle while nv faits
                            break
                    # regles.remove((f'({premisses},{conclusion})'))
        return base_des_faits



    tk.Button(fenAV, text="Ajouter une règle", command=ajouter_regle).pack(padx=10, pady=5)
    tk.Button(fenAV,text="Démarrer le chaînage avant", command=demarrer_chainage_avant).pack(padx=10, pady=10)


    fenAV.mainloop()


def arAction():
    print("hi")






choix = tk.Label(fen,text="Choisir le type de Chainage :", font=('Helvetica', 22),fg="white",bg='blue')
choix.place(x=10,y=125)
ChainageAvantBtn = tk.Button(fen,text='Chainage Avant',command=avAction,font=('Helvetica',14))
ChainageAvantBtn.place(x=50,y=200)
ChainageArrBtn = tk.Button(fen,text='Chainage Arriere',command=arAction,font=('Helvetica',14))
ChainageArrBtn.place(x=240,y=200)


fen.mainloop()