// Variables
var sectionLoading= document.getElementById("loadingScreen");
var sectionMain = document.getElementById("main");
var sectionHome= document.getElementById("home");
var sectionPanel= document.getElementById("panel");
var sectionBills= document.getElementById("bills");
var sectionTransactions= document.getElementById("transactions");

// Vamos começar logo na inicialização o polling  para o servidor para atualizar os dados de 3 em 3 segundos!
// Outra possibilidade é atualizar somente se o usar uma funcionalidade, mas acho que isso é mais elegante e
// Deixa o código mais legível (na minha opinião).
window.onload = function()
{
    start_polling();
}

/******************** PAGES ********************/
// As funções desse bloco fazem as páginas da aplicação aparecerem e desaparecerem
// Deixa o site bonito!
clickHome= function()
{
    sectionHome.style.display = "flex";
    sectionPanel.style.display = "none";
    sectionBills.style.display = "none";
    sectionTransactions.style.display = "none";
}
clickPanel= function()
{
    sectionHome.style.display = "none";
    sectionPanel.style.display = "flex";
    sectionBills.style.display = "none";
    sectionTransactions.style.display = "none";
}
clickBills= function()
{
    sectionHome.style.display = "none";
    sectionPanel.style.display = "none";
    sectionBills.style.display = "flex";
    sectionTransactions.style.display = "none";
}
clickTransactions= function()
{
    sectionHome.style.display = "none";
    sectionPanel.style.display= "none";
    sectionBills.style.display= "none";
    sectionTransactions.style.display= "flex";

}

// Atualiza os dados do painel
function att_panel()
{
    get_month();
    get_six_months();
}

// Atualiza os dados das despesas
function att_bills()
{
    // Por haver somente Posts aqui, não precisa atualizar nada!
}

// Atualiza os dados das transações
function att_transactions()
{
    getValue(); 
}

function polling_data()
{
    att_panel();
    att_bills();
    att_transactions();
}

// long polling
function start_polling()
{
    // Eu não sei fazer websockets em Python, e não consegui aprender a tempo, então vou fazer um long polling a cada 3s para atualizar os dados da conta
    setInterval(polling_data, 3000);
}

// Função para atualizar a tabela dinâmicamente.
function update_table(id, data)
{
    var table = document.getElementById(id);
    for (var i=0; i<data.length; i++)
    {
        let row = document.createElement('tr');
        row.innerHTML = '<td>' + data[i].DATA + '</td>' + 
        '<td>' + data[i].TIPO + '</td>' + 
        '<td>' + data[i].CATEGORIA + '</td>' + 
        '<td>' + data[i].DESCRICAO + '</td>' + 
        '<td>' + data[i].VALOR + '</td>';
        
        table.appendChild(row);
    }
}

/******************** REQUESTS ********************/

// Função para requisitar o valor (monetário) total da conta.
function getValue() {
    var xhr = new XMLHttpRequest();
    xhr.open("GET", "/getValue", true);
    
    xhr.onreadystatechange = function() {
        if (xhr.readyState == 4 && xhr.status == 200) {
            value = 'R$: ' + xhr.responseText;
            let valueElement = document.getElementById("statement");
            valueElement.textContent = value
        }
    }
    xhr.send();
}

// Função para requisitar o valor (monetário) do mês atual.
function get_month()
{
    var xhr = new XMLHttpRequest();
    xhr.open("GET", "/getThisMonth", true);
    xhr.onreadystatechange = function(){
        if(xhr.readyState == 4 && xhr.status == 200){
            value = 'R$: '+ xhr.responseText;
            let valueElement = document.getElementById("this-month");
            valueElement.textContent = value;
        }
    }
    xhr.send();
}

// Função para requisitar o valor (monetário) dos últimos seis meses.
function get_six_months() {
    var xhr = new XMLHttpRequest();
    xhr.open("GET", "/getSixMonths", true);
    xhr.onreadystatechange = function() {
        if (xhr.readyState == 4 && xhr.status == 200) {
            var data = JSON.parse(xhr.responseText);
            var listElement = document.getElementById("six-months-list");
            listElement.innerHTML = "";

            for (var i = 0; i < data.length; i++) {
                var lista = document.createElement("li");
                lista.textContent = "Mês " + (i + 1) + " - R$: " + data[i].toFixed(2)
                listElement.appendChild(lista);
            }
        }
    };
    xhr.send();
}

// Função para enviar dados para o servidor
function post_data(data, url) {
    var xhr = new XMLHttpRequest();
    xhr.open("POST", url, true);
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhr.onreadystatechange = function() {
        if (xhr.readyState == 4 && xhr.status == 200) {
            alert("Dados enviados com sucesso!")
        }
    };
    xhr.send(JSON.stringify(data));
}

// Função para adicionar nova despesa ao banco de dados
function post_new_bill() {
    var formData = {
        'DATA': document.getElementById('date').value,
        'TIPO': document.getElementById('type').value,
        'CATEGORIA': document.getElementById('category').value,
        'DESCRICAO': document.getElementById('description').value,
        'VALOR': document.getElementById('value').value
    }

    var url = "/addBill";
    //console.log(formData);
    post_data(formData, url);
}

// Função para adicionar nova receita ao banco de dados
function post_new_income() {
    var formData = {
        'DATA': document.getElementById('date').value,
        'TIPO': document.getElementById('type').value,
        'CATEGORIA': document.getElementById('category').value,
        'DESCRICAO': document.getElementById('description').value,
        'VALOR': document.getElementById('value').value
    }

    var url = "/addIncome";
    //console.log(formData);
    post_data(formData, url);
}


// Função para exportar dados
exportData = function(){
    var xhr = new XMLHttpRequest();
    xhr.open("GET", "/exportData", true);
    xhr.onreadystatechange = function() {
        if(xhr.readyState == 4 && xhr.status == 200){
            var encoder = new TextEncoder();
            var responseData = encoder.encode(xhr.responseText);
            var a = document.createElement("a");
            var file = new Blob([responseData], {type: "text/csv;charset=utf-8"});
            a.href = URL.createObjectURL(file);
            a.download = "Database.csv";
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
        }
    }
    xhr.send();
}

function alert_with_button() {
    var response = window.confirm("Essa ação irá apagar a última linha do seu banco da dados.\nDeseja continuar?");
    return response;
}

function post_remove_bill()
{
    if (alert_with_button())
    {
        var xhr = new XMLHttpRequest();
        xhr.open("POST", '/deleteAllData', true);
        xhr.setRequestHeader("Content-Type", "text/plain");
        xhr.onreadystatechange = function() {
            if (xhr.readyState == 4 && xhr.status == 200) {
                alert("Comando enviado com sucesso!")
            }
        };
        xhr.send();
    }
    else {
        alert("Comando cancelado! \nNão foi feita nenhuma alteração.")
    }
}

function post_merge_bills() 
{
    var formData = {
        'index_1': document.getElementById('index1').value,
        'index_2': document.getElementById('index2').value,
    }
    var xhr = new XMLHttpRequest();
    xhr.open("POST", '/mergeData', true);
    xhr.setRequestHeader("Content-Type", "text/plain");
    xhr.onreadystatechange = function() {
        if (xhr.readyState == 4 && xhr.status == 200) {
            alert("Comando enviado com sucesso!")
        }
    };
    xhr.send(JSON.stringify(formData));
}