# Import PCL module
import pcl

# Load Point Cloud file

cloud = pcl.load_XYZRGB("tabletop.pcd")
print(f"Loaded cloud with {cloud.size} points")


# Voxel Grid filter
vox = cloud.make_voxel_grid_filter()

LEAF_SIZE = 0.01

vox.set_leaf_size(LEAF_SIZE,LEAF_SIZE,LEAF_SIZE)

cloud_filtered = vox.filter()
print(f"cloud filtered with {cloud_filtered.size} points")

pcl.save(cloud_filtered, "tabletop_voxel_filtered.pcd")



# PassThrough filter
passthrough = cloud_filtered.make_passthrough_filter()

filter_axis = 'z'
passthrough.set_filter_field_name(filter_axis)
axis_min = 0.6
axis_max = 1.1
passthrough.set_filter_limits(axis_min, axis_max)

cloud_filtered = passthrough.filter()
filename = 'pass_through_filtered.pcd'
pcl.save(cloud_filtered, filename)

# RANSAC plane segmentation
seg=cloud_filtered.make_segmenter()
seg.set_model_type(pcl.SACMODEL_PLANE)
seg.set_method_type(pcl.SAC_RANSAC)
max_distance = 0.01
seg.set_distance_threshold(max_distance)



# Extract inliers
inliers, coefficients = seg.segment()
extracted_inliers = cloud_filtered.extract(inliers, negative=False)
filename = 'extracted_inliers.pcd'
pcl.save(extracted_inliers, filename)

extracted_outlires = cloud_filtered.extract(inliers, negative=True)
filename_out = 'extracted_outLiers.pcd'
pcl.save(extracted_outlires, filename_out)
