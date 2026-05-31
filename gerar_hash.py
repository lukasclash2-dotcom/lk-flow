import streamlit_authenticator as stauth

# 1. COLOQUE A SUA SENHA REAL DENTRO DAS ASPAS ABAIXO:
sua_senha_real = "98251195@Luk"  # <-- Mude aqui para a senha que você quiser!

# 2. O CÓDIGO ABAIXO GERA O HASH CORRETAMENTE
senha_criptografada = stauth.Hasher.hash(sua_senha_real)

print("\n" + "="*40)
print("COPIE APENAS O CÓDIGO ABAIXO:")
print(senha_criptografada)
print("="*40 + "\n")