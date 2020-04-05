# -*- coding: utf-8 -*-
"""
Created on Sun Nov 17 23:21:05 2019

@author: mit
"""

import json
import numpy as np
import pandas as pd
import os
import pickle
import sys

if __name__ == "__main__":

	try:

		path_to_videos = "key_points.json"

		

		columns = ['score_overall', 'nose_score', 'nose_x', 'nose_y', 'leftEye_score', 'leftEye_x', 'leftEye_y',
		               'rightEye_score', 'rightEye_x', 'rightEye_y', 'leftEar_score', 'leftEar_x', 'leftEar_y',
		               'rightEar_score', 'rightEar_x', 'rightEar_y', 'leftShoulder_score', 'leftShoulder_x', 'leftShoulder_y',
		               'rightShoulder_score', 'rightShoulder_x', 'rightShoulder_y', 'leftElbow_score', 'leftElbow_x',
		               'leftElbow_y', 'rightElbow_score', 'rightElbow_x', 'rightElbow_y', 'leftWrist_score', 'leftWrist_x',
		               'leftWrist_y', 'rightWrist_score', 'rightWrist_x', 'rightWrist_y', 'leftHip_score', 'leftHip_x',
		               'leftHip_y', 'rightHip_score', 'rightHip_x', 'rightHip_y', 'leftKnee_score', 'leftKnee_x', 'leftKnee_y',
		               'rightKnee_score', 'rightKnee_x', 'rightKnee_y', 'leftAnkle_score', 'leftAnkle_x', 'leftAnkle_y',
		               'rightAnkle_score', 'rightAnkle_x', 'rightAnkle_y']
		data = json.loads(open(path_to_videos , 'r').read())
		csv_data = np.zeros((len(data), len(columns)))
		for i in range(csv_data.shape[0]):
			one = []
			one.append(data[i]['score'])
			for obj in data[i]['keypoints']:
				one.append(obj['score'])
				one.append(obj['position']['x'])
				one.append(obj['position']['y'])
			csv_data[i] = np.array(one)
		df=pd.DataFrame(csv_data, columns=columns)

		length=len(df)
		if length>150:
			x=df.iloc[0:150,:].values
		elif length<150:
			x=df.iloc[:,:].values
			y=df.iloc[-1:,:].values
			rp=150-length
			y=np.tile(y,(rp,1))
			x=np.concatenate((x, y), axis=0)
		else:
			x=df.iloc[:,:].values

		data=np.mean(x,axis=0)
		data= np.reshape(data, (1, 52))

		label=['book','car','gift','movie','sell','total']

		#Prediction1----------------------------------------------------------------------------

		filename='random_forest.sav'
		classifier = pickle.load(open(filename, 'rb'))
		y_pred1 = classifier.predict(data)
		pred_label1=label[int(y_pred1[0])]
		#Prediction1----------------------------------------------------------------------------

		filename='MLP_model.sav'
		classifier = pickle.load(open(filename, 'rb'))
		y_pred2 = classifier.predict(data)
		pred_label2=label[int(y_pred2[0])]
		#Prediction1----------------------------------------------------------------------------

		filename='logistic_regression.sav'
		classifier = pickle.load(open(filename, 'rb'))
		y_pred3 = classifier.predict(data)
		pred_label3=label[int(y_pred3[0])]
		#Prediction1----------------------------------------------------------------------------

		filename='support_vector.sav'
		classifier = pickle.load(open(filename, 'rb'))
		y_pred4 = classifier.predict(data)
		pred_label4=label[int(y_pred4[0])]



		data = {
			
			"1": pred_label1,
			"2": pred_label2,
			"3": pred_label3,
			"4": pred_label4

		}

		jsondata = json.dumps(data)
		print(jsondata)
		sys.stdout.flush()

	except:

		print("Error Occured")



