// Executar quando o documento HTML for completamente carregado
document.addEventListener('DOMContentLoaded', function () {

    // Receber o SELETOR calendar do atributo id
    var calendarEl = document.getElementById('calendar');

    // Receber o SELETOR da janela modal cadastrar
    const cadastrarModal = new bootstrap.Modal(document.getElementById("cadastrarModal")); 

    // Receber o SELETOR da janela modal visualizar
    const visualizarModal = new bootstrap.Modal(document.getElementById("visualizarModal"));

    // Receber o SELETOR "msgViewEvento"
    const msgViewEvento = document.getElementById('msgViewEvento');

    // Instanciar FullCalendar.Calendar e atribuir a variável calendar
    var calendar = new FullCalendar.Calendar(calendarEl, {
         
        initialView: 'dayGridMonth',
        events: '/api/eventos',
        
       // Incluir o bootstrap 5
        themeSystem: 'bootstrap5',

        // Criar o cabeçalho do calendário
        headerToolbar: {
            left: 'prev,next',
            center: 'title',
            right: 'today'
        },

        // Definir o idioma usado no calendário
        locale: 'pt-br',

        // Definir a data inicial
        //initialDate: '2023-01-12',
        //initialDate: '2023-10-12',

        // Permitir clicar nos nomes dos dias da semana 
        navLinks: true,

        // Permitir clicar e arrastar o mouse sobre um ou vários dias no calendário
        selectable: true,

        // Indicar visualmente a área que será selecionada antes que o usuário solte o botão do mouse para confirmar a seleção
        selectMirror: true,

        // Permitir arrastar e redimensionar os eventos diretamente no calendário.
        editable: true,

        // Número máximo de eventos em um determinado dia, se for true, o número de eventos será limitado à altura da célula do dia
        dayMaxEvents: true,

        
        
        // Identificar o clique do usuário sobre o evento existente
        eventClick: function(info) {
            // Função para formatar a data
            function formatDate(dateString) {
                var parts = dateString.split('-');
                return parts[2] + '/' + parts[1] + '/' + parts[0];
 }  

         // Faz uma requisição GET para buscar os detalhes do evento usando o ID do evento
    fetch('/get_event_details/' + info.event.id)
         .then(response => response.json())
         .then(data => {
             // Verifica se a resposta contém um erro
             if(data.error) {
                 alert('Erro ao buscar detalhes do evento: ' + data.error);
             } else {
                 // Preenche os campos do modal com as informações do evento
                 $('#eventPurposeView').val(data.purpose);
                 $('#dosageView').val(data.dosage);
                 $('#type_of_factorView').val(data.type_of_factor);
                 $('#absenceView').val(data.absence);
                 $('#application_dateView').val(formatDate(data.application_date));
                 $('#application_timeView').val(data.application_time);
                 $('#eventID').val(info.event.id); 
                 $('#editEventButton').off('click').on('click', function() {
                    // Chama a função para editar o evento
                    editEvent(info.event.id);
                });
            
               

                 // Abre o modal de visualização
                 visualizarModal.show();
             }
         })
         .catch(error => {
             // Trata erros de rede
             console.error('Erro ao buscar detalhes do evento:', error);
         });
 },


  select: function(arg) {
   
    // Obter a data selecionada
    const dataSelecionada = arg.start;
    const ano = dataSelecionada.getFullYear();
    const mes = dataSelecionada.getMonth() + 1; // Os meses são indexados de 0 a 11, então adicionamos 1
    const dia = dataSelecionada.getDate();
    const dataFormatada = `${ano}-${mes.toString().padStart(2, '0')}-${dia.toString().padStart(2, '0')}`;
    document.getElementById("application_date").value = dataFormatada;

     // Abrir o modal para cadastrar o evento
     $('#cadastrarModal').modal('show');
  } 
});

        // Adicionar os listeners para o botão de excluir 
       
 
  document.getElementById('deleteEventButton').addEventListener('click', function() {
    // Código para excluir o evento
    var eventId = $('#eventID').val(); 
    fetch('/delete_event/' + eventId, { method: 'DELETE' })
        .then(response => {
            if(response.ok) {
                // Fechar o modal e atualizar o calendário
                calendar.refetchEvents();
                $('#visualizarModal').modal('hide');
            } else {
                alert('Erro ao excluir o evento');
            }
        });
   });
// Adicionar os listeners para os botão de editar
  document.getElementById('editEventButton').addEventListener('click', function() {
    // Código para editar o evento
    var eventId = $('#eventID').val(); // ID do evento armazenado no campo oculto
    // Buscar os detalhes do evento para edição
    fetch('/get_event_details/' + eventId)
        .then(response => response.json())
        .then(data => {
            // Preencher o formulário de edição com os dados do evento
            // ...
            // Abrir o modal de edição
            $('#editarModal').modal('show');
        })
        .catch(error => {
            console.error('Erro ao buscar detalhes do evento para edição:', error);
        });
    });
    // Renderizar o calendário
    calendar.render();
            
});
