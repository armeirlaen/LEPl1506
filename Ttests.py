import scipy.stats
import statsmodels.formula.api
import statsmodels.api
import pandas as pd
import numpy as np

upDom = [0.0071974201529609845, 0.004833870192991187, 0.004215239756115963, -0.001956668932304979, -0.03682428339500825]
upNonDom = [0.002829889191621743, -0.0044899444531327475, 0.0023478263919331456, -0.0449824300916208, 0.022308628250713215]
downDom = [0.0029257424545179483, 0.01664989898374193, -0.007685026406955877, 0.000293901486249049, -0.007721514102349619]
downNonDom = [-0.005912868971889528, -0.013184480370751825, -0.023098622942187147, -0.0637486268382845, 0.023884005700257734]
datanp = np.array([upDom,upNonDom,downDom,downNonDom])

print("LESS:")
print("Rel up",scipy.stats.ttest_rel(upDom, upNonDom,alternative='less'))
print("Rel down",scipy.stats.ttest_rel(downDom, downNonDom,alternative='less'))

print("GREATER")
print("Rel up",scipy.stats.ttest_rel(upDom, upNonDom,alternative='greater'))
print("Rel down",scipy.stats.ttest_rel(downDom, downNonDom,alternative='greater'))


data = pd.DataFrame({'upg':datanp[0],'upb':datanp[1],'dwg':datanp[2],'dwb':datanp[3]})
data1 = pd.DataFrame({'Up':np.concatenate((datanp[0],datanp[1])),'Down':np.concatenate((datanp[2],datanp[3]))})
data2 = pd.DataFrame({'GH':np.concatenate((datanp[0],datanp[2])),'BH':np.concatenate((datanp[1],datanp[3]))})
data3 = pd.DataFrame({'Dup': datanp[0]-datanp[2],'Ddw':datanp[1]-datanp[3]})
fit = statsmodels.formula.api.ols('Up ~ Down ', data1).fit()
table = statsmodels.api.stats.anova_lm(fit)
print('Test anova H0 : LFup = LFdown \n',table)

fit = statsmodels.formula.api.ols('GH ~ BH ', data2).fit()
table = statsmodels.api.stats.anova_lm(fit)
print('Test anova H0 : LF_ MD  = LF_MnD \n',table)

fit = statsmodels.formula.api.ols('Dup ~ Ddw ', data3).fit()
table = statsmodels.api.stats.anova_lm(fit)
print('Test anova H0 : [LF_ MD - LF_MnD]up = LF_MD - LF_MnD]down \n',table)
