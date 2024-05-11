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

        // Incluir o bootstrap 5
        themeSystem: 'bootstrap5',

        // Criar o cabeçalho do calendário
        headerToolbar: {
            left: 'prev,next today',
            center: 'title',
            right: 'dayGridMonth,timeGridWeek,timeGridDay'
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

        
        // Identificar o clique do usuário sobre o evento
        eventClick: function (info) {

            // Apresentar os detalhes do evento
            document.getElementById("visualizarEvento").style.display = "block";
            document.getElementById("visualizarModalLabel").style.display = "block";

            // Ocultar o formulário editar do evento
            document.getElementById("editarEvento").style.display = "none";
            document.getElementById("editarModalLabel").style.display = "none";

            // Enviar para a janela modal os dados do evento
            document.getElementById("visualizar_id").innerText = info.event.id;
            document.getElementById("visualizar_title").innerText = info.event.title;
            document.getElementById("visualizar_obs").innerText = info.event.extendedProps.obs;
            document.getElementById("visualizar_start").innerText = info.event.start.toLocaleString();
            document.getElementById("visualizar_end").innerText = info.event.end !== null ? info.event.end.toLocaleString() : info.event.start.toLocaleString();

            // Enviar os dados do evento para o formulário editar
            document.getElementById("edit_id").value = info.event.id;
            document.getElementById("edit_title").value = info.event.title;
            document.getElementById("edit_obs").value = info.event.extendedProps.obs;
            document.getElementById("edit_start").value = converterData(info.event.start);
            document.getElementById("edit_end").value = info.event.end !== null ? converterData(info.event.end) : converterData(info.event.start);
            document.getElementById("edit_color").value = info.event.backgroundColor;

            // Abrir a janela modal visualizar
            visualizarModal.show();
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

    // Renderizar o calendário
    calendar.render();

});