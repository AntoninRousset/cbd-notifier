# CBD notifier

Initialize the database
```sh
python -m cbd_notifier init
```

Add topics
```sh
python -m cbd_notifier add-topic COP16 'https://api.cbd.int/api/v2016/meetings/COP-16/documents'
python -m cbd_notifier add-topic COP16 'https://api.cbd.int/api/v2013/index?q=meeting_ss:COP-16&rows=9999'
python -m cbd_notifier add-topic COP16 'https://api.cbd.int/api/v2021/meeting-interventions?q={%22conferenceId%22:{%22$oid%22:%2265b92d8e85ae8044fbf24c40%22}}'
```

Run the bot
```sh
python -m cbd_notifier run
```
