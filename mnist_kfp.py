import kfp
import os
from kubernetes import client, config
import calendar
import time
from datetime import datetime

class Pipeline:
	'''
	A class object to hold the pipeline and it's components.
	'''
	
	pipeline_components_path = ""
	train_op = ""
	serve_model_op = ""
	inference_app_op = ""
	tensorboard_op = ""

	def mnist_pipeline():

		# Creating timestamp
		timestamp = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')

		#Defining Task for Model training
		train_model_task = self.train_op
		train_model_task.add_volume_mount(self.nfs_volume_mount)

		#Defining Task for model serving    
		serve_model_task = self.serve_model_op(timestamp=timestamp)
		serve_model_task.add_volume_mount(self.nfs_volume_mount)
		serve_model_task.after(train_model_task)

		#Defining task for creating a tensorboard    
		tensorboard_task = self.tensorboard_op(timestamp=timestamp)
		tensorboard_task.add_volume_mount(self.nfs_volume_mount)
		tensorboard_task.after(train_model_task)


		#Defining task for inference app deployment
		webui_task = self.inference_app_op(image_path="docker.io/premkarthi/blerssi-webui:v4",
									timestamp=timestamp)
		webui_task.add_volume_mount(self.nfs_volume_mount)
		webui_task.after(serve_model_task)

	def __init__(self, execution_environment, volume_claim_name='nfs-wf-volume', version='v1'):
		self.execution_environment = execution_environment
		
		if self.execution_environment == "in-cluster":
			self.pipeline_components_path = "apps/networking/ble-localization/onprem/pipelines/"
		else:
			self.pipeline_components_path = ""

		component_root_train= self.pipeline_components_path+'components/'+version+'/train/'
		component_root_serve = self.pipeline_components_path+'components/'+version+'/serve/'
		component_root_inference_app = self.pipeline_components_path+'components/'+version+'/inference-app/'
		component_root_tensorboard= self.pipeline_components_path+'components/'+version+'/tensorboard/'

		self.train_op = kfp.components.load_component_from_file(os.path.join(component_root_train, 'component.yaml')) 
		self.serve_model_op = kfp.components.load_component_from_file(os.path.join(component_root_serve, 'component.yaml'))
		self.inference_app_op = kfp.components.load_component_from_file(os.path.join(component_root_inference_app, 'component.yaml'))
		self.tensorboard_op = kfp.components.load_component_from_file(os.path.join(component_root_tensorboard, 'component.yaml'))

		nfs_pvc = client.V1PersistentVolumeClaimVolumeSource(claim_name=volume_claim_name)
		nfs_volume = client.V1Volume(name=volume_claim_name, persistent_volume_claim=nfs_pvc)
		self.nfs_volume_mount = client.V1VolumeMount(mount_path='/mnt/', name='nfs')
