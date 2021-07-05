""" Negrut Maria-Daniela 133
    Transformare din NFA in DFA si minimizare"""

f = open("date.in", 'r')
g = open("date.out", 'w')
h = open("verificare.txt", 'w')


def checkChei(dictionare, cheie):
    """

    :param dictionare:
    :param cheie:
    :return: indexul dictionarului in care se afla cheia sau False daca nu e in niciunul
    """
    for idx in range(len(dictionare)):
        if cheie in dictionare[idx]:
            return idx
    return False


def getFormula(stari):
    """

    :param stari:
    :return: un string cu starea formata din combinarea starilor din lista data cu '-' intre ele
    """
    auxstari = sorted(stari)
    formula = "".join(auxstari[i] + '-' for i in range(len(stari)))
    formula = formula[:-1]
    return formula


def getStari(formula):
    """

    :param formula:
    :return:
    """
    global stari
    lista_nod_formula = str(formula).split('-')
    lista_litere = []
    aux_rez = {} # nod : {litera: nod}

    for nod in lista_nod_formula: # trec prin nodurile din care e formata formula
        nod_tranz = stari[str(nod)] # ii preiau tranzitiile
        for dic_lit in nod_tranz:
            for litera in dic_lit: # iau cheia = litera tranzitiei
                if litera not in lista_litere: # daca nu am mai dat de litera asta pana acum
                    lista_litere.append(litera) # o adaug
                    aux_rez.update({litera: [nod_Aux for nod_Aux in dic_lit[litera]]}) # adaug drept cheie litera si item un set din starile in care merge
                    # print("updated", aux_rez) #DEBUG
                else: # am dat deja de aceasta litera => trebuie sa updatez ce am deja
                    for stare in dic_lit[litera]: # trec prin starile in care ajung cu litera
                        if stare not in aux_rez[litera]: # daca am dat de o stare pe care nu o stiu
                            aux_rez[litera].append(stare) # o adaug la set
                    aux_rez[litera] = sorted(aux_rez[litera]) # sortez set-ul alfabetic

    rez = []
    for cheie_dic in aux_rez:
        rez.append({cheie_dic: [getFormula(list(aux_rez[cheie_dic]))]})
        # separ aux_rez in dictionare pt fiecare litera doar pt ca asa e formatat
        # combin starile din set intr-una singura = numele stari dat prin getFormula
    # print("rez", rez) # DEBUG

    return rez


def seeFinal(formula):
    """
    :param formula: de forma 'x-y-z' cu x, y, z  stari ale automatului
    :return: True/False daca formula contine o stare finala din DFA initial
    """
    global F
    lista_nod_formula = str(formula).split('-')
    for nod in lista_nod_formula:
        if nod in F:
            return True
    return False


def solveTrans(stare, index_stare):
    global stariDFA, finaleDFA
    dic_st_c = stariDFA[stare]  # dictionarul de tranzitii al starii curente
    # print("sunt la starea", stare, "din DFA cu ", dic_st_c) #DEBUG
    stari_posibile = {}
    for dic_lit in dic_st_c:  # trec prin tranzitii
        for litera in dic_lit:  # iau litera tranzitiei
            if litera not in stari_posibile:  # daca nu am dat de litera deja
                stari_posibile.update(
                    {litera: [getFormula(dic_lit[litera])]})  # o adaug cu item formula din starile in care ajunge
            else:  # am dat deja de litera => updatez ce stiu deja
                stari_posibile[litera].append(getFormula(dic_lit[litera]))  # adaug formula la lista de stari unde ajung
    # print("stari pos", stari_posibile) #DEBUG

    for litera in stari_posibile:
        for st in stari_posibile[litera]:  # trec prin starile in care ajung prin litera
            if st not in stariDFA:  # am gasit stare noua
                if seeFinal(st) is True:  # verific daca in compozitia formulei am vreo stare finala
                    finaleDFA.append(st)  # => aceasta este o noua stare finala
                aux_stariDFA = {st: getStari(st)}  # o noua stare de adaugat cu dictionarul de tranzitii corespunzator
                stariDFA.update(aux_stariDFA)
                # print("aux_stariDFA", aux_stariDFA) #DEBUG

    if index_stare + 1 < len(stariDFA):  # daca mai am de verificat stari
        starea_urmatoare = list(stariDFA.keys())[index_stare + 1]  # iau urmatoarea cheie/stare din dictionar
        solveTrans(starea_urmatoare, index_stare + 1)  # apelez din nou functia de rezolvare


def afisare(stariDFA, finaleDFA, SDFA):
    g.write("Starile obtinute sunt: ")
    for nod in sorted(stariDFA):
        g.write(nod + ' ')
    g.write("\nTranzitiile obtinute sunt: \n")
    for nod in sorted(stariDFA):
        for dic_litera in stariDFA[nod]:
            for litera in dic_litera:
                for destinatie in dic_litera[litera]:
                    g.write(nod + ' ' + destinatie + ' ' + litera + '\n')
    g.write("Starea initiala este: " + SDFA + '\n')
    g.write("Starile finale sunt: ")
    for nod in finaleDFA:
        g.write(nod + ' ')


def afisareDateinType(stariDFA, finaleDFA, S):
    nrstari = len(stariDFA)
    h.write(str(nrstari) + '\n')
    nrtranz = 0
    for nod in sorted(stariDFA):
        h.write(nod + ' ')
        nrtranz += len(stariDFA[nod])
    h.write('\n' +str(nrtranz) + '\n')
    for nod in sorted(stariDFA):
        for dic_litera in stariDFA[nod]:
            for litera in dic_litera:
                for destinatie in dic_litera[litera]:
                    h.write(nod + ' ' + destinatie + ' ' + litera + '\n')
    h.write(S + '\n')
    nrf = len(finaleDFA)
    h.write(str(nrf) + '\n')
    for nod in finaleDFA:
        h.write(nod + ' ')


def update(who, with_what, dict):
    """
    Modific in tranzitiile din dict unde apare 'who' cu 'with_what'
    :param who:
    :param with_what:
    :param dict:
    :return: None
    """
    for stare in dict: # trec prin stari
        aux_line = dict[stare] # iau linia de tranzitii
        for dic_lit in aux_line: # iau tranzitiile
            letter = list(dic_lit.keys())[0] # iau litera
            new_dic_lit_letter = [] # aux pt noua lista de noduri
            for nod in dic_lit[letter]:
                if nod == who: # am gasit de inlocuit
                    new_dic_lit_letter.append(with_what)
                else: new_dic_lit_letter.append(nod) # nu am nimic de inlocuit
            dic_lit[letter] = new_dic_lit_letter # modific dictionarul
            # merge asa pt ca dic_lit este doar un pointer la dict[stare][index]


def removeInnacesibile(stari):
    """
    Scot starile in care nu pot ajunge din nodul initial
    :param stari:
    :return:
    """
    def DFS(stare):
        global checked_stari, transformedStates
        checked_stari.append(stare)
        list_transitions = transformedStates[stare]
        for dic_lit in list_transitions:
            for litera in dic_lit:
                for nod in dic_lit[litera]:
                    if nod not in checked_stari:
                        DFS(nod)

    global replaceS, checked_stari
    checked_stari = []
    DFS(replaceS)
    aux_stari = {stare: stari[stare] for stare in checked_stari}
    return aux_stari


def removeInutile(stari):
    """
    Scot starile care duc in ele insasi
    :param stari:
    :return:
    """
    global F
    aux_stari = {}

    for stare in stari: # trec prin stari
        to_remove = True # presupun ca trebuie scoasa
        for dic_lit in stari[stare]: # iau tranzitiile
            for litera in dic_lit: # iau litera
                for nod in dic_lit[litera]: # iau starea in care ajunge
                    if nod != stare: # daca ajunge la o alta stare decat ea insasi
                        to_remove = False # inseamna ca nu o pot scoate
        if to_remove is False or stare in F: # daca nu pot scoate starea - adica si daca este stare finala
            aux_stari.update({stare: stari[stare]}) # o adaug la solutie
    return aux_stari


def initializare():
    """
    Myhill–Nerode metoda tabelului

    Generez un dictionar ce simuleaza un tabel ce tine doar jumatatea de deasupra diagonalei principale
    Cu cheile perechi stare - stare

    tabel = dictionar {cheie - expl mai sus: [lista cu nodurile din cheie, 0 sau 1 - cu expl urm]}
    1 -> nodurile sunt marcate deci necesare in DFA
    0 -> nodurile nu sunt necesare in DFA => sunt mai multe echivalente si le putem combina intr-o singura stare
    :return: tabel
    """
    global transformedStates, transformedFinal
    tabel = {}

    for stare1 in transformedStates:
        for stare2 in transformedStates:
            new = getFormula([stare1, stare2]) # generez stare1-stare2 ca sa pot sa o pun ca si cheie in dictionar
            if new not in tabel and stare2 != stare1: # daca nu am pus deja aceasta cheie si daca nu iau aceeaasi
                # stare de 2 ori
                if (stare1 in transformedFinal and stare2 not in transformedFinal) or (stare2 in transformedFinal and stare1 not in transformedFinal): # daca am una dintre ele
                    # finala si una nefinala
                    tabel.update({new: [sorted([stare1, stare2]), 1]})
                    # inseamna ca starea e marcata
                else:
                    tabel.update({new: [sorted([stare1, stare2]), 0]})
                    # altfel starea nu e marcata
    # print("tabel", tabel) #DEBUG
    return tabel


def findIndex(stare, letter):
    """

    :param stare:
    :param letter:
    :return: a cata litera este letter in dictionarul de stari sau False daca nu exista
    """
    global copystariMini
    tranz_stare = copystariMini[stare] # lista cu tranzitii din stare
    contor = 0
    for dic_lit in tranz_stare: # iau tranzitia
        if list(dic_lit.keys())[0] == letter: # daca am dat de litera
            return contor # returnez la ce pozitie am gasit-o
        contor += 1
    return False # daca nu am gasit-o returnez False


def marcaj(formula):
    global tabel, copystariMini
    if tabel[formula][1] == 1: # daca starea este marcata
        return 0
    stare1 = tabel[formula][0][0] # starea de pe 'coloana' sa spunem
    stare2 = tabel[formula][0][1] # starea de pe 'linie' sa spunem
    nr_letters_stare1 = len(copystariMini[stare1]) # nr. de tranzitii pe care le are stare1 si implicit si formula
    nr_letters_stare2 = len(copystariMini[stare2])

    if nr_letters_stare1 != nr_letters_stare2:
        tabel[formula][1] = 1
        return 1

    semafor = 0
    for index_letter in range(nr_letters_stare1): # trec prin litere
        letter = list(copystariMini[stare1][index_letter].keys())[0] # iau litera din stare1
        find_index = findIndex(stare2, letter) # verific daca exista vreo tranzitie cu litera resp din stare2
        # print("271 - marcaj", letter, index_letter, stare1, find_index, stare2)
        if find_index is not False: # daca exista
            check_stare1 = copystariMini[stare1][index_letter][letter] # starile in care duce
            # print(letter, copystariMini[stare1][index_letter]) #DEBUG
            check_stare2 = copystariMini[stare2][find_index][letter] # starile in care duce
            # print(letter, copystariMini[stare2][find_index]) #DEBUG
            aux_list = [nod for nod in check_stare1] # fac o lista cu nodurile in care duc cele 2 stari combinate
            aux_list.extend([nod for nod in check_stare2])
            # print(formula, aux_list) #DEBUG
            stare_combined = getFormula(sorted(aux_list)) # vad care este starea in care ajung
            # print(stare_combined) #DEBUG
            if stare_combined in tabel and tabel[stare_combined][1] == 1:
                # daca am gasit starea in tabel si este marcata
                tabel[formula][1] = 1 # marchez formula
                semafor = 1
                break
        else:
            tabel[formula][1] = 1 # stare1 si stare2 nu au aceeasi tranzitii -> trebuie pastrate
            semafor = 1
            break
    return semafor # returnez daca am marcat sau nu formula


def updateDic(stari_list, formula, combined):
    """

    :param stari_list:
    :param formula:
    :param combined:
    :return: dictionarul de stari si tranzitii cu starile din stari_list inlocuite cu formula
    """
    new_copy = {}

    for stare in combined: # trec prin stari
        if stare in stari_list: # daca starea trebuie inlocuita cu formula
            new_copy.update({formula: []}) # initiez
            aux_line = combined[stare] # iau linia de tranzitii a starii
            aux_dic = []
            for dic_lit in aux_line: # trec prin tranzitii
                letter = list(dic_lit.keys())[0] # iau litera
                for nod in dic_lit[letter]: # iau nodul in care duce
                    if nod in stari_list: # daca nodul este in lista de stari ce trebuie inlocuite
                        aux_dic.append({letter: [formula]}) # inlocuiesc cu formula
                    else: # daca nu pastrez tranzitia asa cum era
                        aux_dic.append({a1letter: dic_lit[a1letter] for a1letter in dic_lit})
            new_copy[formula] = aux_dic # initializez item-ul cheii
        else: # starea nu trebuie inlocuita
            new_copy.update({stare: []}) # => pot sa o pastrez ca si cheie
            aux_line = combined[stare]
            aux_dic = []
            # acelasi procedeu ca si anterior
            for dic_lit in aux_line:
                letter = list(dic_lit.keys())[0]
                for nod in dic_lit[letter]:
                    if nod in stari_list:
                        aux_dic.append({letter: [formula]})
                    else:
                        aux_dic.append({a1letter: dic_lit[a1letter] for a1letter in dic_lit})
            new_copy[stare] = aux_dic
    return new_copy


def tableFill():
    """
    Trec prin tabel cat timp mai pot sa marchez stari
    In momentul in care la o iteratie completa a starilor tabelului nu mai marchez nicio stare
    Inseamna ca ma pot opri
    :return:
    """
    global tabel
    filling = 1
    while filling != 0:
        filling = 0
        for formula in tabel.keys():
            filling += marcaj(formula)


def checkNrAppearance(stare, combined):
    """
    Verific daca stare apare in alte stari compuse din DFA ca sa pot sa le combin intr-una singura
    :param stare:
    :param combined: dictionar dfa
    :return: nr. de stari din care face parte stare, list cu starile
    """
    aux_count = 0
    aux_list = []
    for st in combined:
        if st != stare:
            if st.find(stare + '-') != -1:

                aux_count += 1
                aux_list.append(st)
    return aux_count, aux_list


def solveMin():
    """
    Folosind metoda tabelului combinam starile echivalente

    :return: starile automatului cu tranzitii, lista de stari finale
    """
    global tabel, copystariMini, transformedFinal, S
    DFA_min = {key: copystariMini[key] for key in copystariMini}

    for stare in tabel: # trec prin perechi (stare, stare)
        if tabel[stare][1] == 0: # daca nu a fost marcata
            # print("375", stare)
            DFA_min = updateDic(tabel[stare][0], stare, DFA_min) # inseamna ca trebuie combinate starile si le
            # inlocuiesc in dictionar

    # print(DFA_min) #DEBUG

    aux_counter = {} # preiau pt fiecare stare de cate ori apare in starile combinate
    # ca se le pot combina mai departe
    for stare in copystariMini:
        aux_counter.update({stare: checkNrAppearance(stare, DFA_min)})

    # print(aux_counter) #DEBUG

    final_answer = {key: DFA_min[key] for key in DFA_min} # combin starile care trebuie ca sa nu apara de ex
    # q1-q2 si q1-q3 ca si stari separate.
    # este evident ca din moment ce q1 este echivalent cu q2 si q3 si merg combinate
    # este si q2 echivalent cu q3
    for stare in aux_counter:
        if aux_counter[stare][0] != 0: # daca starea apare in mai multe perechi
            aux_l = [] # tin minte nodurile pe care va trebui sa le combin
            # print("394 - solveMin", stare, final_answer)
            for formula in aux_counter[stare][1]: # trec prin lista de stari care trebuie combinate
                # adica in care apare stare
                aux = formula # tin minte oricare dintre starile compuse
                # pt ca sunt echivalente nu conteaza
                # ca sa pot sa ii adaug aceasta linie de tranzitii coresp

                if formula in final_answer: # daca starea compusa este in starile automatului
                    final_answer.pop(formula) # o scot
                    lista_nod_formula = str(formula).split('-') # iau lista de noduri din care e formata
                    for nod in lista_nod_formula: # si le adaug la lista mare de noduri
                        if nod not in aux_l: # daca nu au aparut deja
                            aux_l.append(nod)
            aux_l = sorted(aux_l) # sortez nodurile ca sa pot sa mentin unicitatea stariilor
            # in sensul in care: q1-q2-q3 este acelasi lucru cu q2-q1-q3
            new = getFormula(aux_l) # combin starile in string
            # print(new) #DEBUG
            if new not in final_answer and new != '': # daca am dat de o stare ce trebuie adaugata
                final_answer.update({new: DFA_min[aux]}) # o adaug la stari
                # cu linia uneia dintre starile pe care le continea -> pt ca sunt echivalente nu conteaza
            for formula in aux_counter[stare][1]: # inlocuiesc in dictionar starile pe care le-am combinat
                # cu cea finala
                update(formula, new, final_answer)

    # print(final_answer) #DEBUG

    F_answer = [] # starile finale ale automatului
    for final in transformedFinal: # trec prin starile finale ale automatului initial
        for stare in final_answer: # trec prin starile auto. minimizat
            if stare.find(final) != -1 and stare not in F_answer: # daca o stare compusa este formata dintr-o stare
                # ce era finala
                F_answer.append(stare) # o adaug ca si stare finala a automatului minimizat

    # print('fans', F_answer) #DEBUG

    Sanswer = ''

    for stare in final_answer:
        if stare.find(S) != -1:
            Sanswer = stare
            break

    return final_answer, F_answer, Sanswer


stari = {} # stare: [{litera: stare}, {litera: stare}]
N = int(f.readline().strip())
aux = f.readline().strip().split()
for i in range(N):
    stari.update({aux[i]: []})
M = int(f.readline().strip())
for i in range(M):
    aux = f.readline().strip().split()
    if checkChei(stari[aux[0]], aux[2]) is False:
        stari[aux[0]].append({aux[2]: [aux[1]]})
    else:
        stari[aux[0]][checkChei(stari[aux[0]], aux[2])][aux[2]].append(aux[1])

# nod: [dictionare cu litera: [starile unde duc]]

S = f.readline().strip()
nrF = int(f.readline().strip())
F = []
aux = f.readline().strip().split()
for i in range(nrF):
    F.append(aux[i])

stariDFA = {str(S): stari[str(S)]} # pun doar starea initiala din NFA
finaleDFA = []
solveTrans(str(S), 0)  # incep rezolvarea din S
stariDFA[S] = getStari(S) # preiau dictionarul pt S
g.write("Din transformare:\n")
afisare(stariDFA, finaleDFA, S)


g.write('\n\n')

# redenumesc starile pt lizibilitate
transformedStates = {st: stariDFA[st] for st in stariDFA}
transformedFinal = []
newstates = []
replaceS = ''
# print(replacenamesDFA) #DEBUG
counter = 0
for stare in stariDFA:
    newstare = 'q' + str(counter)
    transformedStates.update({newstare: transformedStates[stare]})
    newstates.append(newstare)
    update(stare, newstare, transformedStates)
    if stare not in newstates:
        transformedStates.pop(stare)
    if stare in finaleDFA:
        transformedFinal.append(newstare)
    if stare is S:
        replaceS = newstare
    counter += 1

afisareDateinType(transformedStates, transformedFinal, replaceS)
# print(replacenamesDFA) #DEBUG
# print(replacenamesDFAF) #DEBUG


stariMini = removeInnacesibile(transformedStates)
stariMini = removeInutile(stariMini)
copystariMini = {key: stariMini[key] for key in stariMini}
tabel = initializare()
tableFill()

# print(tabel) #DEBUG
stariRaspuns, FRaspuns, SRaspuns = solveMin()

g.write("\nDin minimizare:\n")
afisare(stariRaspuns, FRaspuns, SRaspuns)
h.write('\n\n')
afisareDateinType(stariRaspuns, FRaspuns, SRaspuns)
h.write('\n\n')