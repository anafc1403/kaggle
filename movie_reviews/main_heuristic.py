import load_data

print "base_training"
train_dicts = load_data.load_base_training()
#dict=load_data.parse_dict(train_dicts,False)
dict=load_data.create_corpus(train_dicts,media=True, moda=False,mediana=False)
#load_data.get_sentimental_value(train_dicts,dict)

print "test"
test_array = load_data.load_base_test()

test_prediction=load_data.get_sentimental_value(test_array,dict,media=True, moda=False,mediana=False)

load_data.write_submission(test_prediction)

