# Notes

1. `django_vue_cli` is the main django module
   1. `django_vue_cli.urls` is used as main url
2. all secondary apps (modules) are under `applications/`
3. django.settings is used
4. Database is sqlite3 and file is stored in `BASE_DIR/db.sqlite3`
5. state management through `vuex`
6. frontend call api through axios
7. form validation through `vee-validate`
8. `component/music_tag` includes all music file formats
9. `component/mz` is all musicbrainz details
10. `component/utils/exceptions.py` includes all the application exceptions
11. `component/zhconv` converts between chinese characters
