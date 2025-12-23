import hashlib
import string
import random
import os

def encontrar_colisao_shake128():
    """
    Desafio A: Encontrar duas strings x e y tais que H(x) = H(y).
    Saída: 4 bytes (32 bits).
    """
    # Pasta para o resultado do Desafio A
    os.makedirs("resultados", exist_ok=True)
    
    chars = string.ascii_letters + string.digits
    historico_hashes = {} # Dicionário para armazenar {hash: string_que_gerou}
    tentativas = 0
    
    print("--- DESAFIO A: BUSCANDO COLISÃO SHAKE128 (4 BYTES) ---")
    print("Aguarde... o Paradoxo do Aniversário facilitará as coisas.")

    while True:
        # 1. Gera uma string aleatória
        candidato = ''.join(random.choices(chars, k=12))
        
        # 2. Gera o hash SHAKE128 de 4 bytes
        shake = hashlib.shake_128()
        shake.update(candidato.encode('utf-8'))
        digest = shake.digest(4).hex().upper()
        
        # 3. Verifica se este digest já foi visto antes
        if digest in historico_hashes:
            string_original = historico_hashes[digest]
            
            # Garante que não é a mesma string (improvável com random, mas boa prática)
            if string_original != candidato:
                print(f"\n[!!!] COLISÃO ENCONTRADA!")
                print(f"Tentativas totais: {tentativas}")
                print(f"String 1: {string_original} -> {digest}")
                print(f"String 2: {candidato} -> {digest}")
                
                # Salva o resultado
                res_path = os.path.join("resultados", "resultado_desafio_A.txt")
                with open(res_path, "w") as f:
                    f.write("=== DESAFIO A: QUEBRA DE RESISTÊNCIA A COLISÃO ===\n")
                    f.write(f"Tentativas: {tentativas}\n")
                    f.write(f"String 1: {string_original} | Hash: {digest}\n")
                    f.write(f"String 2: {candidato} | Hash: {digest}\n")
                
                break
        
        # 4. Se não viu, guarda no dicionário e continua
        historico_hashes[digest] = candidato
        tentativas += 1
        
        if tentativas % 10000 == 0:
            print(f"Tentativas: {tentativas}...")

if __name__ == "__main__":
    encontrar_colisao_shake128()