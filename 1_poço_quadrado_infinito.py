#Poço quadrado infinito

---

## Requisitos do Código
Primeiramente, vamos falar das bibliotecas, que são essênciais para o bom funcionamento do código! Nessa simulação, vamos utilizar três:
- numpy
- matplotlib.pyplot
- ipywidgets

Elas são utilizadas para cálculos matemáticos, construções gráficas e criação de interfaces interativas, respectivamente. Com esse conhecimento, podemos partir para o código em si!

**NÃO SE ESQUEÇA DOS DESAFIOS PARA TREINAR APÓS O CÓDIGO!!**

---

## Potencial e Função de onda
O ponto chave desta simulação é a nossa função de onda, que nada mais é do que uma solução da Equação de Schrodinger para o seguinte potencial:

$$
V(x) =
\begin{cases}
0, & 0 < x < a \\\\
\infty, & \text{caso contrário}
\end{cases}
$$

Após realizarmos os cálculos da equação de Schrodinger (Em breve iremos inserir aqui, enquanto isso você pode consultar o livro de referência (páginas 22-28) ou qualquer livro de sua escolha) chegamos na seguinte função de onda solução (já normalizada):

$$
\psi_n(x) =
\begin{cases}
\sqrt{\dfrac{2}{a}} \sin\left(\dfrac{n\pi x}{a}\right), & 0 < x < a \\\\
0, & \text{caso contrário}
\end{cases}
$$

Como "fora do poço" a nossa função de onda deve ser zero pelas condições de normalização, os parâmetros que vão nos interessar aqui serão "n" e "a", o **número quântico** e a **largura do poço**! É através deles que iremos mudar os gráficos em tempo real e ver os resultados!

---

## Quantização da Energia

Dada a solução, descobrimos que a Energia dos estados estacionários tem de ser quantizada para satisfazer as condições de contorno do problema! Assim, chegamos em na seguinte fórmula:

$$
E_n = \frac{n^2 \pi^2 \hbar^2}{2 m a^2}, \quad n = 1, 2, 3, \dots
$$

Fisicamente, isso diz que a função de onda só pode assumir certos valores discretos, **e não nulos**, já que isso faria a função não ser normalizável (pois seria constante e nula). Quanto maior o "n", maior a energia, tornando nossa função mais ondulada! (Importante ressaltar que esse fenômeno de quantização só ocorre em um confinamento quântico devido as regras de ressonância do sistema).

---

## Aplicações
Mesmo sendo um conceito introdutório de mecânica quântica, ele serve de base para estudarmos modelos avançados (como o poço finito) e em aplicações que utilizamos no dia a dia!

O exemplo mais conhecido são os **LED's**! Imagine dois materiais semicondutores, sendo um deles com energia de banda maior que o outro. Ao colocar um pedaço muito fino do material com menor energia entre duas partes do que possui maior energia, criamos um confinamento dos elétrons naquela região, **como se estivem entre duas barreiras!** Através desse confinamento, podemos alterar a largura do "poço" criado para mudarmos a frequência emitida, mudando diretamente seus **estados de energia quantizados!!** É graças a esse conhecimento e tecnologia que podemos criar luzes LED de várias cores!

---

## Conclusão

Finalizando, plotamos também a densidade de probabilidade da nossa função, para vermos o local que tem mais chance de conter a partícula! As linhas verticais e a área vermelha representam as "bordas" e a área proíbida, respectivamente. Segue uma legenda de cores do gráfico:

Azul - Nível de energia atual

Verde claro - Níveis sucessores e antecessores de energia

Roxo - Função de onda

Amarelo - Densidade de probabilidade da função de onda

Rosa/Vermelho Claro - Local de potencial infinito

---

##Código
"""

!pip install -q ipywidgets

#Bibliotecas utilizadas
import numpy as np
import matplotlib.pyplot as plt
from ipywidgets import interact, IntSlider, FloatSlider, Dropdown

#Constantes em unidades naturais, para simplificar cálculos
hbar = 1.0
m = 1.0

#Definição da Função de Psi com condições de contorno
def psi_n(x, n, a):
    psi = np.sqrt(2/a) * np.sin(n * np.pi * x / a)
    psi[(x < 0) | (x > a)] = 0
    return psi

#Definição da função de Energia Quantizada
def energia(ns, a):
    return (ns**2 * np.pi**2 * hbar**2) / (2 * m * a**2)

#Definição da função do Poço
def plot_poco_multienergia(n=1, a=1.0, viz='ψ(x)', Nx=1000):
    Nlevels = 5
    x = np.linspace(-0.1, a + 0.1, Nx)

#Função de onda do nível, em destaque
    psi = psi_n(x, n, a)

#Índices de 1 a 5 e suas energias
    ns = np.arange(1, Nlevels + 1)
    Es = energia(ns, a)

#Exibição dos níveis vizinhos
    idx = n - 1
    prev_idx = idx - 1 if idx > 0 else None
    next_idx = idx + 1 if idx < Nlevels - 1 else None
    prev_level = Es[prev_idx] if prev_idx is not None else None
    next_level = Es[next_idx] if next_idx is not None else None
    En = Es[idx]

#Cálculo da diferença de energia entre os níveis
    if next_level is not None:
        dE = next_level - En
    elif prev_level is not None:
        dE = En - prev_level
    else:
        dE = En

#Subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 5))

#Regiões proibidas em vermelho
    ax1.axvspan(x.min(), 0, color='red', alpha=0.2)
    ax1.axvspan(a, x.max(), color='red', alpha=0.2)

#Energia anterior em verde
    if prev_level is not None:
        ax1.hlines(prev_level, 0, a, colors='green', linestyles='-.', alpha=0.9, linewidth=2,
                   label=f'$E_{{{n-1}}}$ (anterior)')

#Energia posterior em verde
    if next_level is not None:
        ax1.hlines(next_level, 0, a, colors='green', linestyles='-.', alpha=0.9, linewidth=2,
                   label=f'$E_{{{n+1}}}$ (próximo)')

#Energia atual em azul
    ax1.hlines(En, 0, a, color='blue', linestyle='-', linewidth=2.5,
               label=f'$E_{{{n}}} = {En:.2f}$')

#Plot de ψ e/ou densidade para o nível n
    if viz in ['ψ(x)', 'Ambos']:
        scale_psi = 0.6 * dE / np.max(np.abs(psi)) if np.max(np.abs(psi)) > 0 else 1
        y_psi = psi * scale_psi + En
        ax1.plot(x, y_psi, color='purple', linewidth=2, label=f'$\\psi_{{{n}}}(x)$')
    if viz in ['|ψ(x)|^2', 'Ambos']:
        dens = psi ** 2
        scale_dens = 0.6 * dE / np.max(dens) if np.max(dens) > 0 else 1
        y_dens = dens * scale_dens + En
        ax1.plot(x, y_dens, color='orange', linewidth=2, label=f'$|\\psi_{{{n}}}(x)|^2$')

#Ajuste de limites gráficos
    y_min = En - 1.2 * dE
    y_max = En + 1.2 * dE
    ax1.set_ylim(y_min, y_max)
    ax1.set_xlim(-0.1, a + 0.1)
    ax1.set_xlabel('x')
    ax1.set_ylabel('Amplitude + Energia')
    ax1.set_title(f'Poço Infinito (n={n}, a={a:.1f})')
    ax1.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    ax1.grid(True)

#Região proibida do gráfico estático
    ax2.axvspan(x.min(), 0, color='red', alpha=0.2)       # região proibida x<0
    ax2.axvspan(a, x.max(), color='red', alpha=0.2)       # região proibida x>a

#Recriar a função de onda e densidade de prob. de cada nível i (1 a 5)
    for i, Ei in zip(ns, Es):
        psi_i = psi_n(x, i, a)
        dens_i = psi_i ** 2

#Cálculo ΔE_i para escalonar essa função
        if i < Nlevels:
            dE_i = Es[i] - Ei            # E_{i+1} - E_i
        else:
            dE_i = Ei - Es[i - 2]        # (último caso) E_i - E_{i-1}

#Escalonar ψ_i em roxo
        scale_psi_i = 0.6 * dE_i / np.max(np.abs(psi_i)) if np.max(np.abs(psi_i)) > 0 else 1
        y_psi_i = psi_i * scale_psi_i + Ei
        ax2.plot(x, y_psi_i, color='purple', linewidth=1)

#Escalonar dens_i em amarelo
        scale_dens_i = 0.6 * dE_i / np.max(dens_i) if np.max(dens_i) > 0 else 1
        y_dens_i = dens_i * scale_dens_i + Ei
        ax2.plot(x, y_dens_i, color='gold', linewidth=1)


#Ajustes no gráfico fixo
    menor_espaco = Es[1] - Es[0]
    maior_espaco = Es[-1] - Es[-2]
    ax2.set_ylim(Es[0] - 1.2 * menor_espaco, Es[-1] + 1.2 * maior_espaco)
    ax2.set_xlim(-0.1, a + 0.1)
    ax2.set_xlabel('x')
    ax2.set_ylabel('Amplitude + Energia')
    ax2.set_title('Níveis 1 a 5: ψ em roxo e |ψ|² em amarelo')
    ax2.grid(True)

    plt.tight_layout()
    plt.show()

#Interatividade
interact(
    plot_poco_multienergia,
    n=IntSlider(value=1, min=1, max=5, step=1, description='n'),
    a=FloatSlider(value=1.0, min=0.5, max=5.0, step=0.1, description='a'),
    viz=Dropdown(options=['ψ(x)', '|ψ(x)|^2', 'Ambos'], value='ψ(x)', description='Mostrar'),
    Nx=IntSlider(value=1000, min=200, max=2000, step=100, description='Pontos x')
)

"""## Desafios para fixação

---

### Exercício 1 — Energia vs Largura do Poço

Com o número quântico fixado em **n = 3**, utilize os controles interativos para alterar a **largura do poço \( a \)** em três valores diferentes:

- \( a = 1.0 \)
- \( a = 3.0 \)
- \( a = 5.0 \)

Acompanhe os valores aproximados de Energia na legenda do gráfico ou pela linha azul no gráfico.

$$
E_n ∝ \frac{n^2}{a^2}
$$

> **Atividade**:
>
> 1. Observe e anote as alturas aproximadas de E(3) no eixo y para os três valores de (a).
> 2. Comprove que a energia **diminui quando o poço se alarga**.

---

### Exercício 2 — Do Quântico ao Clássico

Mude o modo de visualização para densidade de probabilidade (botão "Mostrar"). Explore como a distribuição se comporta para diferentes valores de número quântico \( n \):

- \( n = 1 \)
- \( n = 2 \)
- \( n = 3 \)
- \( n = 4 \)
- \( n = 5 \)

Observe como o gráfico muda conforme o número de oscilações da função de onda aumenta.

> **Atividade**:
>
> 1. Compare a forma da densidade de probabilidade para os diferentes valores de (n).
> 2. O gráfico se torna mais "uniforme" à medida que \( n \) cresce?
> 3. O que isso nos diz sobre a **transição entre o mundo quântico e o mundo clássico**?

---

"""
