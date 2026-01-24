const form = document.getElementById('form-produto');
const lista = document.getElementById('lista-produtos');

// Função para carregar produtos do backend
async function carregarProdutos() {
    const resposta = await fetch('/produtos');
    const produtos = await resposta.json();

    lista.innerHTML = ''; // Limpa lista
    produtos.forEach(produto => {
        const li = document.createElement('li');
        li.setAttribute('data-id', produto.id);
        li.innerHTML = `
            ${produto.nome} - R$ ${produto.preco.toFixed(2)}
            <button class="excluir">Excluir</button>
        `;
        lista.appendChild(li);
    });
}

// Adicionar produto
form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const nome = document.getElementById('nome').value;
    const preco = parseFloat(document.getElementById('preco').value);

    const resposta = await fetch('/produtos', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ nome, preco })
    });

    if (resposta.ok) {
        document.getElementById('nome').value = '';
        document.getElementById('preco').value = '';
        carregarProdutos(); // Atualiza lista
    } else {
        alert('Erro ao adicionar produto');
    }
});

// Excluir produto
lista.addEventListener('click', async (e) => {
    if (e.target.classList.contains('excluir')) {
        const li = e.target.parentElement;
        const id = li.getAttribute('data-id');

        const resposta = await fetch(`/produtos/${id}`, {
            method: 'DELETE'
        });

        if (resposta.ok) {
            li.remove(); // Remove do frontend
        } else {
            alert('Erro ao excluir produto');
        }
    }
});

// Carrega os produtos assim que a página abre
window.onload = carregarProdutos;
