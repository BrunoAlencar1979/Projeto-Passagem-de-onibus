document.addEventListener('DOMContentLoaded', function () {

    // Exibe a mensagem de atraso de 4 horas para a rota "Vitória -> Linhares"
    const rotaElement = document.getElementById('rota');
    if (rotaElement) {
        rotaElement.addEventListener('change', function (e) {
            const rota = e.target.value;
            const messageContainer = document.getElementById('warning-message');

            // Verifica se a rota é "Vitória -> Linhares"
            if (rota === "Vitória -> Linhares") {
                messageContainer.innerHTML = "<p><strong>Atenção:</strong> Esta viagem terá um atraso de 4 horas.</p>";
            } else {
                messageContainer.innerHTML = "";  // Limpa a mensagem de atraso se outra rota for escolhida
            }
        });
    }

    // Processa a compra de passagem e exibe o ticket de compra
    const viagemForm = document.getElementById('viagem-form');
    if (viagemForm) {
        viagemForm.addEventListener('submit', function (e) {
            e.preventDefault();

            const rota = document.getElementById('rota').value;
            const horario_embarque = document.getElementById('horario_embarque').value;
            const data_viagem = document.getElementById('data_viagem').value;

            // Verifica se os campos estão preenchidos corretamente
            if (!rota || !horario_embarque || !data_viagem) {
                document.getElementById('ticket-message').innerText = "Preencha todos os campos!";
                return;
            }

            // Envia os dados para o servidor para processar a compra da passagem
            fetch('/comprar', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                body: new URLSearchParams({
                    rota: rota,  // Nome do campo precisa coincidir com o esperado no Flask
                    horario_embarque: horario_embarque,  // Nome do campo precisa coincidir com o esperado no Flask
                    data_viagem: data_viagem  // Nome do campo precisa coincidir com o esperado no Flask
                })
            })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        // Exibe as informações do ticket de compra e a mensagem de sucesso
                        let message = `
                        <h2>Ticket de Compra</h2>
                        <p>Empresa: ${data.empresa}</p>
                        <p>Nome: ${data.nome}</p>
                        <p>CPF: ${data.cpf}</p>
                        <p>Horário de embarque: ${data.horario_embarque}</p>
                        <p>Tempo de viagem: ${data.tempo_viagem}</p>
                        <p>Horário de chegada: ${data.horario_chegada}</p>
                        <p>Preço: R$ ${data.preco.toFixed(2)}</p>
                    `;
                        if (data.atraso !== '0:00:00') {
                            message += `<p><strong>Atenção:</strong> Esta viagem teve um atraso de 4 horas.</p>`;
                        }
                        message += `<p style="color: green;"><strong>Compra realizada com sucesso!</strong></p>`;
                        document.getElementById('ticket-message').innerHTML = message;
                    } else {
                        // Exibe uma mensagem de erro se não foi possível processar a compra
                        document.getElementById('ticket-message').innerText = data.message;
                    }
                })
                .catch(error => {
                    console.error('Erro:', error);
                    document.getElementById('ticket-message').innerText = "Erro ao processar a compra.";
                });
        });
    }

    // Cadastro de usuário
    const registerForm = document.getElementById('register-form');
    if (registerForm) {
        registerForm.addEventListener('submit', function (e) {
            e.preventDefault();

            const nome = document.getElementById('nome').value;
            const email = document.getElementById('email').value;
            const senha = document.getElementById('senha').value;
            const confirmar_senha = document.getElementById('confirmar_senha').value;
            const cpf = document.getElementById('cpf').value;
            const cep = document.getElementById('cep').value;
            const rua = document.getElementById('rua').value;
            const cidade = document.getElementById('cidade').value;
            const bairro = document.getElementById('bairro').value;

            // Validação simples de senha e CPF
            if (senha !== confirmar_senha) {
                document.getElementById('message').innerText = "As senhas não coincidem.";
                return;
            }

            if (cpf.length !== 11) {
                document.getElementById('message').innerText = "O CPF deve conter 11 dígitos.";
                return;
            }

            // Envia os dados do cadastro
            fetch('/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                body: new URLSearchParams({
                    nome: nome,
                    email: email,
                    senha: senha,
                    confirmar_senha: confirmar_senha,
                    cpf: cpf,
                    cep: cep,
                    rua: rua,
                    cidade: cidade,
                    bairro: bairro
                })
            })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        // Exibe a mensagem de sucesso e redireciona para a página de login
                        alert(data.message);
                        window.location.href = data.redirect;
                    } else {
                        // Exibe a mensagem de erro
                        document.getElementById('message').innerText = data.message;
                    }
                })
                .catch(error => {
                    console.error('Erro:', error);
                    document.getElementById('message').innerText = "Erro ao processar o cadastro.";
                });
        });
    }
});
