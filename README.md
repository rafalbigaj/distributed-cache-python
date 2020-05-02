# Rozproszona pamięć podręczna z wykorzystaniem Etcd

## Laboratorium - NoSQL - zadanie domowe

Repozytorium zawiera kod aplikacji [`flask`](https://flask.palletsprojects.com/), która implementuje
interfejs [`REST`](https://en.wikipedia.org/wiki/Representational_state_transfer) pozwalający na wykonanie akcji:
- `POST /config/<key>` - ustawienie wartości dla danego klucza
- `GET /config/<key>` - popranie wartości danego klucza
- `DELETE /config/<key>` - usunięcie klucza

### Przed rozpoczęciem zadania

Aby rozpocząć pracę z kodem musisz mieć środowisko python 3.6 z zainstalowanymi zależnościami przy pomocy komendy:

```shell script
pip install -r requirements.txt
```

Zawartość repozytorium:

- `instance/etcd.config.json` - plik konfiguracyjny do udostępnionej w trakcie laboratorium bazy etcd
- `manifest.yml` i `runtime.txt` - pliki zawierające konfigurację aplikacji [Cloud Foundry w IBM Cloud](https://cloud.ibm.com/docs/cloud-foundry-public?topic=cloud-foundry-public-creating_cloud_foundry_apps)
- `app.py` - interfejs `REST` - aplikacja `flask`
- `etcd_client.py` - klient etcd oparty na [`python-etcd3`](https://python-etcd3.readthedocs.io/en/latest/)
- `distributed_cache.py` - szkielet kodu rozproszonej pamięci podręcznej **do uzupełnienia**
- `locustfile.py` - testy wykonane z wykorzystanie narzędzia [`locust`](https://locust.io/)
- `requirements.txt` - plik z wymaganymi pakietami

### Zadanie

Zaimplementuje klasę `DistributedCache` zgodnie ze szkieletem dostępnym w pliku `distributed_cache.py`, 
która umożliwia na:

- wpisanie wartości klucza do rozporoszonej pamięci podręcznej przy pomocy metody `put`
- usunięcie klucza z rozporoszonej pamięci podręcznej przy pomocy metody `delete`
- pobranie wartości klucza z rozporoszonej pamięci podręcznej przy pomocy metody `get`

Ostatnia metoda `get` powinna działać w dwóch wariantach:

- zwracać wartość przechowywaną w pamięci procesu, gdy argument `use_cache` ma wartość `True`
- zwracać wartość bezpośrednio z bazy etcd, gdy argument `use_cache` ma wartość `False`

Wymagania:

- aplikację moźna uruchomić w dowolnej liczbie kopii (maksymalnie 64)
- każda instancja aplikacji zapewnia dostęp do tych samych danych
- wartość klucza wpisana w jednej instancji może być odczytana z innej
- procesy aplikacji przechowują wartości kluczy w pamięci operacyjnej
- procesy synchronizują wartości kluczy pomiędzy sobą

### Uruchomienie lokalne

W celu uruchomienia aplikacji na własnej maszynie należy wpisać komendę:

```shell script
python app.py
```

Aplikacja po uruchomieniu jest dostępna pod adresem: `http://0.0.0.0:8080`.

### Testowanie lokalne

W celu uruchomienia testów należy uruchomić komendę, która uruchomi aplikację testującą:

```shell script
locust
```

Aplikacja testująca po uruchomieniu jest dostępna pod adresem: `http://0.0.0.0:8089`.

Pod wskazanym adresem, aby uruchomić test należy podać następujące parametry:

- "Number of total users to simulate" - ilość symulowanych użytkowników - np. `40`
- "Hatch rate" - ilość użytkowników uruchamianych na sekundę - np. `10`
- "Host" - adres właściwej aplikacji - np. `http://0.0.0.0:8080`

### Dostarczania do IBM Cloud

TBD

### Testowanie w IBM Cloud

TBD

