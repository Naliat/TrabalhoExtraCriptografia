import matplotlib.pyplot as plt
import os
import re

# Informando meu hardware no top
CPU_NOME = "Intel® Core™ i5-12450HX (12 Núcleos)"

def obter_totais():
    nucleos_totais = {}
    vencedor = None
    
    # Identifica quem foi o vencedor no resultado.txt
    if os.path.exists('resultado.txt'):
        with open('resultado.txt', 'r', encoding='utf-8') as f:
            texto = f.read()
            m = re.search(r'(?:N.cleo vencedor|SUCESSO NO N.CLEO)\D*(\d+)', texto, re.IGNORECASE)
            if m: vencedor = int(m.group(1))

    # Lê o último checkpoint de cada arquivo de log
    arquivos = [f for f in os.listdir('.') if f.startswith('testes_nucleo_') and f.endswith('.txt')]
    arquivos.sort(key=lambda x: int(re.search(r'\d+', x).group()))

    for f_name in arquivos:
        num = int(re.search(r'\d+', f_name).group())
        try:
            with open(f_name, 'r', encoding='utf-8') as f:
                linhas = f.readlines()
                for linha in reversed(linhas):
                    m = re.search(r'Tentativa\s+(\d+):', linha)
                    if m:
                        nucleos_totais[num] = int(m.group(1)) / 1_000_000 # Em Milhões
                        break
        except Exception:
            continue

    return nucleos_totais, vencedor

def plotar_barras():
    dados, win_id = obter_totais()
    if not dados:
        print("Nenhum dado de log encontrado.")
        return

    plt.style.use('seaborn-v0_8-muted')
    fig, ax = plt.subplots(figsize=(10, 6))

    # Configuração das Barras
    labels = [f"Core {k}" for k in dados.keys()]
    valores = list(dados.values())
    
    # Cores simples: Azul para todos, Vermelho para o vencedor
    cores = ['#4C72B0' if k != win_id else '#C44E52' for k in dados.keys()]

    barras = ax.bar(labels, valores, color=cores, edgecolor='black', alpha=0.8)

    # Adicionar os valores numéricos em cima de cada barra
    for barra in barras:
        altura = barra.get_height()
        ax.text(barra.get_x() + barra.get_width()/2, altura, f'{altura:.1f}M', 
                ha='center', va='bottom', fontsize=9, fontweight='bold')

    # Personalização Acadêmica
    ax.set_title(f'Esforço de Auditoria por Núcleo\nHardware: {CPU_NOME}', fontsize=12, pad=15)
    ax.set_ylabel('Hashes Processados (Milhões de Tentativas)', fontsize=10)
    ax.set_xlabel('Núcleos da CPU', fontsize=10)
    ax.grid(axis='y', linestyle='--', alpha=0.7)

    # Legenda informativa
    total_geral = sum(dados.values())
    plt.figtext(0.15, 0.8, f"Total Processado: {total_geral:.1f}M hashes\nAlvo: 49FC0AA4", 
                fontsize=9, bbox=dict(facecolor='white', alpha=0.5))

    plt.tight_layout()
    plt.savefig('comparativo_barras_nucleos.png', dpi=300)
    print("\n[SUCESSO] Gráfico 'comparativo_barras_nucleos.png' gerado.")
    plt.show()

if __name__ == "__main__":
    plot_bars = plotar_barras()