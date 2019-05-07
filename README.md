https://github.com/michaeltran/CV-Contour-Drawings

Altered some files to use different datasets.

"python TrainNeuralNetworkSplit.py" - to split data into train/test/validation

"python TrainNeuralNetwork.py" to train the data and then test it and output accuracy.

Labeled images to be placed in the data/presplit/__label__ folders ie data/presplit/male and data/presplit/female

Dataset for faces can be acquired here: http://mmlab.ie.cuhk.edu.hk/projects/CelebA.html
Relevant paper: @inproceedings{liu2015faceattributes,
 	author = {Ziwei Liu, Ping Luo, Xiaogang Wang, and Xiaoou Tang},
 	title = {Deep Learning Face Attributes in the Wild},
 	booktitle = {Proceedings of International Conference on Computer Vision (ICCV)},
 	month = December,
 	year = {2015} 
  }

PhotoSketch (see michael's repo) used to generate contour images of the face dataset. 