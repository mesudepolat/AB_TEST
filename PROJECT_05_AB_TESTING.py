###########################################
# AB Testing for Facebook Bidding Strategies
############################################

# soru: müşterimiz mevcut iki teklif verme türünden hangisini tercih etmeli, hangisinden
# daha çok kazanç elde eder?


############################
# 1. Varsayım Kontrolü
############################

############################
# 1.1 Normallik Varsayımı
############################

# H0: Normal dağılım varsayımı sağlanmaktadır.
# H1:..sağlanmamaktadır.

import pandas as pd
from scipy.stats import shapiro

control = pd.read_excel("datasets/ab_testing_data.xlsx",
                        sheet_name="Control Group")

test = pd.read_excel("datasets/ab_testing_data.xlsx",
                     sheet_name="Test Group")

test_istatistigi, pvalue = shapiro(control["Purchase"])
print('Test İstatistiği = %.4f, p-değeri = %.4f' % (test_istatistigi, pvalue))
# p-value = 0.5891 --> H0 reddedilemez, varsayım sağlanır

test_istatistigi, pvalue = shapiro(test["Purchase"])
print('Test İstatistiği = %.4f, p-değeri = %.4f' % (test_istatistigi, pvalue))
# p-value = 0.1541 --> H0 reddedilemez, varsayım sağlanır

############################
# 1.2 Varyans Homojenligi Varsayımı
############################

# H0: Varyanslar Homojendir
# H1: Varyanslar Homojen Değildir

from scipy import stats
stats.levene(control["Purchase"],
             test["Purchase"])
# p-value = 0.1082 --> H0 reddedilemez, varyanslar homojendir

############################
# 2. Hipotezin Uygulanması
############################

# H0: M1 = M2 (iki grup satın alma sayıları arasında ist ol.anl.fark yoktur.)
# H1: M1 != M2 (...vardır)

# varsayımlar sağlanıyor, bağımsız iki örneklem t testi(parametrik test) kullanacağız.
test_istatistigi, pvalue = stats.ttest_ind(control["Purchase"],
                                           test["Purchase"],
                                           equal_var=True)
print('Test İstatistiği = %.4f, p-değeri = %.4f' % (test_istatistigi, pvalue))
# p-value = 0.3493 --> H0 reddedilemez,iki grup satın alma sayıları arasında ist ol.anl.fark yoktur.


# Görselleştirme

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


control = pd.read_excel("datasets/ab_testing_data.xlsx",
                        sheet_name="Control Group")

test = pd.read_excel("datasets/ab_testing_data.xlsx",
                     sheet_name="Test Group")

control["Group"] = "Control"
test["Group"] = "Test"
Data = pd.concat([control, test], ignore_index=True)
sns.boxplot(x="Group", y="Purchase", data=Data)
plt.show()
