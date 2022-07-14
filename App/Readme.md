# **YAPILACAKLAR LISTESI**
## Genel Yapılacaklar Listesi
- [x] Gitignore certs eklenicek. Klasör yapısını değiştirmişsin ama .gitignore düzenlememişsin.
- [x] Gerekli dosyalar [main kısmı eklenecek ](https://www.freecodecamp.org/news/if-name-main-python-example/#:~:text=We%20can%20use%20an%20if,name%20if%20it%20is%20imported.) 
- [x] Client, Server ve ReverseProxy için farklı TOML dosyaları oluşturulacak. Her biri kendine ait toml dosyasını okuyacak.
- [ ] [HaProxy](https://www.haproxy.com/) ve [NGINX](https://www.nginx.com/) araştırılıcak ve kurulumu yapılacak. ReverseProxynin önüne HaProxy kurulucak. Örnek bir NGINX kurulumu yapılacak ve ReverseProxy NGINX sunucusuna istek yapacak şekilde olacak.
## Örnek Client TOML Dosyası
```
title = "Client TOML Config File"
[ClientSettings]
URI = "http(s)://......" #Buraya Request isteğinin gideceği URI yazılacak 
NumberOfRequests = 1 #Buraya ReverseProxy kısmına kaç kere istek yapılacağı eklenecek
RequestMethod = "GET/POST/...." # Yapılacak olan requestin METHOD'u buraya yazılacak
EnableCustomHeader = true/false # Header ekleme özelliğini açıp/kapama
CustomHeaders = [["header-key","header-value"][...][...]] #Request yollanacağı zaman eklenecek olan
EnableCustomData = true/false # Body gönderme özelliğini açıp/kapama. Seçilen Methoda göre bu durumu göze almayacaksın. Örn RequestMethod "GET" ise BODY gönderme gibi bir işlem olamaz.
CustomData = "MyDataFolder/test.json" #Buraya datanın tutulduğu dosyanın full pathi yazılacak. Bu dosyanın içindeki datayı okuyup göndericek.
StreamMode = true/false #Stream mode açıp/kapama. Stream mode açık ise request ve response tarafındaki BODY kısımları buna uygun şekilde okunacak
```

### ReverseProxy Yapılacaklar Listesi
- [ ] Body ve Header Filter/Replacer kısmında refactor yapılacak. Nasıl bir yol izlenirse burada aynı işi yapan duplicate code sayısı düşürülür bakılacak. Request ve response genel olarak aynı şeyleri yapıyor tek farklılıkları config içinden okudukları alan isimi.
- [x] Filter ve Replacer özelliklerinin açılıp/kapanması TOML tarafına eklenecek ve gerekli geliştirilmeler yapılacak. 
- Filters tarafı; 
  - (Request/Response)BodyFilter = true/false
  - (Request/Response)HeaderFilter = true/false
  - InvalidMethodsFilter = true/false
  - InvalidQueryFilter = true/false
  - InvalidPathFilter = true/false
- Replacer Tarafı
    - (Request/Response)BodyReplacer = true/false
    - (Request/Response)HeaderReplacer = true/false
- [x] 46. satırdan itibaren başlayan request.method if checkleri kaldırılacak tek bir satırda halledilecek.
- [x] Argparser kısmında default değer verebilme özelliği var. Eğer kullanıcı programı çalıştırır iken --toml parametresini vermez ise ise o değer gelsin.
- [x] Filter/Replacer kısmında ...CaseSensitive isimleri => ...CaseInsensitive olarak değiştirilecek. Çünkü yaptıkları iş case-insensitiv
- [ ] Stream kısmı koda eklenecek.
- [x] Header check olayı case-insesitive olacak.
- [x] Request.py sertifika olayına gerek yok.
- [ ] Loggin kısmı biraz daha araştırılması lazım. Her seferinde log yazmak için basicconf çağırmaya gerek var mı?
