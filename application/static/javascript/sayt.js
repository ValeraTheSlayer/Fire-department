<script>
  $(function() {
    // создаем Broadcast Channel с именем 'my-channel'
    const channel = new BroadcastChannel('my-channel');

    // сохраняем данные в локальном хранилище и отправляем сообщение
    $('#current_emergency_form').on('input', function() {
      localStorage.setItem('emergency_form_data', $(this).serialize());
      channel.postMessage('emergency_form_data_updated');
    });

    // слушаем сообщения в других вкладках
    channel.addEventListener('message', event => {
      if (event.data === 'emergency_form_data_updated') {
        // обновляем данные из локального хранилища
        const formData = localStorage.getItem('emergency_form_data');
        $('#current_emergency_form').deserialize(formData);
      }
    });

    // инициализируем плагин 'sayt'
    $('#current_emergency_form').sayt();
  });
</script>
