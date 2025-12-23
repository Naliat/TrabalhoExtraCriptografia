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
    Função executada por cada núcleo da CPU para busca exaustiva.
    Salva logs na pasta 'testes/'.
    """
    # Garantir que a pasta de testes existe
    os.makedirs("testes", exist_ok=True)
    
    chars = string.ascii_letters + string.digits
    attempts = 0
    log_file = os.path.join("testes", f"testes_nucleo_{core_id}.txt")
    
    with open(log_file, "w") as f_log:
        f_log.write(f"Iniciando busca no Núcleo {core_id} - Alvo: {TARGET_HEX}\n")
        
        while not found_event.is_set():
            candidate = ''.join(random.choices(chars, k=12))
            
            # SHAKE128: Função XOF da família SHA-3
            shake = hashlib.shake_128()
            shake.update(candidate.encode('utf-8'))
            
            # Extrai 4 bytes (32 bits) para comparação
            digest = shake.digest(4).hex().upper()
            
            # Log de auditoria a cada 1 milhão de tentativas 
            if attempts % 1000000 == 0:
                f_log.write(f"Tentativa {attempts}: {candidate} -> {digest}\n")
                f_log.flush()
                if core_id == 0: 
                    print(f"[PROGRESSO] Núcleo 0 atingiu {attempts} tentativas...")

            # Quebrando a Resistência à Pré-imagem
            if digest == TARGET_HEX:
                found_event.set() 
                
                # Garantir que a pasta de resultados existe
                os.makedirs("resultados", exist_ok=True)
                res_path = os.path.join("resultados", "resultado.txt")
                
                with open(res_path, "w") as f_res:
                    f_res.write("=== SUCESSO NA QUEBRA DE PRÉ-IMAGEM ===\n")
                    f_res.write(f"Alvo: {TARGET_HEX}\n")
                    f_res.write(f"Candidato encontrado (x): {candidate}\n")
                    f_res.write(f"Hash gerado: {digest}\n")
                    f_res.write(f"Núcleo vencedor: {core_id}\n")
                
                print(f"\n[!!!] SUCESSO NO NÚCLEO {core_id}!")
                print(f"Candidato: {candidate}")
                print(f"Resultado salvo em '{res_path}'.")
                break
            
            attempts += 1

if __name__ == "__main__":
    cpus = multiprocessing.cpu_count()
    print(f"--- AUDITORIA SHAKE128 ---")
    print(f"Hardware: Intel Core i5-12450HX ({cpus} threads)")
    print(f"Alvo: {TARGET_HEX} | Dificuldade: 34 bits ")
    
    found_event = multiprocessing.Event()
    processes = []
    start_time = time.time()

    for i in range(cpus):
        p = multiprocessing.Process(target=brute_force_worker, args=(i, found_event))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    end_time = time.time()
    print(f"Tempo total: {end_time - start_time:.2f} segundos.")
    print(f" {TARGET_HEX} foi quebrado.")