# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name" : "CamTrax",
    "author" : "CamTrax", 
    "description" : "",
    "blender" : (3, 0, 0),
    "version" : (1, 0, 0),
    "location" : "",
    "warning" : "",
    "doc_url": "camtrax.io", 
    "tracker_url": "camtrax.io", 
    "category" : "Import-Export" 
}


import bpy
import bpy.utils.previews
import os
from bpy_extras.io_utils import ImportHelper, ExportHelper
import json


addon_keymaps = {}
_icons = None


def load_preview_icon(path):
    global _icons
    if not path in _icons:
        if os.path.exists(path):
            _icons.load(path, path, "IMAGE")
        else:
            return 0
    return _icons[path].icon_id


class SNA_PT_CAMTRAX_PANEL_4FD3F(bpy.types.Panel):
    bl_label = 'CamTrax Panel'
    bl_idname = 'SNA_PT_CAMTRAX_PANEL_4FD3F'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_context = ''
    bl_category = 'CamTrax'
    bl_order = 0
    bl_ui_units_x=0

    @classmethod
    def poll(cls, context):
        return not (False)

    def draw_header(self, context):
        layout = self.layout

    def draw(self, context):
        layout = self.layout
        layout.template_icon(icon_value=load_preview_icon(bpy.path.abspath(os.path.join(os.path.dirname(__file__), 'assets', 'logo2.png'))), scale=5.0)
        row_20D1F = layout.row(heading='', align=False)
        row_20D1F.alert = False
        row_20D1F.enabled = True
        row_20D1F.active = True
        row_20D1F.use_property_split = False
        row_20D1F.use_property_decorate = False
        row_20D1F.scale_x = 1.0
        row_20D1F.scale_y = 1.0
        row_20D1F.alignment = 'Center'.upper()
        row_20D1F.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        row_20D1F.label(text='', icon_value=0)
        row_20D1F.label(text='CamTrax v1.0.0', icon_value=0)
        row_20D1F.label(text='', icon_value=0)
        op = layout.operator('sna.import_48be2', text='Import .Trx File', icon_value=706, emboss=True, depress=False)
        op.sna_path = os.path.basename(r'')
        op = layout.operator('sna.shadow_992d5', text='Enable Shadow Catcher', icon_value=627, emboss=True, depress=False)


class SNA_OT_Import_48Be2(bpy.types.Operator, ImportHelper):
    bl_idname = "sna.import_48be2"
    bl_label = "Import"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}
    filter_glob: bpy.props.StringProperty( default='*.Trx', options={'HIDDEN'} )
    bl_property = 'sna_path'
    sna_path: bpy.props.StringProperty(name='Path', description='Path', default='', subtype='FILE_PATH', maxlen=0)

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        print(self.sna_path)
        filepath = self.filepath
        import math
        import mathutils
        # Define axis conversions and constants
        UNITY2BLENDER = mathutils.Matrix((
            (-1, 0, 0, 0),
            (0, 0, -1, 0),
            (0, 1, 0, 0),
            (0, 0, 0, 1)
        ))
        IDENTITY_MATRIX = mathutils.Matrix.Identity(4)
        ORIENTATION_PORTRAIT = 1
        ORIENTATION_UPSIDE_DOWN = 2
        ORIENTATION_LANDSCAPE_LEFT = 3
        ORIENTATION_LANDSCAPE_RIGHT = 4
        RAD_PORTRAIT = math.radians(0)
        RAD_LANDSCAPE_LEFT = math.radians(0)
        RAD_LANDSCAPE_RIGHT = math.radians(180)
        ROTATE_PORTRAIT = mathutils.Matrix.Rotation(RAD_PORTRAIT, 4, 'Z')
        ROTATE_LANDSCAPE_LEFT = mathutils.Matrix.Rotation(RAD_LANDSCAPE_LEFT, 4, 'Z')
        ROTATE_LANDSCAPE_RIGHT = mathutils.Matrix.Rotation(RAD_LANDSCAPE_RIGHT, 4, 'Z')
        # Create the node graph function before calling it in import_Trxfile

        def create_node_graph(context, filepath, orientation):
            scene = context.scene
            scene.use_nodes = True
            node_tree = scene.node_tree
            nodes = node_tree.nodes
            # Remove existing nodes
            for node in list(nodes):
                nodes.remove(node)
            for obj in bpy.data.objects:
                obj.select_set(False)
            # Create video node and load its movie clip
            video_filepath = filepath.replace('-camera.Trx', '-video.mp4')
            video_node = nodes.new('CompositorNodeMovieClip')
            video_node.clip = bpy.data.movieclips.load(filepath=video_filepath)
            video_node.location.x = -1209.803955078125
            video_node.location.y = 692.0598754882812
            # Create rotate node
            rotate_node = nodes.new('CompositorNodeRotate')
            rotate_node.filter_type = 'BILINEAR'
            if orientation == ORIENTATION_PORTRAIT:
                rotate_node.inputs['Degr'].default_value = math.radians(-90)
            elif orientation == ORIENTATION_LANDSCAPE_RIGHT:
                rotate_node.inputs['Degr'].default_value = math.radians(180)
            rotate_node.location.x = -967.3910522460938
            rotate_node.location.y = 680.869384765625
            # Connect the output of the video clip into the rotate node
            node_tree.links.new(
                video_node.outputs['Image'],
                rotate_node.inputs['Image']
            )
            # Create first scale node
            scale_node_1 = nodes.new('CompositorNodeScale')
            scale_node_1.space = 'SCENE_SIZE'
            scale_node_1.location.x = -773.644287109375
            scale_node_1.location.y = 665.2340698242188
            # Connect the output of the rotate node into the scale node
            node_tree.links.new(
                rotate_node.outputs['Image'],
                scale_node_1.inputs['Image']
            )
            # Create a composite node
            composite_node = nodes.new('CompositorNodeComposite')
            composite_node.use_alpha = False
            composite_node.location.x = 1379.92529296875
            composite_node.location.y = 493.9861145019531
            # Connect the output of the first scale node to the composite node
            node_tree.links.new(
                scale_node_1.outputs['Image'],
                composite_node.inputs['Image']
            )
            # Create a viewer node and set it to use alpha
            viewer_node = nodes.new('CompositorNodeViewer')
            viewer_node.use_alpha = True
            viewer_node.location.x = 1384.837890625
            viewer_node.location.y = 309.9682922363281
            # Connect the output of the scale node to the viewer node
            node_tree.links.new(
                scale_node_1.outputs['Image'],
                viewer_node.inputs['Image']
            )

        def import_Trxfile(filepath, create_nodes=True, switch_to_cam=False):
            context = bpy.context
            scene = context.scene
            # Parse json data
            with open(filepath, 'r') as f:
                data = json.load(f)
            # Pull out relevant properties
            render_data = data.get('render_data') or {}
            camera_frames = data.get('camera_frames') or []
            camera_timestamps = camera_frames.get('timestamps') or []
            camera_transforms = camera_frames.get('transforms') or []
            camera_datas = camera_frames.get('datas') or []
            planes = data.get('planes') or []
            tracked_transforms = data.get('tracked_transforms') or []
            resolution_x = render_data['video_resolution_x']
            resolution_y = render_data['video_resolution_y']
            camera_rotation = IDENTITY_MATRIX
            video_orientation = render_data['orientation']
            if video_orientation == ORIENTATION_PORTRAIT:
                camera_rotation = ROTATE_PORTRAIT
            elif video_orientation == ORIENTATION_LANDSCAPE_LEFT:
                camera_rotation = ROTATE_LANDSCAPE_LEFT
            elif video_orientation == ROTATE_LANDSCAPE_RIGHT:
                camera_rotation = ROTATE_LANDSCAPE_RIGHT
            # Render settings that we want to switch all the time
            scene.render.film_transparent = True
            scene.render.ffmpeg.audio_codec = 'AAC'
            if create_nodes:
                create_node_graph(context, filepath, video_orientation)
                # Disable any filmic or custom color management and switch to standard
                scene.view_settings.view_transform = 'Standard'
                # Set defaults for the video encoding outputs
                scene.render.filepath = filepath.replace('-camera.Trx', '-blender-render.mp4')
                scene.render.image_settings.file_format = 'FFMPEG'
                scene.render.ffmpeg.constant_rate_factor = 'HIGH'
                scene.render.ffmpeg.format = 'MPEG4'
            # Setup render settings
            fps = render_data.get('fps', 60)
            scene.render.fps = fps
            scene.render.resolution_x = resolution_x
            scene.render.resolution_y = resolution_y
            # Setup scene settings
            if len(camera_timestamps) > 0:
                scene.frame_end = max(int(math.ceil(camera_timestamps[-1] * fps)), 1)
            bpy.ops.object.add()
            Trx_root = context.object
            Trx_root.name = 'Imported Tracking Data'
            # Create camera
            bpy.ops.object.camera_add(enter_editmode=False)
            cam = context.active_object
            cam.data.sensor_fit = 'VERTICAL'
            cam.data.lens_unit = 'MILLIMETERS'
            cam.name = 'ARCamera'
            cam.parent = Trx_root
            # Setup video background
            video_filepath = filepath.replace('-camera.Trx', '-video.mp4')
            background = cam.data.background_images.new()
            background.source = 'MOVIE_CLIP'
            background.alpha = 1
            background.clip = bpy.data.movieclips.load(filepath=video_filepath)
            background.frame_method = 'STRETCH'
            background.show_background_image = True
            if video_orientation == ORIENTATION_PORTRAIT:
                background.frame_method = 'CROP'
                background.rotation = math.radians(90)
                background.scale = resolution_x / resolution_y
            elif video_orientation == ORIENTATION_LANDSCAPE_RIGHT:
                background.rotation = RAD_LANDSCAPE_RIGHT
            cam.data.show_background_images = True
            # Ensure that there's a sequencer
            if not scene.sequence_editor:
                scene.sequence_editor_create()
            # Add the video background audio clip to the sequencer
            scene.sequence_editor.sequences.new_sound('background_audio', video_filepath, 1, 1)
            # Switch the 3D windows to view through the new camera with the background
            for screen in context.workspace.screens:
                for area in screen.areas:
                    for space in area.spaces:
                        if space.type == 'VIEW_3D':
                            space.camera = cam
                            if switch_to_cam:
                                space.region_3d.view_perspective = 'CAMERA'
            # Create camera animation
            for idx, timestamp in enumerate(camera_timestamps):
                try:
                    mat = mathutils.Matrix(camera_transforms[idx])
                    data = camera_datas[idx]
                except IndexError:
                    continue
                focal_length, sensor_height = data[0], data[1]
                frameidx = max(int(math.ceil(timestamp * fps)), 1)
                scene.frame_set(frameidx)
                cam.data.lens = focal_length
                cam.data.sensor_height = sensor_height
                cam.data.keyframe_insert('lens', frame=frameidx)
                cam.matrix_world = UNITY2BLENDER @ (mat @ camera_rotation)
                # Insert loc and rot keyframes
                bpy.ops.anim.keyframe_insert_menu(type='BUILTIN_KSI_LocRot')
            # Rewind back to the first frame
            scene.frame_set(1)
            # Add planes
            for plane_index, plane in enumerate(planes):
                bpy.ops.mesh.primitive_plane_add(size=1.0, calc_uvs=True, enter_editmode=False, align='WORLD')
                plane_obj = context.object
                plane_obj.parent = Trx_root
                plane_obj.name = '%s Plane [%d]' % (plane['alignment'].capitalize(), plane_index + 1)
                plane_obj.display_type = 'WIRE'
                plane_obj.hide_render = True
                plane_obj.matrix_world = (UNITY2BLENDER @ mathutils.Matrix(plane['transform']))
                visibility = getattr(plane_obj, 'cycles_visibility', None)
                if visibility is not None:
                    visibility.camera = False
                    visibility.diffuse = False
                    visibility.glossy = False
                    visibility.transmission = False
                    visibility.scatter = False
                plane_obj.visible_camera = False
                plane_obj.visible_diffuse = False
                plane_obj.visible_glossy = False
                plane_obj.visible_shadow = False
                plane_obj.visible_transmission = False
                plane_obj.visible_volume_scatter = False
            # Add tracked empty transforms
            for track_index, tfm in enumerate(tracked_transforms):
                bpy.ops.object.add()
                tracked_obj = context.object
                tracked_obj.parent = Trx_root
                tracked_obj.name = 'Empty [%d]' % (track_index + 1,)
                tracked_obj.empty_display_size = 0.2
                tracked_obj.matrix_world = UNITY2BLENDER @ mathutils.Matrix(tfm)
            # Select the camera object again so that the user can adjust any keyframes as needed
            for obj in bpy.data.objects:
                obj.select_set(False)
            cam.select_set(True)
            return {'FINISHED'}

        def create_node_graph(context, filepath, orientation):
            scene = context.scene
            scene.use_nodes = True
            node_tree = scene.node_tree
            nodes = node_tree.nodes
            # Remove existing nodes, we'll be recreating everything we need
            for node in list(nodes):
                nodes.remove(node)
            for obj in bpy.data.objects:
                obj.select_set(False)
            # Create video node and load its movie clip
            video_filepath = filepath.replace('-camera.Trx', '-video.mp4')
            video_node = nodes.new('CompositorNodeMovieClip')
            video_node.clip = bpy.data.movieclips.load(filepath=video_filepath)
            video_node.location.x = -1209.803955078125
            video_node.location.y = 692.0598754882812
            # Create rotate node
            rotate_node = nodes.new('CompositorNodeRotate')
            rotate_node.filter_type = 'BILINEAR'
            if orientation == ORIENTATION_PORTRAIT:
                rotate_node.inputs['Degr'].default_value = math.radians(-90)
            elif orientation == ORIENTATION_LANDSCAPE_RIGHT:
                rotate_node.inputs['Degr'].default_value = math.radians(180)
            rotate_node.location.x = -967.3910522460938
            rotate_node.location.y = 680.869384765625
            # Connect the output of the video clip into the rotate node
            node_tree.links.new(
                video_node.outputs['Image'],
                rotate_node.inputs['Image']
            )
            # Create first scale node
            scale_node_1 = nodes.new('CompositorNodeScale')
            scale_node_1.space = 'SCENE_SIZE'
            scale_node_1.location.x = -773.644287109375
            scale_node_1.location.y = 665.2340698242188
            # Connect the output of the rotate node into the scale node
            node_tree.links.new(
                rotate_node.outputs['Image'],
                scale_node_1.inputs['Image']
            )
            # Create a mix node
            mix_node_1 = nodes.new('CompositorNodeMixRGB')
            mix_node_1.location.x = 1133.854736328125
            mix_node_1.location.y = 392.45819091796875
            # Connect the output of the first scale node into the first image input of
            # the mix node
            node_tree.links.new(
                scale_node_1.outputs['Image'],
                mix_node_1.inputs[1]
            )
            # Create a composite node
            composite_node = nodes.new('CompositorNodeComposite')
            composite_node.use_alpha = False
            composite_node.location.x = 1379.92529296875
            composite_node.location.y = 493.9861145019531
            # Connect the output of the mix node to the composite node
            node_tree.links.new(
                mix_node_1.outputs['Image'],
                composite_node.inputs['Image']
            )
            # Create a viewer node and set it to use alpha
            viewer_node = nodes.new('CompositorNodeViewer')
            viewer_node.use_alpha = True
            viewer_node.location.x = 1384.837890625
            viewer_node.location.y = 309.9682922363281
            # Connect the output of the mix node to the viewer node
            node_tree.links.new(
                mix_node_1.outputs['Image'],
                viewer_node.inputs['Image']
            )
            # Create an RLayers node
            rlayers_node = nodes.new('CompositorNodeRLayers')
            rlayers_node.location.x = -1213.6219482421875
            rlayers_node.location.y = 271.8380432128906
            # Create a multiply node
            multiply_node = nodes.new('CompositorNodeMixRGB')
            multiply_node.blend_type = 'MULTIPLY'
            multiply_node.inputs['Fac'].default_value = 1
            multiply_node.location.x = 435.77789306640625
            multiply_node.location.y = -66.51539611816406
            # Create a small frame node
            small_frame_node = nodes.new('NodeFrame')
            small_frame_node.label = 'TURN SEGMENTATION ON AND OFF'
            small_frame_node.location.x = 778.8148193359375
            small_frame_node.location.y = 149.1981964111328
            # Create segmentation mix node
            segmentation_mix_node = nodes.new('CompositorNodeMixRGB')
            segmentation_mix_node.parent = small_frame_node
            segmentation_mix_node.blend_type = 'MIX'
            segmentation_mix_node.inputs['Fac'].default_value = 0
            segmentation_mix_node.location.x = -30.51397705078125
            segmentation_mix_node.location.y = -17.452789306640625
            # Connect the output of the multiply node to the mix node
            node_tree.links.new(
                multiply_node.outputs['Image'],
                segmentation_mix_node.inputs[2]
            )
            # Connect the image output of the RLayers node to the mix node
            node_tree.links.new(
                rlayers_node.outputs['Image'],
                mix_node_1.inputs[2]
            )
            # Connect the alpha output of the RLayers node to the multiply node
            node_tree.links.new(
                rlayers_node.outputs['Alpha'],
                multiply_node.inputs[2]
            )
            # Connect the alpha output of the RLayers node to the segmentation mix node
            node_tree.links.new(
                rlayers_node.outputs['Alpha'],
                segmentation_mix_node.inputs[1]
            )
            # Connect the image output of the segmentation mix node to the final mix node
            node_tree.links.new(
                segmentation_mix_node.outputs['Image'],
                mix_node_1.inputs['Fac']
            )
            # Create segmentation node and load its movie clip
            segmentation_filepath = filepath.replace('-camera.Trx', '-segmentation.mp4')
            segmentation_node = nodes.new('CompositorNodeMovieClip')
            segmentation_node.clip = bpy.data.movieclips.load(filepath=segmentation_filepath)
            segmentation_node.location.x = -1218.925537109375
            segmentation_node.location.y = -288.89691162109375
            # Create a frame node
            frame_node = nodes.new('NodeFrame')
            frame_node.label = 'ADJUST THESE FOR THE SEGMENTATION MASK SIZE AND FEATHER'
            frame_node.location.x = -352.728515625
            frame_node.location.y = -243.61328125
            # SECOND FRAME NODE (778.8148193359375, 149.1981964111328)
            # Create second scale node
            scale_node_2 = nodes.new('CompositorNodeScale')
            scale_node_2.space = 'RENDER_SIZE'
            scale_node_2.frame_method = 'STRETCH'
            scale_node_2.location.x = -999.0
            scale_node_2.location.y = -310.29962158203125
            # Connect the output of the segmentation clip into the scale node
            node_tree.links.new(
                segmentation_node.outputs['Image'],
                scale_node_2.inputs['Image']
            )
            # Create third scale node
            scale_node_3 = nodes.new('CompositorNodeScale')
            scale_node_3.parent = frame_node
            scale_node_3.space = 'RELATIVE'
            scale_node_3.location.x = -426.41912841796875
            scale_node_3.location.y = -62.532958984375
            # Connect the output of the second scale node into the third scale node
            node_tree.links.new(
                scale_node_2.outputs['Image'],
                scale_node_3.inputs['Image']
            )
            # Create an exposure node
            exposure_node = nodes.new('CompositorNodeExposure')
            exposure_node.parent = frame_node
            exposure_node.inputs['Exposure'].default_value = 3
            exposure_node.location.x = -233.28424072265625
            exposure_node.location.y = -102.9228515625
            # Connect the output of the scale node into the exposure node
            node_tree.links.new(
                scale_node_3.outputs['Image'],
                exposure_node.inputs['Image']
            )
            # Create an invert node
            invert_node = nodes.new('CompositorNodeInvert')
            invert_node.parent = frame_node
            invert_node.invert_rgb = True
            invert_node.invert_alpha = False
            invert_node.inputs['Fac'].default_value = 1
            invert_node.hide = True
            invert_node.location.x = -48.83795166015625
            invert_node.location.y = -120.58245849609375
            # Connect the output of the exposure node into the invert node
            node_tree.links.new(
                exposure_node.outputs['Image'],
                invert_node.inputs['Color']
            )
            # Create the first blur node
            blur_node_1 = nodes.new('CompositorNodeBlur')
            blur_node_1.parent = frame_node
            blur_node_1.filter_type = 'MITCH'
            blur_node_1.size_x = 20
            blur_node_1.size_y = 20
            blur_node_1.inputs['Size'].default_value = 1
            blur_node_1.location.x = 178.44140625
            blur_node_1.location.y = -45.1683349609375
            # Connect the output of the invert node into the blur node
            node_tree.links.new(
                invert_node.outputs['Color'],
                blur_node_1.inputs['Image']
            )
            # Create the dialate/erode filter node
            de_node = nodes.new('CompositorNodeDilateErode')
            de_node.parent = frame_node
            de_node.mode = 'THRESHOLD'
            de_node.distance = 3
            de_node.edge = 3
            de_node.location.x = 377.0482177734375
            de_node.location.y = -50.9749755859375
            # Connect the output of the first blur node into the dilate/erode node
            node_tree.links.new(
                blur_node_1.outputs['Image'],
                de_node.inputs['Mask']
            )
            # Create the second blur node
            blur_node_2 = nodes.new('CompositorNodeBlur')
            blur_node_2.parent = frame_node
            blur_node_2.filter_type = 'MITCH'
            blur_node_2.size_x = 10
            blur_node_2.size_y = 10
            blur_node_2.inputs['Size'].default_value = 1
            blur_node_2.location.x = 555.4044189453125
            blur_node_2.location.y = -27.837646484375
            # Connect the output of the dilate/erode filter node into the second blur node
            node_tree.links.new(
                de_node.outputs['Mask'],
                blur_node_2.inputs['Image']
            )
            # Connect the output of the second blur node into the multiply node
            node_tree.links.new(
                blur_node_2.outputs['Image'],
                multiply_node.inputs[1]
            )
            for obj in bpy.data.objects:
                obj.select_set(False)
        # Set the file path for your specific Trx file
        import_Trxfile(filepath, create_nodes=True, switch_to_cam=True)
        return {"FINISHED"}


class SNA_OT_Shadow_992D5(bpy.types.Operator):
    bl_idname = "sna.shadow_992d5"
    bl_label = "Shadow"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not bpy.data.objects['Horizontal Plane [1]'].is_shadow_catcher

    def execute(self, context):
        bpy.data.objects['Horizontal Plane [1]'].is_shadow_catcher = True
        bpy.data.scenes['Scene'].render.engine = 'CYCLES'
        bpy.data.objects['Horizontal Plane [1]'].hide_render = False
        bpy.data.objects['Horizontal Plane [1]'].visible_camera = True
        bpy.data.objects['Horizontal Plane [1]'].visible_diffuse = True
        bpy.data.objects['Horizontal Plane [1]'].visible_glossy = True
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


def register():
    global _icons
    _icons = bpy.utils.previews.new()
    bpy.utils.register_class(SNA_PT_CAMTRAX_PANEL_4FD3F)
    bpy.utils.register_class(SNA_OT_Import_48Be2)
    bpy.utils.register_class(SNA_OT_Shadow_992D5)


def unregister():
    global _icons
    bpy.utils.previews.remove(_icons)
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    for km, kmi in addon_keymaps.values():
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()
    bpy.utils.unregister_class(SNA_PT_CAMTRAX_PANEL_4FD3F)
    bpy.utils.unregister_class(SNA_OT_Import_48Be2)
    bpy.utils.unregister_class(SNA_OT_Shadow_992D5)
