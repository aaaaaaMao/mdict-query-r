import os

temp_dir = os.path.join(os.getcwd(), 'tests/temp')
if not os.path.exists(temp_dir):
    os.mkdir(temp_dir)