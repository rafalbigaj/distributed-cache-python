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

### Dostarczanie do IBM Cloud

W celu dostarczenia Twojej aplikacji do IBM Cloud wymagana jest rejestracja.
Dla studentów i pracowników naukowych oferujemy specjalne kody promocyjne, które pozwalają na pracę z większą ilością
serwisów w chmurze.

Procedura rejestracji:
https://ibm.box.com/shared/static/nw3ednr2c43gzaw4gj1yl1ak0jgv1qkg.pptx

Posiadanie konta umożliwia zainstalowanie narzędzi CLI potrzebnych do dostarczenia aplikacji:
https://cloud.ibm.com/docs/cli?topic=cloud-cli-getting-started

Oraz rozszerzenia `cloud foundry`:
```shell script
ibmcloud cf install
```

Następny krok to logowanie do IBM Cloud przy użyciu komendy:
```shell script
ibmcloud login -r eu-de --sso
```

Proszę zwróć uwagę na region: `eu-de` (Frankfurt). Jego wybór jest potrzebny, ponieważ udostępniona baza etcd
znajduje się właśnie w tym regionie.

Następnie należy wybrać dalsze parametry, gdzie aplikacja będzie umieszczona:

```shell script
ibmcloud target --cf
```

Poprawność logowania możesz sprawdzić przy pomocy komendy:

```shell script
ibmcloud target

                      
API endpoint:      https://cloud.ibm.com   
Region:            eu-de   
User:              rafal.bigaj@pl.ibm.com   
Account:           Rafal Bigaj's Account (a34b4e9ea7ab66770e048caf83277971) <-> 1729119   
Resource group:    No resource group targeted, use 'ibmcloud target -g RESOURCE_GROUP'   
CF API endpoint:   https://api.eu-de.cf.cloud.ibm.com (API version: 2.147.0)   
Org:               rafal.bigaj@pl.ibm.com   
Space:             test
```

Przed dostarczenie aplikacji należy jeszcze uzupełnić plik `manifest.yml` w sekcji `env` ustalając wartość zmiennej: `USER_KEY_PREFIX`,
która będzie wykorzystywana jako prefiks wszystkich kluczy. Wartość ta powinna być unikalna dla każdego studenta.

Ostatecznie jesteś gotowy, żeby uruchomić komendę:

```shell script
ibmcloud cf push
```

Poprawność doostarczenia można zweryfikować komendą:

```shell script
ibmcloud cf apps

Invoking 'cf apps'...

Getting apps in org rafal.bigaj@pl.ibm.com / space test as rafal.bigaj@pl.ibm.com...
OK

name                            requested state   instances   memory   disk   urls
distributed-cache               started           4/4         256M     1G     distributed-cache-friendly-gnu.eu-de.mybluemix.net
locust                          started           1/1         256M     1G     locust-timely-swan.eu-de.mybluemix.net
```

Powyższy przykład pokazuje dwie aplikacje `distributed-cache` oraz `locust`. Pierwsza z nich to właściwa aplikacja
z implementacją API do rozproszonej pamięci podręcznej, druga to aplikacja do uruchomienia testów.

### Testowanie w IBM Cloud

Aplikacja testująca po dostarczeniu do IBM Cloud jest dostępna pod adresem wskazanym na liście aplikacji.
W przykłądzie z poprzedniej sekcji jest to `locust-timely-swan.eu-de.mybluemix.net`.

Pod wskazanym adresem, aby uruchomić test należy podać następujące parametry:

- "Number of total users to simulate" - ilość symulowanych użytkowników - np. `40`
- "Hatch rate" - ilość użytkowników uruchamianych na sekundę - np. `10`
- "Host" - adres właściwej aplikacji - np. `https://distributed-cache-friendly-gnu.eu-de.mybluemix.net`

Oczekiwany rezultat wykonania testu powinnien wyglądać podobnie jak w tabeli poniżej:

| Type   | Name                                            | # requests | # failures | Median response time | Average response time | Min response time | Max response time |
| -----  | -----                                           | -----      | -----      | -----                | -----                 | -----             | -----             |
|        |                                                 |            |            |                      |                       |                   |                   |
| DELETE | /config/performance_tests/<key>                 | 40         | 0          | 51                   | 55                    | 30                | 134               |
| PUT    | /config/performance_tests/<key>                 | 80         | 0          | 73                   | 88                    | 34                | 484               |
| GET    | /config/performance_tests/<key>?use_cache=false | 612        | 0          | 49                   | 64                    | 27                | 691               |
| GET    | /config/performance_tests/<key>?use_cache=true  | 625        | 0          | 38                   | 47                    | 19                | 424               |
|        | Aggregated                                      | 1357       | 0          | 45                   | 57                    | 19                | 691               |
