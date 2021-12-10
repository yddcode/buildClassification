import re, os

label_fn_prefix = 'Rectangle_Level_'
# label_paths = list_paths(label_dir, ext='.geojson')
# name = os.path.splitext(name)[0]
label_paths = []
for filename in os.listdir('D:/111/geojson/'):
    if filename.endswith('tif'):
        # filename = os.path.splitext(filename)[0]
        label_paths.append(filename)

label_re = re.compile(r'.*{}(\d+).tif'.format(
     label_fn_prefix))
print(label_re, label_paths)     
scene_ids = [
      label_re.match(label_path).group(1) for label_path in label_paths]

print(scene_ids)