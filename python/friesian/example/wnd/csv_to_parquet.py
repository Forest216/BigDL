#
# Copyright 2016 The BigDL Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import os
from argparse import ArgumentParser
from pyspark.sql import SparkSession
from pyspark.sql.types import *


LABEL_COL = 0
INT_COLS = list(range(1, 14))
CAT_COLS = list(range(14, 40))


if __name__ == '__main__':
   parser = ArgumentParser()
   parser.add_argument('--input_files_path', type=str, required=True, help="Path to the txt file/files to be processed.")
   parser.add_argument('--output_folder_path', type=str, default=".", help="The path of the folder to save the parquet data.")
   args = parser.parse_args()
   spark = SparkSession.builder.getOrCreate()
   input_files_path = args.input_files_path.split(',')
   output_folder_path = args.output_folder_path

   label_fields = [StructField('_c%d' % LABEL_COL, IntegerType())]
   int_fields = [StructField('_c%d' % i, IntegerType()) for i in INT_COLS]
   str_fields = [StructField('_c%d' % i, StringType()) for i in CAT_COLS]
   schema = StructType(label_fields + int_fields + str_fields)

   # paths = [os.path.join(folder, 'day_%d' % i) for i in day_range]
   for file in input_files_path:
       df = spark.read.schema(schema).option('sep', '\t').csv(file)
       file_name = file.split('/')[-1].split('.')[0]
       output_file_path = os.path.join(output_folder_path, '{}.parquet'.format(file_name)).lstrip(".txt")
       df.write.parquet(output_file_path, mode="overwrite")