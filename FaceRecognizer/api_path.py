image_path = '../data/'  # Set where you want to store Scanned Images
__config_path = '../config/'  # Set where  data files to be stored
__server_path = '../serve/'   # Set to Webserver Location

classifiers = {'face': "face.xml"}  # Add Classifiers
classifier_path = '../classifiers/'  # Set Directory to Classifiers

total_bin = __config_path + 'total.bin'
names_bin = __config_path + 'names.bin'
data_bin = __config_path + 'data.bin'

names_json = __server_path + 'names.json'
out_time_json = __server_path + 'out-time.json'
report_json = __server_path + 'report.json'
in_time_json = __server_path + 'in-time.json'

model_path = '../models/net_model.yml'

url = 'http://localhost'
