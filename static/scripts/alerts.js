function validateCheckboxes(event) {
    // Получаем все чекбоксы
    var checkboxes = document.querySelectorAll('input[type="checkbox"]');
    var isChecked = false;

    // Проверяем, есть ли хотя бы один выбранный чекбокс
    checkboxes.forEach(function(checkbox) {
        if (checkbox.checked) {
            isChecked = true;
        }
    });

    // Если ни один чекбокс не выбран, показываем предупреждение и отменяем отправку формы
    if (!isChecked) {
        event.preventDefault(); // Отмена отправки формы
        alert("Нужно выбрать хотя бы один параметр для генерации пароля!");
    } else {
        // Показать сообщение об успешном создании пароля
        alert("Пароль успешно создан");
    }
}

function userExistAllert(event) {
    event.preventDefault();
    alert("Пользователь с таким именем уже есть")
}
function savedPasswordAlert() {
    alert("Пароль сохранен")
}
