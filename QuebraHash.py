import hashlib
import string
import random
import multiprocessing
import time
import os

# Definição do alvo
TARGET_HEX = "49FC0AA4"

def brute_force_worker(core_id, found_event):
    """
    Função executada por cada núcleo da CPU para busca exaustiva
    """
    chars = string.ascii_letters + string.digits
    attempts = 0
    log_file = f"testes_nucleo_{core_id}.txt"
    
    # Abre o arquivo de log para este núcleo
    with open(log_file, "w") as f_log:
        f_log.write(f"Iniciando busca no Núcleo {core_id} - Alvo: {TARGET_HEX}\n")
        
        while not found_event.is_set():
           
            candidate = ''.join(random.choices(chars, k=12))
            
            # SHAKE128 conforme requisito do laboratório 
            shake = hashlib.shake_128()
            shake.update(candidate.encode('utf-8'))
            
            # Extrai 4 bytes (32 bits) para comparação com o prefixo 
            digest = shake.digest(4).hex().upper()
            
            # Log a cada 1 milhão de tentativas para manter performance
            if attempts % 1000000 == 0:
                f_log.write(f"Tentativa {attempts}: {candidate} -> {digest}\n")
                f_log.flush()
                # Exibe progresso no terminal
                if core_id == 0: 
                    print(f"[PROGRESSO] Núcleo 0 atingiu {attempts} tentativas...")

            # Verificando se encontrou a pré-imagem 
            if digest == TARGET_HEX:
                found_event.set() # Avisa os outros núcleos para pararem
                
                # Salva o resultado final 
                with open("resultado.txt", "w") as f_res:
                    f_res.write("=== SUCESSO NA QUEBRA DE PRÉ-IMAGEM ===\n")
                    f_res.write(f"Alvo: {TARGET_HEX}\n")
                    f_res.write(f"Candidato encontrado (x): {candidate}\n")
                    f_res.write(f"Hash gerado: {digest}\n")
                    f_res.write(f"Núcleo vencedor: {core_id}\n")
                
                print(f"\n[!!!] SUCESSO NO NÚCLEO {core_id}!")
                print(f"Candidato: {candidate}")
                print("Resultado salvo em 'resultado.txt'.")
                break
            
            attempts += 1

if __name__ == "__main__":
    # Detecta quantos núcleos a CPU possui para usar 100% da capacidade
    cpus = multiprocessing.cpu_count()
    print(f"--- AUDITORIA SHAKE128 ---")
    print(f"Utilizando {cpus} núcleos da CPU para máxima velocidade.")
    print(f"Alvo: {TARGET_HEX} | Dificuldade: 34 bits ")
    
    found_event = multiprocessing.Event()
    processes = []

    start_time = time.time()

    # Inicia um processo para cada CPU
    for i in range(cpus):
        p = multiprocessing.Process(target=brute_force_worker, args=(i, found_event))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    end_time = time.time()
    print(f"Tempo total de execução: {end_time - start_time:.2f} segundos.")
    print(f"Verifique 'resultado.txt' e informe no grupo do Telegram[cite: 48].")