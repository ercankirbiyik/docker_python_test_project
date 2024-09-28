# DevOps in Test

Bu proje, Dockerize edilmiş bir Python test projesini ve Selenium Grid yapılandırmasını içerir. Ayrıca Jenkins kullanarak AWS EC2 üzerinde çalışan bir pipeline ile testler otomatik olarak yürütülmektedir. Proje, test sonuçlarını webhook.site gibi bir URL'ye gönderir.

## İçindekiler

1. [Proje Tanımı](#proje-tanımı)
2. [Kurulum Adımları](#kurulum-adımları)
3. [Jenkins Pipeline Yapılandırması](#jenkins-pipeline-yapılandırması)
4. [Test Sonuçlarını Görüntüleme](#test-sonuçlarını-görüntüleme)
5. [Dosya ve Kaynaklar](#dosya-ve-kaynaklar)

---

## Proje Tanımı

Bu proje, aşağıdaki işlemleri gerçekleştiren bir Python test projesini Dockerize eder:

1. **Dockerize Python Test Projesi**: Python test projesi Dockerfile ve docker-compose kullanılarak Dockerize edilmiştir.
2. **Dockerize Selenium Grid**: Selenium Grid, `selenium/hub` ve `selenium/node-chrome` imajları kullanılarak oluşturulmuştur.
3. **Python Test Çalıştırma Scripti**: Docker konteynerlerini çalıştırıp testleri node sayısı parametresi ile çalıştıran bir Python scripti yazılmıştır.
4. **AWS EC2 Üzerinde Jenkins Kurulumu**: AWS EC2'de t3.micro instance üzerinde Jenkins kurulumu yapılmış ve pipeline ile testler otomatik olarak çalıştırılmıştır.
5. **Test Sonuçlarının Webhook ile Gönderilmesi**: Test sonuçları, webhook.site gibi bir URL'ye gönderilmektedir.

---

## Kurulum Adımları

### 1. Dockerize Python Test Projesi

- Python test projesini Dockerize etmek için [Dockerfile](./Dockerfile) ve [docker-compose.yml](./docker-compose.yml) dosyalarını kullanın.
- Projeyi çalıştırmak için şu komutu çalıştırın:

```bash
docker-compose up
```

### 2. Selenium Grid Yapılandırması
- Selenium Grid için selenium/hub ve selenium/node-chrome imajları kullanıldı.
- Selenium Grid'i başlatmak için şu komutu çalıştırın:

```bash
docker-compose -f selenium-grid-compose.yml up
```

### 3. Python Test Scripti Çalıştırma
Test scriptini çalıştırmak için şu komutu kullanın:

```bash
python3 run_tests.py <node_count>
```
- node_count: Çalıştırılacak Chrome node sayısını belirtir (1 ile 5 arasında bir değer olabilir).


### 4.AWS EC2 Üzerinde Jenkins Kurulumu
- AWS EC2 üzerinde t3.micro instance oluşturun ve aşağıdaki komutları kullanarak Jenkins'i kurun:

```bash
sudo apt update
sudo apt install openjdk-8-jdk
wget -q -O - https://pkg.jenkins.io/debian/jenkins.io.key | sudo apt-key add -
sudo sh -c 'echo deb http://pkg.jenkins.io/debian-stable binary/ > /etc/apt/sources.list.d/jenkins.list'
sudo apt update
sudo apt install jenkins
```
- Jenkins, 8080 portu üzerinden erişilebilir olacaktır.

### 5. Sudo Yetkisini Jenkins Kullanıcısına Vermek
- Jenkins kullanıcısına parolasız sudo yetkisi vermek için şu komutu çalıştırın

```bash
sudo visudo
```
- Açılan dosyanın sonuna şu satırı ekleyin:

```bash
jenkins ALL=(ALL) NOPASSWD: ALL
```

- Control + O ile kaydedin ve Control + X ile komut satırını kapatın

### 6. Pipeline Konfigürasyonu
- Jenkins web arayüzünde bir pipeline oluşturun ve Jenkinsfile dosyasını kullanarak pipeline'ı yapılandırın.
- Pipeline parametrelerini ayarlayın: Build_Name ve node_count.

#### Jenkins Pipeline Yapılandırması
Jenkins Pipeline yapısında aşağıdaki aşamalar bulunmaktadır:

1. Install Dependencies: Python ve gerekli paketlerin kurulumu yapılır.
2. Run Tests: Testler, verilen node sayısına göre çalıştırılır.
3. Send Test Results: Test sonuçları webhook.site sitesine gönderilir.

Test Sonuçlarını Görüntüleme
Test sonuçları, otomatik olarak webhook.site(https://webhook.site/#!/view/5120da85-4b4d-4d06-9fe3-11f5eacfcc93/dbb53b47-9c45-4467-9700-e16bed333db2/1) adresine gönderilir. 

### Dosya ve Kaynaklar
Dockerfile
docker-compose.yml
Jenkinsfile

### Sonuçlar
Bu proje sonucunda elde edilen çıktıların listesi:

1. VCS Bağlantısı: Proje ve script dosyalarını görmek için bir VCS (GitHub) bağlantısı.
   * GitHub Projesi (https://github.com/ercankirbiyik/docker_python_test_project)

2. Jenkins URL: Jenkins üzerinden job'ınızı tetiklemek ve izlemek için bir bağlantı.
   * Jenkins Pipeline URL (http://16.171.148.111:8080/job/python_test_project/)

3. Webhook.site URL: Test sonuçlarını görmek için webhook.site üzerinden sonuçlara ulaşabilirsiniz.
   * Webhook Test Sonuçları (https://webhook.site/b8f12633-2a84-4e1c-9950-a76fa8ab8c66)