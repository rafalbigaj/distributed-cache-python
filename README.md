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

#### `etcd.config.json`

Dane dostępowe do bazy etcd udostępnione na kanale slack: https://join.slack.com/t/ibm-agh-labs/shared_invite/zt-e8xfjgtd-8IDWmn912qPOflbM1yk6~Q
należy umieścić w pliku: `instance/etcd.config.json`. 
Ten krok jest wymagany w celu poprawnej konfiguracji aplikacji lokalnej i przed dostarczeniem do chmury. 

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

- aplikację można uruchomić w dowolnej liczbie kopii (maksymalnie 64)
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

Informacje na temat uruchomionych aplikacji są także dostępne pod adresem:
https://cloud.ibm.com/cloudfoundry/public

### Testowanie w IBM Cloud

Aplikacja testująca po dostarczeniu do IBM Cloud jest dostępna pod adresem wskazanym na liście aplikacji.
W przykłądzie z poprzedniej sekcji jest to `locust-timely-swan.eu-de.mybluemix.net`.

Pod wskazanym adresem, aby uruchomić test należy podać następujące parametry:

- "Number of total users to simulate" - ilość symulowanych użytkowników - np. `40`
- "Hatch rate" - ilość użytkowników uruchamianych na sekundę - np. `10`
- "Host" - adres właściwej aplikacji - np. `https://distributed-cache-friendly-gnu.eu-de.mybluemix.net`

Oczekiwany rezultat wykonania testu powinien wyglądać podobnie jak w tabeli poniżej:

| Type   | Name                                            | # requests | # failures | Median response time | Average response time | Min response time | Max response time |
| -----  | -----                                           | -----      | -----      | -----                | -----                 | -----             | -----             |
|        |                                                 |            |            |                      |                       |                   |                   |
| DELETE | /config/performance_tests/<key>                 | 40         | 0          | 51                   | 55                    | 30                | 134               |
| PUT    | /config/performance_tests/<key>                 | 80         | 0          | 73                   | 88                    | 34                | 484               |
| GET    | /config/performance_tests/<key>?use_cache=false | 612        | 0          | 49                   | 64                    | 27                | 691               |
| GET    | /config/performance_tests/<key>?use_cache=true  | 625        | 0          | 38                   | 47                    | 19                | 424               |
|        | Aggregated                                      | 1357       | 0          | 45                   | 57                    | 19                | 691               |


### Dostęp do danych uruchomionej aplikacji w IBM Cloud

IBM Cloud udostępnia narzędzia do śledzenia wykonania aplikacji, dostępu do logów, a także możliwość zalogowania
się do kontenera z aplikacją przy pomocy `ssh`.

Poniżej zebraliśmy kilka przydatnych komend dostępnych w IBM Cloud CLI.
`distributed-cache` w tych przykładach jest nazwą Twojej aplikacji CloudFoundry.

#### Pobierz informację o detalach aplikacji oraz uruchomionych kontenerach (instancjach)

```shell script
ibmcloud cf app distributed-cache
```

Przykładowa odpowiedź:

```
Invoking 'cf app distributed-cache'...

Showing health and status for app distributed-cache in org rafal.bigaj@pl.ibm.com / space test as rafal.bigaj@pl.ibm.com...

name:              distributed-cache
requested state:   started
routes:            distributed-cache-friendly-gnu.eu-de.mybluemix.net
last uploaded:     Wed 06 May 23:57:30 CEST 2020
stack:             cflinuxfs3
buildpacks:        python

type:           web
instances:      4/4
memory usage:   256M
     state     since                  cpu    memory          disk           details
#0   running   2020-05-07T06:35:06Z   6.4%   67.2M of 256M   304.6M of 1G   
#1   running   2020-05-07T06:35:42Z   8.2%   69.1M of 256M   276.4M of 1G   
#2   running   2020-05-07T06:35:07Z   6.5%   67.6M of 256M   276.4M of 1G   
#3   running   2020-05-07T06:35:04Z   4.5%   65.3M of 256M   276.4M of 1G
```

Istnieje także możliwość śledzenia logów w osobnym serwisie LogDNA (**opcjonalne**):
https://cloud.ibm.com/docs/services/Log-Analysis-with-LogDNA?topic=LogDNA-monitor_cfapp_logs


#### Pobierz informację o detalach aplikacji oraz uruchomionych kontenerach (instancjach)

```shell script
ibmcloud cf app distributed-cache
```

Przykładowa odpowiedź:

```
Invoking 'cf app distributed-cache'...

Showing health and status for app distributed-cache in org rafal.bigaj@pl.ibm.com / space test as rafal.bigaj@pl.ibm.com...

name:              distributed-cache
requested state:   started
routes:            distributed-cache-friendly-gnu.eu-de.mybluemix.net
last uploaded:     Wed 06 May 23:57:30 CEST 2020
stack:             cflinuxfs3
buildpacks:        python

type:           web
instances:      4/4
memory usage:   256M
     state     since                  cpu    memory          disk           details
#0   running   2020-05-07T06:35:06Z   6.4%   67.2M of 256M   304.6M of 1G   
#1   running   2020-05-07T06:35:42Z   8.2%   69.1M of 256M   276.4M of 1G   
#2   running   2020-05-07T06:35:07Z   6.5%   67.6M of 256M   276.4M of 1G   
#3   running   2020-05-07T06:35:04Z   4.5%   65.3M of 256M   276.4M of 1G
```

#### Pobierz log-i wyprodukowane przez aplikację

Pobierz ostatnie log-i:

```shell script
cf logs distributed-cache --recent
```

Nasłuchuj na log-i w czasie rzeczywistym:

```shell script
cf logs distributed-cache
```

Przykładowa odpowiedź:

```
Invoking 'cf logs distributed-cache --recent'...

Retrieving logs for app distributed-cache in org rafal.bigaj@pl.ibm.com / space test as rafal.bigaj@pl.ibm.com...

   2020-05-11T08:24:40.91+0200 [RTR/0] OUT distributed-cache-friendly-gnu.eu-de.mybluemix.net - [2020-05-11T06:24:40.896696232Z] "GET /config/performance_tests/ICrqWHBnmVnALxtKSalwmKerDgsZpkiieeHqxxsPGWBCMvkBdFuigDeULbbXTuPH?use_cache=false HTTP/1.1" 200 0 5 "-" "python-requests/2.23.0" "10.85.78.52:40662" "149.81.69.221:61146" x_forwarded_for:"149.81.126.101, 10.85.78.52" x_forwarded_proto:"https" vcap_request_id:"28c9dbd5-ddcb-49d6-5797-e966ff378771" response_time:0.019545 gorouter_time:0.000389 app_id:"834ef717-00f0-4163-94f4-5cd5a9ac2b15" app_index:"0" x_global_transaction_id:"aad3dade5eb8efa82b6ac6cf" true_client_ip:"-" x_b3_traceid:"4a2896d28b0aa209" x_b3_spanid:"4a2896d28b0aa209" x_b3_parentspanid:"-" b3:"4a2896d28b0aa209-4a2896d28b0aa209"
   2020-05-11T08:24:40.91+0200 [RTR/0] OUT
   ... 

```

#### Dostęp do aplikacji przy pomocy `ssh`

```shell script
ibmcloud cf ssh distributed-cache
```

Przykładowa odpowiedź:
```
Invoking 'cf ssh distributed-cache'...

vcap@ef20c9ca-9cae-4194-4f4f-4844:~$ 
```

## Raport z wykonania zadania

W raporcie opisującym wykonanie zadania proszę o umieszczenie następujących informacji:

- wyniki testu trwającego 3 minuty i wykonanego lokalnie z wykorzystaniem aplikacji `locust` dla parametrów 
  "Number of total users to simulate" - 40 oraz "Hatch rate" - 10 
- wyniki testu trwającego 3 minuty i wykonanego na IBM Cloud z wykorzystaniem aplikacji `locust` dla parametrów 
  "Number of total users to simulate" - 40 oraz "Hatch rate" - 10
- wyjaśnienie rozbieżności w wynikach uruchomionych lokalnie oraz w chmurze
- odpowiedź z komendy `ibmcloud target` uruchomionej na Państwa koncie
- odpowiedź z komendy `ibmcloud cf app distributed-cache` uruchomionej dla Państwa aplikacji
- odpowiedź z komendy `ibmcloud cf logs distributed-cache --recent | head -n 20` uruchomionej dla Państwa aplikacji