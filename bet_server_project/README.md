Для начала работы выполнить:
1) virtualenv -p /usr/bin/python3.4 env
2) source env/bin/activate
3) pip install -r requirements.txt

API доступно по адресу $(server_address)/api/
На данный момент есть:
- GET и POST для получения списка bets и добавления новой соответственно: $(server_address)/api/bets/
- GET и DELETE для получения и удаления конкретной bet по id: $(server_address)/api/bets/$(some_id)
