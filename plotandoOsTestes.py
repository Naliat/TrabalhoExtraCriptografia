import matplotlib.pyplot as plt
import os
import re

# Especificações do hardware e tempo real da auditoria
CPU_INFO = "12th Gen Intel® Core i5-12450HX"
TARGET = "49FC0AA4"
TEMPO_TOTAL = "7384.41s (~2h 03min)" # Tempo real informado

def carregar_dados_auditoria():
    cores_data = {}
    vencedor_id = None
    
    # Busca o vencedor na pasta 'resultados/'
    caminho_resultado = os.path.join('resultados', 'resultado.txt')
    if os.path.exists(caminho_resultado):
        with open(caminho_resultado, 'r', encoding='utf-8') as f:
            conteudo = f.read()
            match = re.search(r'(?:N.cleo vencedor|SUCESSO NO N.CLEO|N.cleo)\D*(\d+)', conteudo, re.IGNORECASE)
            if match:
                vencedor_id = int(match.group(1))

    # Carrega logs da pasta 'testes/'
    pasta_testes = 'testes'
    if os.path.exists(pasta_testes):
        arquivos = [f for f in os.listdir(pasta_testes) if f.startswith('testes_nucleo_') and f.endswith('.txt')]
        arquivos.sort(key=lambda x: int(re.search(r'\d+', x).group()))

        for f_name in arquivos:
            core_num = int(re.search(r'\d+', f_name).group())
            pontos = []
            with open(os.path.join(pasta_testes, f_name), 'r', encoding='utf-8') as f:
                for linha in f:
                    m = re.search(r'Tentativa\s+(\d+):', linha)
                    if m:
                        pontos.append(int(m.group(1)) / 1_000_000)
            if pontos:
                cores_data[core_num] = pontos

    return cores_data, vencedor_id

def gerar_visualizacao_profissional():
    dados, win_id = carregar_dados_auditoria()
    if not dados:
        print("Erro: Verifique se as pastas 'testes/' e 'resultados/' contêm os arquivos.")
        return

    plt.style.use('seaborn-v0_8-whitegrid')
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))

    # --- GRÁFICO 1: PROGRESSÃO (LINHA) ---
    for core_id, valores in sorted(dados.items()):
        if core_id == win_id:
            ax1.plot(valores, label=f"C{core_id} (VENCEDOR)", color='#d62728', linewidth=3, zorder=5)
            ax1.scatter(len(valores)-1, valores[-1], color='#d62728', s=100, zorder=6)
        else:
            ax1.plot(valores, label=f"C{core_id}", color='#1f77b4', alpha=0.3, linewidth=1)

    ax1.set_title(f'Progresso Temporal da Auditoria\nAlvo: {TARGET}', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Milhões de Hashes Processados')
    ax1.set_xlabel('Amostras de Log')
    ax1.legend(loc='upper left', fontsize='small', ncol=2)

    # --- GRÁFICO 2: ESFORÇO TOTAL (BARRAS) ---
    labels = [f"C{k}" for k in dados.keys()]
    totais = [v[-1] for v in dados.values()]
    cores_barras = ['#d62728' if k == win_id else '#1f77b4' for k in dados.keys()]
    
    bars = ax2.bar(labels, totais, color=cores_barras, alpha=0.7, edgecolor='black')
    ax2.set_title(f'Esforço Total por Núcleo\nTempo de Execução: {TEMPO_TOTAL}', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Total de Milhões de Hashes')
    
    # Adicionar valor no topo das barras
    for bar in bars:
        yval = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2, yval + 1, f'{int(yval)}M', ha='center', va='bottom', fontsize=8)

    # Rodapé com Info do Hardware
    plt.figtext(0.5, 0.01, f"Hardware: {CPU_INFO} | Auditoria SHAKE128 | Resistência à Pré-imagem Quebrada", 
                ha="center", fontsize=10, bbox={"facecolor":"orange", "alpha":0.2, "pad":5})

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    
    os.makedirs("resultados", exist_ok=True)
    nome_arquivo = os.path.join('resultados', 'dashboard_final_auditoria.png')
    plt.savefig(nome_arquivo, dpi=300)
    print(f"\n[SUCESSO] Dashboard salvo em: {nome_arquivo}")
    plt.show()

if __name__ == "__main__":
    gerar_visualizacao_profissional()