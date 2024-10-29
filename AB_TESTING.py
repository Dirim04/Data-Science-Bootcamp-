#####################################################
# AB Testi ile BiddingYöntemlerinin Dönüşümünün Karşılaştırılması
#####################################################

#####################################################
# İş Problemi
#####################################################

# Facebook kısa süre önce mevcut "maximumbidding" adı verilen teklif verme türüne alternatif
# olarak yeni bir teklif türü olan "average bidding"’i tanıttı. Müşterilerimizden biri olan bombabomba.com,
# bu yeni özelliği test etmeye karar verdi veaveragebidding'in maximumbidding'den daha fazla dönüşüm
# getirip getirmediğini anlamak için bir A/B testi yapmak istiyor.A/B testi 1 aydır devam ediyor ve
# bombabomba.com şimdi sizden bu A/B testinin sonuçlarını analiz etmenizi bekliyor.Bombabomba.com için
# nihai başarı ölçütü Purchase'dır. Bu nedenle, istatistiksel testler için Purchasemetriğine odaklanılmalıdır.

#####################################################
# Veri Seti Hikayesi
#####################################################

# Bir firmanın web site bilgilerini içeren bu veri setinde kullanıcıların gördükleri ve tıkladıkları
# reklam sayıları gibi bilgilerin yanı sıra buradan gelen kazanç bilgileri yer almaktadır.Kontrol ve Test
# grubu olmak üzere iki ayrı veri seti vardır. Bu veri setleriab_testing.xlsxexcel’ininayrı sayfalarında yer
# almaktadır. Kontrol grubuna Maximum Bidding, test grubuna AverageBiddinguygulanmıştır.

# impression: Reklam görüntüleme sayısı
# Click: Görüntülenen reklama tıklama sayısı
# Purchase: Tıklanan reklamlar sonrası satın alınan ürün sayısı
# Earning: Satın alınan ürünler sonrası elde edilen kazanç

#####################################################
# Proje Görevleri
#####################################################

######################################################
# AB Testing (Bağımsız İki Örneklem T Testi)
######################################################

# 1. Hipotezleri Kur
# 2. Varsayım Kontrolü
#   - 1. Normallik Varsayımı (shapiro)
#   - 2. Varyans Homojenliği (levene)
# 3. Hipotezin Uygulanması
#   - 1. Varsayımlar sağlanıyorsa bağımsız iki örneklem t testi
#   - 2. Varsayımlar sağlanmıyorsa mannwhitneyu testi
# 4. p-value değerine göre sonuçları yorumla
# Not:
# - Normallik sağlanmıyorsa direkt 2 numara. Varyans homojenliği sağlanmıyorsa 1 numaraya arguman girilir.
# - Normallik incelemesi öncesi aykırı değer incelemesi ve düzeltmesi yapmak faydalı olabilir.




#####################################################
# Görev 1:  Veriyi Hazırlama ve Analiz Etme
#####################################################
import pandas as pd
import numpy as np
import itertools
import matplotlib.pyplot as plt
import seaborn as sns
pip install statsmodels
from scipy.stats import shapiro, levene, ttest_1samp, mannwhitneyu, pearsonr, spearmanr, kendalltau, kruskal, f_oneway, ttest_ind
from statsmodels.stats.proportion import  proportions_ztest

pd.set_option('display.max_columns', None)
# pd.set_option('display.max_rows', None)
pd.set_option('display.width', 500)
# çıktının tek bir satırda olmasını sağlar.
pd.set_option('display.expand_frame_repr', False)

# Adım 1:  ab_testing_data.xlsx adlı kontrol ve test grubu verilerinden oluşan veri setini okutunuz. Kontrol ve test grubu verilerini ayrı değişkenlere atayınız.
df = pd.read_excel("C:\\Users\\Dirim\\Desktop\\ab_testing.xlsx")

control_group = pd.read_excel("C:\\Users\\Dirim\\Desktop\\ab_testing.xlsx", sheet_name="Control Group")
test_group = pd.read_excel("C:\\Users\\Dirim\\Desktop\\ab_testing.xlsx", sheet_name="Test Group")

# Adım 2: Kontrol ve test grubu verilerini analiz ediniz.

control_group.describe().T
test_group.describe().T

# Adım 3: Analiz işleminden sonra concat metodunu kullanarak kontrol ve test grubu verilerini birleştiriniz.

new_df = pd.concat([control_group, test_group], axis=1) # axis=1 değişkenleri yan yana dizdi, axis=0 değerleri alt alta dizerdi.
new_df.columns = ["Impression_C", "Click_C", "Purchase_C", "Earning_C", "Impression_T", "Click_T", "Purchase_T", "Earning_T"]


#####################################################
# Görev 2:  A/B Testinin Hipotezinin Tanımlanması
#####################################################

# Adım 1: Hipotezi tanımlayınız.
# H0: M1 = M2
# H1: M1 != M2

# Adım 2: Kontrol ve test grubu için purchase(kazanç) ortalamalarını analiz ediniz
control_mean = new_df["Purchase_C"].mean()
test_mean = new_df["Purchase_T"].mean()

#####################################################
# GÖREV 3: Hipotez Testinin Gerçekleştirilmesi
#####################################################

######################################################
# AB Testing (Bağımsız İki Örneklem T Testi)
######################################################

# Adım 1: Hipotez testi yapılmadan önce varsayım kontrollerini yapınız.Bunlar Normallik Varsayımı ve Varyans Homojenliğidir.
# Kontrol ve test grubunun normallik varsayımına uyup uymadığını Purchase değişkeni üzerinden ayrı ayrı test ediniz.

##### Normallik Varsayımı

# H0: Normal dağılım varsayımı sağlanmaktadır
# H1: Sağlanmamaktadır

# Kontrol grubu:
test_stat_C, pvalue_C = shapiro(new_df["Purchase_C"])
print("Kontrol Grubu \nTest Stat = %.4f, p-value = %.4f" % (test_stat_C, pvalue_C)) # pvalue = 0.5891 pvalue > 0.05 REDDEDİLEMEZ

# Test grubu:
test_stat_T, pvalue_T = shapiro(new_df["Purchase_T"])
print("Test Grubu \nTest Stat = %.4f, p-value = %.4f" % (test_stat_T, pvalue_T)) # pvalue = 0.1541 > 0.05 REDDEDİLEMEZ


#### Varyans Homojenliği

# H0: Varyanslar homojendir.
# H1: Varyanslar homojen değildir.

# Kontrol grubu:
test_stat, pvalue = levene(new_df["Purchase_C"], new_df["Purchase_T"])
print("Levene Testi \nTest Stat = %.4f, p-value = %.4f" % (test_stat, pvalue)) # PVALUE = 0.10 > 0.05 REDDEDİLEMEZ

# Adım 2: Normallik Varsayımı ve Varyans Homojenliği sonuçlarına göre uygun testi seçiniz

# Varsayımlar sağlanıyor --> Parametrik Test

test_stat, pvalue = ttest_ind( new_df["Purchase_C"], new_df["Purchase_T"], equal_var=True) # True çünkü levene testinde H0 REDDEDİLEMEZ çıktı.
print("Parametrik Test \nTest Stat = %.4f, p-value = %.4f" % (test_stat, pvalue))
# pvalue = 0.3493 > 0.05 --> H0 REDDEDİLEMEZ.

# Adım 3: Test sonucunda elde edilen p_value değerini göz önünde bulundurarak kontrol ve test grubu satın alma
# ortalamaları arasında istatistiki olarak anlamlı bir fark olup olmadığını yorumlayınız.

# H0 REDDEDİLEMEZ olduğundan ortalamalar arasında anlamlı bir fark yoktur diyebiliriz


##############################################################
# GÖREV 4 : Sonuçların Analizi
##############################################################

# Adım 1: Hangi testi kullandınız, sebeplerini belirtiniz.

# Parametrik test kullandım çünkü varsayım kontrolü yaptığımda normallik varsayımı ve varyans homojenliğinden
# reddedilemez sonucu geldi.

# Adım 2: Elde ettiğiniz test sonuçlarına göre müşteriye tavsiyede bulununuz.

# M1 = M2' dir iki ürün arasında anlamlı bir fiyat farkı yoktur, ikisi de alınabilir.

