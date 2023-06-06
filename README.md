## Практика 2. Клиент-серверное приложение для игры в мафию на основе gRPC

Сафонова Елизавета, БПМИ-206

-------

### Структура

Следующие команды запускают все контейнеры:

```
docker compose build
docker compose up -d
```

При этом запускается один сервер и 8 клиентов-ботов, и проводятся две игры по 4 игрока: мафия, комиссар и два мирных жителя. Ход игры, действия каждого игрока и результат игры можно посмотреть в выводе каждого контейнера, например, с помощью Docker Desktop.

### Часть «Привет Мафия»

На порте 50051 запускается сервер, к нему могут подключаться клиенты. Имя клиента можно задать аргументом командной строки (можно изменить в docker compose), или вручную при работе с программой, если оставить аргумент пустым. Имена должны быть различны. Заданные в docker compose имена клиентов: "1", ... "8". Клиенту при подключении приходит приветствие и номер сессии игры, далее он получает уведомления о подключившихся к той же сессии игроках. Клиент печатает в выводе все поступившие уведомления:

```
Hello, <Name>   // приветствие
<Name> joined   // уведомления о подключившихся игроках
```

### Часть «Боты мафии»

После того, как к серверу подключились 4 игрока, начинается новая сессия игры. Следующие 4 игрока попадают в следующую сессию и начинается еще одна игра и так далее. Сервер распределяет роли между участниками сессии, и уведомляет клиентов об их ролях. Игра автоматически начинается с нулевой ночи, и нулевой день пропускается, т.к. все игроки боты, и голосования в нулевой день не происходит. Каждый из игроков определяет действия случайным образом в рамках своей роли. При окончании игры всем клиентам приходит уведомление о ее завершении и о том, кто выиграл.

Сервер печатает в выводе уведомление о начале сессии, выборе игроков и конце игры. Клиент печатает в выводе все полученные уведомления и свои действия. Примеры:

```
<Name>, you are <Role>   // уведомление игрока о его роли (ghost - в роли духа)
Day/Night <Number>       // уведомление о начале дня или ночи
<Name> killed            // уведомление об убийстве игрока мафией
<Name> executed          // уведомление о казни игрока общим голосованием
Chose to execute <Name>  // игрок проголосовал за казнь игрока <Name>
Game over                // уведомление о завершении игры
и так далее
```
