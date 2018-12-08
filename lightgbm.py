# coding: utf-8
# pylint: disable = invalid-name, C0111
import lightgbm as lgb
import pandas as pd

print('Loading data...')
train_data = pd.read_csv('train_org.csv')   # 读取数据
header = ['service_type', 'is_mix_service', 'online_time', 'many_over_bill',
          'contract_type', 'contract_time', 'is_promise_low_consume',
          'net_service', 'pay_times', 'gender', 'age', 'complaint_level', 'former_complaint_num',
          'current_service']
train_data[header] = train_data[header].astype(int)

dict = {89950166: 0, 89950167: 1, 89950168: 2, 90063345: 3, 90109916: 4, 90155946: 5,
        99999825: 6, 99999826: 7, 99999827: 8, 99999828: 9, 99999830: 0}
reversedict = {0: 89950166, 1: 89950167, 2: 89950168, 3: 90063345, 4: 90109916, 5: 90155946,
               6: 99999825, 7: 99999826, 8: 99999827, 9: 99999828, 10: 99999830}

# train_data.pop('user_id')
ty = train_data.pop('current_service')
ty = ty.astype(int)
y = [dict[x] for x in ty]

train = lgb.Dataset(train_data, label=y)

# specify your configurations as a dict
params = {
    'boosting_type': 'gbdt',
    'objective': 'multiclass',
    'metric': 'multi_logloss',
    'num_class': 10,
    'num_leaves': 1000,
    'learning_rate': 0.05,
    'feature_fraction': 0.9,
    'bagging_fraction': 0.8,
    'bagging_freq': 5,
    'verbose': 0
}

print('Starting training...')
# train
gbm = lgb.train(params,
                train,
                num_boost_round=300)

print('Saving model...')
# save model to file
gbm.save_model('model.txt')

"""
print('Starting predicting...')
# predict
y_pred = gbm.predict(valid_x, num_iteration=gbm.best_iteration)
temp_result = [y.argmax() for y in y_pred]

cnt1 = 0
cnt2 = 0
for i in range(len(valid_y)):
    if temp_result[i] == valid_y[i]:
        cnt1 += 1
    else:
        cnt2 += 1

print("Accuracy: %.2f %% " % (100 * cnt1 / (cnt1 + cnt2)))


final_result = [reversedict[x] for x in temp_result]
"""
