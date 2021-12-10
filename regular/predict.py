from rastervision.pipeline import rv_config
from rastervision.core.predictor import Predictor

# model_path = '/opt/data/raster-vision/0.12/model-zoo-0.12/isprs-potsdam-ss/model-bundle.zip'
model_path = 'D:/111/geojson/output/bundle/model-bundle.zip'

with rv_config.get_tmp_dir() as tmp_dir:
    model = Predictor(model_path, tmp_dir)
    print(model)