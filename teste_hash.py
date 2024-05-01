from werkzeug.security import check_password_hash, generate_password_hash

# Substitua 'senha_secreta' pela senha que você quer testar
senha_hasheada = generate_password_hash('1234')
assert check_password_hash(senha_hasheada, '1234') == True
