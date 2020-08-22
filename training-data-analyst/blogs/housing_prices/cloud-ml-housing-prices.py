#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import tensorflow as tf


# In[ ]:


print(tf.__version__)


# In[ ]:


#downlad data from GCS and store as pandas dataframe 
data_train = pd.read_csv(
  filepath_or_buffer='https://storage.googleapis.com/vijay-public/boston_housing/housing_train.csv',
  names=["CRIM","ZN","INDUS","CHAS","NOX","RM","AGE","DIS","RAD","TAX","PTRATIO","MEDV"])

data_test = pd.read_csv(
  filepath_or_buffer='https://storage.googleapis.com/vijay-public/boston_housing/housing_test.csv',
  names=["CRIM","ZN","INDUS","CHAS","NOX","RM","AGE","DIS","RAD","TAX","PTRATIO","MEDV"])


# In[ ]:


data_train.head()


# In[ ]:


FEATURES = ["CRIM", "ZN", "INDUS", "NOX", "RM",
            "AGE", "DIS", "TAX", "PTRATIO"]
LABEL = "MEDV"

feature_cols = [tf.feature_column.numeric_column(k)
                  for k in FEATURES] #list of Feature Columns


# In[ ]:


def generate_estimator(output_dir):
  return tf.estimator.DNNRegressor(feature_columns=feature_cols,
                                            hidden_units=[10, 10],
                                            model_dir=output_dir)


# In[ ]:


def generate_input_fn(data_set):
    def input_fn():
      features = {k: tf.constant(data_set[k].values) for k in FEATURES}
      labels = tf.constant(data_set[LABEL].values)
      return features, labels
    return input_fn


# In[ ]:


def serving_input_fn():
  #feature_placeholders are what the caller of the predict() method will have to provide
  feature_placeholders = {
      column.name: tf.placeholder(column.dtype, [None])
      for column in feature_cols
  }
  
  #features are what we actually pass to the estimator
  features = {
    # Inputs are rank 1 so that we can provide scalars to the server
    # but Estimator expects rank 2, so we expand dimension
    key: tf.expand_dims(tensor, -1)
    for key, tensor in feature_placeholders.items()
  }
  return tf.estimator.export.ServingInputReceiver(
    features, feature_placeholders
  )


# In[ ]:


get_ipython().run_cell_magic('bash', '', 'cd /home/jupyter/training-data-analyst/blogs/housing_prices\nmkdir trainer\ntouch trainer/__init__.py')


# In[ ]:


get_ipython().run_cell_magic('writefile', 'trainer/task.py', '\nimport argparse\nimport pandas as pd\nimport tensorflow as tf\nfrom tensorflow.contrib.learn.python.learn import learn_runner\nfrom tensorflow.contrib.learn.python.learn.utils import saved_model_export_utils\n\nprint(tf.__version__)\ntf.logging.set_verbosity(tf.logging.ERROR)\n\ndata_train = pd.read_csv(\n  filepath_or_buffer=\'https://storage.googleapis.com/vijay-public/boston_housing/housing_train.csv\',\n  names=["CRIM","ZN","INDUS","CHAS","NOX","RM","AGE","DIS","RAD","TAX","PTRATIO","MEDV"])\n\ndata_test = pd.read_csv(\n  filepath_or_buffer=\'https://storage.googleapis.com/vijay-public/boston_housing/housing_test.csv\',\n  names=["CRIM","ZN","INDUS","CHAS","NOX","RM","AGE","DIS","RAD","TAX","PTRATIO","MEDV"])\n\nFEATURES = ["CRIM", "ZN", "INDUS", "NOX", "RM",\n            "AGE", "DIS", "TAX", "PTRATIO"]\nLABEL = "MEDV"\n\nfeature_cols = [tf.feature_column.numeric_column(k)\n                  for k in FEATURES] #list of Feature Columns\n\ndef generate_estimator(output_dir):\n  return tf.estimator.DNNRegressor(feature_columns=feature_cols,\n                                            hidden_units=[10, 10],\n                                            model_dir=output_dir)\n\ndef generate_input_fn(data_set):\n    def input_fn():\n      features = {k: tf.constant(data_set[k].values) for k in FEATURES}\n      labels = tf.constant(data_set[LABEL].values)\n      return features, labels\n    return input_fn\n\ndef serving_input_fn():\n  #feature_placeholders are what the caller of the predict() method will have to provide\n  feature_placeholders = {\n      column.name: tf.placeholder(column.dtype, [None])\n      for column in feature_cols\n  }\n  \n  #features are what we actually pass to the estimator\n  features = {\n    # Inputs are rank 1 so that we can provide scalars to the server\n    # but Estimator expects rank 2, so we expand dimension\n    key: tf.expand_dims(tensor, -1)\n    for key, tensor in feature_placeholders.items()\n  }\n  return tf.estimator.export.ServingInputReceiver(\n    features, feature_placeholders\n  )\n\ntrain_spec = tf.estimator.TrainSpec(\n                input_fn=generate_input_fn(data_train),\n                max_steps=3000)\n\nexporter = tf.estimator.LatestExporter(\'Servo\', serving_input_fn)\n\neval_spec=tf.estimator.EvalSpec(\n            input_fn=generate_input_fn(data_test),\n            steps=1,\n            exporters=exporter)\n\n######START CLOUD ML ENGINE BOILERPLATE######\nif __name__ == \'__main__\':\n  parser = argparse.ArgumentParser()\n  # Input Arguments\n  parser.add_argument(\n      \'--output_dir\',\n      help=\'GCS location to write checkpoints and export models\',\n      required=True\n  )\n  parser.add_argument(\n        \'--job-dir\',\n        help=\'this model ignores this field, but it is required by gcloud\',\n        default=\'junk\'\n    )\n  args = parser.parse_args()\n  arguments = args.__dict__\n  output_dir = arguments.pop(\'output_dir\')\n######END CLOUD ML ENGINE BOILERPLATE######\n\n  #initiate training job\n  tf.estimator.train_and_evaluate(generate_estimator(output_dir), train_spec, eval_spec)')


# In[ ]:


GCS_BUCKET = 'gs://BUCKET_NAME' #CHANGE THIS TO YOUR BUCKET
PROJECT = 'PROJECT_ID' #CHANGE THIS TO YOUR PROJECT ID
REGION = 'us-central1' #OPTIONALLY CHANGE THIS


# In[ ]:


import os
os.environ['GCS_BUCKET'] = GCS_BUCKET
os.environ['PROJECT'] = PROJECT
os.environ['REGION'] = REGION


# In[ ]:


get_ipython().run_cell_magic('bash', '', "gcloud ai-platform local train \\\n   --module-name=trainer.task \\\n   --package-path=trainer \\\n   -- \\\n   --output_dir='./output'")


# In[ ]:


get_ipython().run_cell_magic('bash', '', 'JOBNAME=housing_$(date -u +%y%m%d_%H%M%S)\n\ngcloud ai-platform jobs submit training $JOBNAME \\\n   --region=$REGION \\\n   --module-name=trainer.task \\\n   --package-path=./trainer \\\n   --job-dir=$GCS_BUCKET/$JOBNAME/ \\\n   --runtime-version 1.15 \\\n   -- \\\n   --output_dir=$GCS_BUCKET/$JOBNAME/output')


# In[ ]:


get_ipython().run_cell_magic('bash', '', 'JOBNAME=housing_$(date -u +%y%m%d_%H%M%S)\n\ngcloud ai-platform jobs submit training $JOBNAME \\\n   --region=$REGION \\\n   --module-name=trainer.task \\\n   --package-path=./trainer \\\n   --job-dir=$GCS_BUCKET/$JOBNAME \\\n   --runtime-version 1.15 \\\n   --scale-tier=STANDARD_1 \\\n   -- \\\n   --output_dir=$GCS_BUCKET/$JOBNAME/output')


# In[ ]:


get_ipython().run_cell_magic('bash', '', 'JOBNAME=housing_$(date -u +%y%m%d_%H%M%S)\n\ngcloud ai-platform jobs submit training $JOBNAME \\\n   --region=$REGION \\\n   --module-name=trainer.task \\\n   --package-path=./trainer \\\n   --job-dir=$GCS_BUCKET/$JOBNAME \\\n   --runtime-version 1.15 \\\n   --scale-tier=BASIC_GPU \\\n   -- \\\n   --output_dir=$GCS_BUCKET/$JOBNAME/output')


# In[ ]:


get_ipython().run_cell_magic('writefile', 'config.yaml', 'trainingInput:\n  scaleTier: CUSTOM\n  masterType: complex_model_m_gpu\n  workerType: complex_model_m_gpu\n  workerCount: 1')


# In[ ]:


get_ipython().run_cell_magic('bash', '', 'JOBNAME=housing_$(date -u +%y%m%d_%H%M%S)\n\ngcloud ai-platform jobs submit training $JOBNAME \\\n   --region=$REGION \\\n   --module-name=trainer.task \\\n   --package-path=./trainer \\\n   --job-dir=$GCS_BUCKET/$JOBNAME \\\n   --runtime-version 1.15 \\\n   --config config.yaml \\\n   -- \\\n   --output_dir=$GCS_BUCKET/$JOBNAME/output')


# In[ ]:


get_ipython().run_cell_magic('bash', '', 'MODEL_NAME="housing_prices"\nMODEL_VERSION="v1"\nMODEL_LOCATION=output/export/Servo/$(ls output/export/Servo | tail -1) \n\n#gcloud ai-platform versions delete ${MODEL_VERSION} --model ${MODEL_NAME} #Uncomment to overwrite existing version\n#gcloud ai-platform models delete ${MODEL_NAME} #Uncomment to overwrite existing model\ngcloud ai-platform models create ${MODEL_NAME} --regions $REGION\ngcloud ai-platform versions create ${MODEL_VERSION} --model ${MODEL_NAME} --origin ${MODEL_LOCATION} --staging-bucket=$GCS_BUCKET --runtime-version=1.15')


# In[ ]:


get_ipython().run_cell_magic('writefile', 'records.json', '{"CRIM": 0.00632,"ZN": 18.0,"INDUS": 2.31,"NOX": 0.538, "RM": 6.575, "AGE": 65.2, "DIS": 4.0900, "TAX": 296.0, "PTRATIO": 15.3}\n{"CRIM": 0.00332,"ZN": 0.0,"INDUS": 2.31,"NOX": 0.437, "RM": 7.7, "AGE": 40.0, "DIS": 5.0900, "TAX": 250.0, "PTRATIO": 17.3}')


# In[ ]:


get_ipython().system('gcloud ai-platform predict --model housing_prices --json-instances records.json')

