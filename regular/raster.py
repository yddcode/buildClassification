from rastervision.core.rv_pipeline import *
from rastervision.core.backend import *
from rastervision.core.data import *
from rastervision.pytorch_backend import *
from rastervision.pytorch_learner import *

from torchvision.models.segmentation.segmentation import fcn_resnet50, FCN, fcn_resnet101, deeplabv3_resnet50,deeplabv3_resnet101
from torchvision.models.segmentation.fcn import FCN, FCNHead
from torchvision.models.segmentation.deeplabv3 import DeepLabHead, DeepLabV3
from torchvision.models import resnet, mobilenet_v2
from torchvision.models._utils import IntermediateLayerGetter
from torchvision.models.utils import load_state_dict_from_url
# python -m rastervision.pipeline.cli predict code/model-bundle.zip code/sample-img-spacenet-r
# io-cc.tif predict.tif
def get_config(runner) -> SemanticSegmentationConfig:
    root_uri = '/opt/data/output/'
    # base_uri = ("https://s3.amazonaws.com/azavea-research-public-data/raster-vision/examples/spacenet")
    base_uri = '/opt/src/code/'

    # train_image_uri = f'{base_uri}/RGB-PanSharpen_AOI_2_Vegas_img205.tif'
    # train_label_uri = f'{base_uri}/buildings_AOI_2_Vegas_img205.geojson'
    train_image_uri1 = f'{base_uri}/Rectangle_taishun_train_Level_18.tif'#, f'{base_uri}/Rectangle_ceshi_Level_18.tif' # Rectangle_c3_Level_18.tif cuiyuan_Level_18 Rectangle_ceshi_Level_18
    train_label_uri1 = f'{base_uri}/taishun_train.geojson'#, f'{base_uri}/ceshi.geojson' # bxy_afterc3t.geojson
    # val_image_uri = f'{base_uri}/RGB-PanSharpen_AOI_2_Vegas_img25.tif'
    # val_label_uri = f'{base_uri}/buildings_AOI_2_Vegas_img25.geojson'
    val_image_uri1 = f'{base_uri}/Rectangle_taishun_train_Level_18flip.tif'#, f'{base_uri}/Rectangle_ceshi_Level_18.tif'
    val_label_uri1 = f'{base_uri}/taishun_train.geojson'#, f'{base_uri}/ceshi.geojson'

    train_image_uri2 = f'{base_uri}/Rectangle_ceshi_Level_18.tif'
    train_label_uri2 = f'{base_uri}/ceshi.geojson'

    train_image_uri3 = f'{base_uri}/Rectangle_train3_Level_18.tif'
    train_label_uri3 = f'{base_uri}/0trainjwzb3.geojson'

    train_image_uri4 = f'{base_uri}/Rectangle_train4_Level_18.tif'
    train_label_uri4 = f'{base_uri}/0trainjwzb4.geojson'

    val_image_uri2 = f'{base_uri}/Rectangle_ceshi_Level_18.tif'
    val_label_uri2 = f'{base_uri}/ceshi.geojson'

    val_image_uri3 = f'{base_uri}/Rectangle_vaild_Level_18.tif'
    val_label_uri3 = f'{base_uri}/0vaildjwzb.geojson'

    channel_order = [0, 1, 2]
    class_config = ClassConfig(
        names=['building', 'background'], colors=['red', 'black'])

    def make_scene(scene_id: str, image_uri: str,
                   label_uri: str) -> SceneConfig:
        """
        - The GeoJSON does not have a class_id property for each geom,
          so it is inferred as 0 (ie. building) because the default_class_id
          is set to 0.
        - The labels are in the form of GeoJSON which needs to be rasterized
          to use as label for semantic segmentation, so we use a RasterizedSource.
        - The rasterizer set the background (as opposed to foreground) pixels
          to 1 because background_class_id is set to 1.
        """
        raster_source = RasterioSourceConfig(
            uris=[image_uri], channel_order=channel_order)
        vector_source = GeoJSONVectorSourceConfig(
            uri=label_uri, default_class_id=0, ignore_crs_field=True)
        label_source = SemanticSegmentationLabelSourceConfig(
            raster_source=RasterizedSourceConfig(
                vector_source=vector_source,
                rasterizer_config=RasterizerConfig(background_class_id=1)))
        return SceneConfig(
            id=scene_id,
            raster_source=raster_source,
            label_source=label_source)

    scene_dataset = DatasetConfig(
        class_config=class_config,
        train_scenes=[
            # make_scene('scene_205', train_image_uri, train_label_uri)
            make_scene('scene_1', train_image_uri1, train_label_uri1),
            make_scene('scene_2', train_image_uri2, train_label_uri2),
            make_scene('scene_3', train_image_uri3, train_label_uri3),
            make_scene('scene_4', train_image_uri4, train_label_uri4),
        ],
        validation_scenes=[
            # make_scene('scene_25', val_image_uri, val_label_uri)
            make_scene('scene_1', val_image_uri1, val_label_uri1),
            make_scene('scene_2', val_image_uri2, val_label_uri2),
            make_scene('scene_3', val_image_uri3, val_label_uri3),
        ])

    # Use the PyTorch backend for the SemanticSegmentation pipeline.
    chip_sz = 256
    img_sz = chip_sz

    backend = PyTorchSemanticSegmentationConfig(
        data=SemanticSegmentationGeoDataConfig(
            scene_dataset=scene_dataset,
            window_opts=GeoDataWindowConfig(
                method=GeoDataWindowMethod.random,
                size=chip_sz,
                size_lims=(chip_sz, chip_sz + 1),
                max_windows=300)),
        # model=SemanticSegmentationModelConfig(backbone=Backbone.resnet50),
        model = SemanticSegmentationModelConfig(
            external_def=ExternalModuleConfig(
                uri = '/opt/src/code/pytorch-fpn-master.zip', 
                # github_repo='AdeelH/pytorch-fpn:0.2',
                name='fpn',
                entrypoint='make_fpn_resnet',
                entrypoint_kwargs={
                    'name': 'resnet50',
                    'fpn_type': 'panoptic',
                    'num_classes': 3, #len(class_config.names),
                    'fpn_channels': 256,
                    'in_channels': len(channel_order),
                    'out_size': (img_sz, img_sz)
                })),
        solver=SolverConfig(lr=1e-4, num_epochs=80, batch_sz=2, one_cycle=True))
    print(chip_sz, '\n', backend, '\n', scene_dataset)
    return SemanticSegmentationConfig(
        root_uri=root_uri,
        dataset=scene_dataset,
        backend=backend,
        train_chip_sz=chip_sz,
        predict_chip_sz=chip_sz)