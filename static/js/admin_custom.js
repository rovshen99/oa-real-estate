document.addEventListener('DOMContentLoaded', function() {
    // Функция для переключения видимости поля
    function toggleNumberOfFloorsField() {
        console.log("admin_custom.js");
        // Получаем элемент select для типа недвижимости
        const typeSelect = document.querySelector('#id_type');
        // Получаем контейнер поля "количество этажей"
        const floorsField = document.querySelector('.field-number_of_floors');

        if (typeSelect && floorsField) {
            // Скрываем или показываем поле в зависимости от выбора
            if (typeSelect.value === 'apartment') {
                floorsField.style.display = '';  // Проверьте, правильно ли это строка 20
            } else {
                floorsField.style.display = 'none';
            }
        }
    }

    const typeSelect = document.querySelector('#id_type');
    console.log(typeSelect.valuex4);
    if (typeSelect) {
        console.log("1")
        typeSelect.addEventListener('change', {
        console.log('Change event triggered');
        toggleNumberOfFloorsField();
    });
        console.log("2")
    }

    toggleNumberOfFloorsField();
});
