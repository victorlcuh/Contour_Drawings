import os
import numpy as np

from keras.preprocessing import image
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Conv2D
from keras.layers import MaxPooling2D
from keras.layers import Flatten
from keras.layers import Dense
from keras.callbacks import EarlyStopping

import matplotlib.pyplot as plt
EPOCH_STEP = 200
EPOCH = 20

def eval_metric(model, history, metric_name):
    '''
    Function to evaluate a trained model on a chosen metric. 
    Training and validation metric are plotted in a
    line chart for each epoch.
    
    Parameters:
        history : model training history
        metric_name : loss or accuracy
    Output:
        line chart with epochs of x-axis and metric on
        y-axis
    '''
    metric = history.history[metric_name]
    val_metric = history.history['val_' + metric_name]
    e = range(1, EPOCH + 1)
    plt.plot(e, metric, 'bo', label='Train ' + metric_name)
    plt.plot(e, val_metric, 'b', label='Validation ' + metric_name)
    plt.xlabel('Epoch number')
    plt.ylabel(metric_name)
    plt.title('Comparing training and validation ' + metric_name + ' for ' + model.name)
    plt.legend()
    plt.show()

## Part 1 - CNN Setup

# Initialize the CNN
classifier = Sequential()

# Step 1 - Convolution
# Step 2 - Pooling
classifier.add(Conv2D(32, (3, 3), input_shape=(64, 64, 1), activation='relu'))
classifier.add(MaxPooling2D(pool_size=(2, 2)))

classifier.add(Conv2D(64, (3, 3), activation='relu'))
classifier.add(MaxPooling2D(pool_size=(2, 2)))

classifier.add(Conv2D(128, (3, 3), activation='relu'))
classifier.add(MaxPooling2D(pool_size=(2, 2)))

classifier.add(Conv2D(256, (3, 3), activation='relu'))
classifier.add(MaxPooling2D(pool_size=(2, 2)))

# Step 3 - Flattening
classifier.add(Flatten())

# Step 4 - Full Connection
classifier.add(Dense(units=128, activation='relu'))
classifier.add(Dense(units=2, activation='softmax'))

# Compiling the CNN
classifier.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

## Part 2 - Fitting the CNN to the images

train_datagen = ImageDataGenerator(
    rescale=1./255,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True)

test_datagen = ImageDataGenerator(
    rescale=1./255)

training_set = train_datagen.flow_from_directory(
    'data/train',
    target_size=(64, 64),
    batch_size=32,
    class_mode='categorical',
    color_mode='grayscale')

test_set = train_datagen.flow_from_directory(
    'data/test',
    target_size=(64, 64),
    batch_size=32,
    class_mode='categorical',
    color_mode='grayscale')

print('Training Neural Network')

#es = EarlyStopping(monitor='val_acc', mode='auto', verbose=1, restore_best_weights=True, patience=10)

base_history = classifier.fit_generator(
    training_set,
    steps_per_epoch=EPOCH_STEP,
    epochs=EPOCH,
    validation_data=test_set,
    validation_steps=800,
    workers=7,
    max_queue_size=100,
    )

eval_metric(classifier, base_history, 'loss')

print('Done Training Neural Network')

#from keras.models import model_from_json
## load json and create model
#json_file = open('model/model.json', 'r')
#loaded_model_json = json_file.read()
#json_file.close()
#classifier = model_from_json(loaded_model_json)
## load weights into new model
#classifier.load_weights("model/model.h5")
#print("Loaded model from disk")

print(training_set.class_indices)
print('')

correct_classifications = 0
incorrect_classifications = 0

print('Expecting: female')
for file_name in os.listdir('data/validation/female'):
    test_image = image.load_img('data/validation/female/' + file_name, color_mode='grayscale', target_size=(64,64))
    test_image = image.img_to_array(test_image)
    test_image = np.expand_dims(test_image, axis=0)
    result = classifier.predict(test_image)
    print(file_name)
    print(result)
    best_result = np.argmax(result)
    for class_name in training_set.class_indices:
        if best_result == training_set.class_indices[class_name]:
            prediction = class_name
    if prediction == 'female':
        correct_classifications += 1
    else:
        incorrect_classifications += 1
    print('Prediction: ' + str(best_result) + ' - ' + prediction)
    print('')

print('')
print('')

print('Expecting: male')
for file_name in os.listdir('data/validation/male'):
    test_image = image.load_img('data/validation/male/' + file_name, color_mode='grayscale', target_size=(64,64))
    test_image = image.img_to_array(test_image)
    test_image = np.expand_dims(test_image, axis=0)
    result = classifier.predict(test_image)
    print(file_name)
    print(result)
    best_result = np.argmax(result)
    for class_name in training_set.class_indices:
        if best_result == training_set.class_indices[class_name]:
            prediction = class_name
    if prediction == 'male':
        correct_classifications += 1
    else:
        incorrect_classifications += 1
    print('Prediction: ' + str(best_result) + ' - ' + prediction)
    print('')

print("Accuracy: %0.2f" % (correct_classifications / (correct_classifications + incorrect_classifications)))

# Serialize model to JSON
if not os.path.exists('model'):
    os.makedirs('model')
model_json = classifier.to_json()
with open("model/model.json", "w") as json_file:
    json_file.write(model_json)
# Serialize weights to HDF5
classifier.save_weights("model/model.h5")
print("Saved model to disk")