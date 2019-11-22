import pandas as pd
from statsmodels.tsa.arima_model import ARMA
import warnings
warnings.filterwarnings("ignore")
import datetime
file_place='D:\\'
df_store=pd.read_csv(file_place+'Quantify\\factor\\factor_alpha_2019.csv')
code=[]
p=[]
pre_a=[]
cal_len2=30
date1=[]
coeff=[]
for group in df_store.groupby(['code']):
    code_store=group[0]
  #  print(group[0])#输出股票代码，提示进度
    g=group[1]#每一个股票的数据
    roll_len2 = len(g) - cal_len2##滚动长度
    for i in range(0, roll_len2+1):
        g1 = g.iloc[0 + i:cal_len2 + i, :]
        if g1["p"].mean()<0.05:
            model = ARMA(g1['alpha_c'], order=(1,0,0))
            result_arma = model.fit(disp=-1, method='css')
            predict = result_arma.predict()
            co=result_arma.params.iloc[1]
            predict = predict.iloc[0]
            if predict>0 and co>=0.75:
                print(group[0])
                code.append(group[0])
                coeff.append(co)
                #print(g1['p'].mean())
                p.append(g1['p'].mean())
                pre_a.append(predict)
                date1.append(g1.iloc[cal_len2-1, 1])
        else:
            continue
df_alpha = pd.DataFrame({'code': code,'date':date1,'p': p, 'pre_a': pre_a,'coeff': coeff})
df_alpha['date'] = [datetime.datetime.strptime(x, '%Y/%m/%d') for x in df_alpha['date']]
df_alpha['date'] = [datetime.datetime.strftime(x, '%Y/%m/%d') for x in df_alpha['date']]
df_alpha=df_alpha.sort_values(by=['date','pre_a'],ascending=(True,False))
alpha = pd.DataFrame(columns=['code','date','p', 'pre_a','coeff'])
for group in df_alpha.groupby(['date']):
    g=group[1]
    g=[ g.iloc[0:2,:] if len(g)>=2 else g ]
    alpha =alpha.append(g)
print(alpha)
alpha.to_csv(file_place + 'Quantify\\factor\\factor_alpha_predict.csv', header=True, index=False)
