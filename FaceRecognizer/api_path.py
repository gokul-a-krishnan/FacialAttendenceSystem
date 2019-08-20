image_path = '../data/'  # Change where you want to store Scanned Images

classifier_path = '../classifiers/'  # Set Directory to Classifiers
classifiers = {'face': "face.xml"}  # Add Classifiers

__config_path = '../config/'  # Change where  data files to be stored
total_bin = __config_path + 'total.bin'  # test to store as Binary
names_bin = __config_path + 'names.bin'
data_bin = __config_path + 'data.bin'

__server_path = '../serve/'
names_json = __server_path + 'names.json'
out_time_json = __server_path + 'out-time.json'
report_json = __server_path + 'report.json'
in_time_json = __server_path + 'in-time.json'

model_path = '../models/net_model.yml'

url = 'http://localhost'
