DEV

descr:

Короче, задумка такая
Сделать сервис, в котором в реальном времени будет отображаться приготовление блюда
Туда в зависимости от того, как и что будет получаться, можно добавлять что-то
Например,если все супер идет - можно будет поиграться и маленькими очередями внутри больших очередей + приоритетностью очередей
Проще всего - это табло в маке

Ты заходишь на сайт и делаешь заказ (бургер+пицца+кола) -> это большая очередь задач
Потом ты хочешь смотреть, на каком этапе готовка каждой единицы (эта малая очередь задач)

------------------------------------------------------------------------------------

пока вот

1 на эндпоинт приходит пост запрос с моделью заказа, в которую вложены модели позиций
2 достаем позиции из бд в виде моделей и кладем в основной воркер
3 в основном воркере для каждой позиции вызываем свой воркер. можно сделать базовый воркер и передавать ему какую то структуру, где будут задачи индивидуально для каждой позиции, определенные в отдельном классе, наследующем от какого то базового
4 на отдельный эндпоинт каждые n сек отправляем гет запрос на получение статуса, чекаем статус текущего микроворкера(пока хз как это реализовать, наверное отдельный какой то модуль лучше сделать) и возвращаем его (можно красиво что то на фронте нарисовать в теории)
5 можно привязать к завершению работы основного воркера что то типа уведомления, just for fun


-------------------------------------------------------------------------------
константы для конфига пока что в .env, потом перенесем