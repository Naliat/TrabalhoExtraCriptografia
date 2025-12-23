import matplotlib.pyplot as plt
import os
import re

# Especificações do meu hardware
CPU_INFO = "12th Gen Intel® Core™ i5-12450HX"
METRICA = "34 bits de dificuldade"

def carregar_dados_auditoria():
    cores_data = {}
    vencedor_id = None
    
    #  Buscando o vencedor no arquivo de resultado
    if os.path.exists('resultado.txt'):
        with open('resultado.txt', 'r', encoding='utf-8') as f:
            conteudo = f.read()
            match = re.search(r'(?:N.cleo vencedor|SUCESSO NO N.CLEO)\D*(\d+)', conteudo, re.IGNORECASE)
            if match:
                vencedor_id = int(match.group(1))

    # Carregando logs dos núcleos
    arquivos = [f for f in os.listdir('.') if f.startswith('testes_nucleo_') and f.endswith('.txt')]
    arquivos.sort(key=lambda x: int(re.search(r'\d+', x).group()))

    for f_name in arquivos:
        core_num = int(re.search(r'\d+', f_name).group())
        pontos = []
        with open(f_name, 'r', encoding='utf-8') as f:
            for linha in f:
                m = re.search(r'Tentativa\s+(\d+):', linha)
                if m:
                    pontos.append(int(m.group(1)) / 1_000_000) # Converter para milhões
        if pontos:
            cores_data[core_num] = pontos

    return cores_data, vencedor_id

def gerar_grafico_simples():
    dados, win_id = carregar_dados_auditoria()
    if not dados:
        print("Dados não encontrados.")
        return

    plt.style.use('seaborn-v0_8-whitegrid')
    fig, ax = plt.subplots(figsize=(12, 7))

    for core_id, valores in sorted(dados.items()):
        if core_id == win_id:
            # Plotando o vencedor de acordo com o resultado, cor escolhida vermelha.
            ax.plot(valores, label=f"Núcleo {core_id} (VENCEDOR)", color='#d62728', linewidth=3, zorder=5)
            ax.scatter(len(valores)-1, valores[-1], color='#d62728', s=100, zorder=6)
        else:
            # Outros núcleos em tons de azul/cinza sutis
            ax.plot(valores, label=f"Núcleo {core_id}", color='#1f77b4', alpha=0.3, linewidth=1)

    # Títulos e Legendas
    ax.set_title(f'Análise de Esforço Computacional - Desafio C\nHardware: {CPU_INFO}', fontsize=14, pad=15)
    ax.set_xlabel('Progresso da Auditoria (Amostras de Log)', fontsize=11)
    ax.set_ylabel('Milhões de Hashes Processados', fontsize=11)
    
    # Grid e detalhes
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.legend(loc='upper left', bbox_to_anchor=(1, 1), frameon=True)
    
    # Adiciona caixa de texto com o resumo técnico
    resumo = f"Alvo: 49FC0AA4\nHardware: {CPU_INFO}\nStatus: Quebrado pelo Núcleo {win_id}"
    plt.text(0.02, 0.95, resumo, transform=ax.transAxes, fontsize=10,
             verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

    plt.tight_layout()
    
    # Salvando
    nome_arquivo = 'relatorio_auditoria_simples.png'
    plt.savefig(nome_arquivo, dpi=300)
    print(f"\n[SUCESSO] Gráfico salvo como: {nome_arquivo}")
    plt.show()

if __name__ == "__main__":
    gerar_grafico_simples()