def calcular_tabela_xp():
    tabela = [0]
    for nivel in range(2,21):
        tabela.append((nivel-1)*1000 + tabela[-1])
    return tuple(tabela)

TABELA_XP = calcular_tabela_xp()