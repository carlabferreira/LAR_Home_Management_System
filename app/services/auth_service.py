# gerencia os usuários

# registrar_usuario(nome, email, senha): valida os dados, verifica e-mail duplicado, gera o hash da senha (werkzeug.security.generate_password_hash) e salva
# autenticar(email, senha): busca o usuário e confere o hash, lançando CredenciaisInvalidasError se falhar