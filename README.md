# softwareEngineering

Для того чтобы установить зависимости для проекта нужно выполнить команду относительно корневой директории проекта:
```
pip install -r requirements.txt
```


Для того чтобы запустить сервер нужно выполнить команду: 
```
uvicorn api:app
```

Для того чтобы при запуске передать путь к файлу с переменным окружением можно выполнить такую команду:

```
uvicorn --env-file путь_к_файлу api:app
```