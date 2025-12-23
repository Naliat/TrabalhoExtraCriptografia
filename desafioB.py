import hashlib
import string
import random
import multiprocessing
import os
import time

# Dados do Aluno conforme o PDF
NOME_COMPLETO = "Tailan de Souza Oliveira" 
X1 = f"Aluno: {NOME_COMPLETO}"

def worker_segunda_pre_imagem(core_id, target_hash, found_event):
    chars = string.ascii_letters + string.digits
    tentativas = 0
    
    # Pasta para logs temporários (opcional)
    os.makedirs("testes", exist_ok=True)
    
    while not found_event.is_set():
        # Gera candidato x2
        x2 = ''.join(random.choices(chars, k=15))
        if x2 == X1: continue 

        # SHAKE128 - 4 bytes
        shake = hashlib.shake_128()
        shake.update(x2.encode('utf-8'))
        digest = shake.digest(4).hex().upper()

        if digest == target_hash:
            found_event.set()
            os.makedirs("resultados", exist_ok=True)
            res_path = os.path.join("resultados", "resultado_desafio_B.txt")
            
            with open(res_path, "w") as f:
                f.write("=== DESAFIO B: SEGUNDA PRÉ-IMAGEM ===\n")
                f.write(f"x1 (fixo): {X1}\n")
                f.write(f"x2 (encontrado): {x2}\n")
                f.write(f"Hash Comum: {target_hash}\n")
                f.write(f"Núcleo Vencedor: {core_id}\n")
                f.write(f"Tentativas aproximadas por núcleo: {tentativas}\n")
            
            print(f"\n[!!!] SUCESSO NO NÚCLEO {core_id}!")
            print(f"x2 encontrado: {x2} -> {digest}")
            break

        tentativas += 1
        if tentativas % 1000000 == 0 and core_id == 0:
            print(f"[PROGRESSO] Núcleo 0: {tentativas} tentativas...")

if __name__ == "__main__":
    # 1. Calcula o hash alvo do x1
    shake_alvo = hashlib.shake_128()
    shake_alvo.update(X1.encode('utf-8'))
    target_hash = shake_alvo.digest(4).hex().upper()

    print(f"--- DESAFIO B: BUSCANDO SEGUNDA PRÉ-IMAGEM ---")
    print(f"Alvo fixo (x1): {X1}")
    print(f"Hash a encontrar: {target_hash}")

    cpus = multiprocessing.cpu_count()
    found_event = multiprocessing.Event()
    processes = []
    
    start_time = time.time()

    for i in range(cpus):
        p = multiprocessing.Process(target=worker_segunda_pre_imagem, args=(i, target_hash, found_event))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    end_time = time.time()
    print(f"Tempo total: {end_time - start_time:.2f} segundos.")