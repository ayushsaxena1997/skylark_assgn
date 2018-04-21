# Skylark Drones
# Technical Assignment
Search and identification of GCPs in images

The problem statement and dataset can be found in the following link:
https://drive.google.com/open?id=1BVI69XsNBp4ekbAuSlx5jdJTv6--29CE

The code was written and tested on Spyder (Python 3.6) running on Ubuntu 16.04 64 bit machine. No GPU was used.
Libraries used: OpenCV (cv2), Numpy and CSV

# Approach Undertaken:-
The problem can be broken down into two major sub-sections. 
1. Identification of GCP in an image.
2. Extracting the coordinates of inner corner of the GCPs.

The dataset provided for the dataset was small (10 images), which meant that learning was not at all an option. So, in this assignment, for identification of GCPs, Template Matching technique was used. In this technique, a 40x40 size template of GCP was cut out from one of the images. The template was used as a groundtruth for identification in all other images.

Template Matching technique is theoritically scale as well as rotation variant. Although the images in the dataset appeared to have been taken from same scale(height), the GDPs on the ground were positioned in any random orientation. To tackle this problem, the template extracted was rotated by fixed amount (30 degrees) and was saved everytime as a new image. This helped us create spatially varied versions of our template. An OpenCV function was used to facilitate this process.
Since every rotation of 40x40 sized image did not always produce a perfect square image, the OpenCV function inherently padded the blank spaces with black pixels. Now in order to make it look similar to original template, the black pixels were replaced by a colour resembling the surroundings (40 in grayscale) of the original GCP in the template. Finally, with these templates the data was tested using an OpenCV function 'cv2.matchTemplate'.


# Parameters:

delta: If the GCP identified is very close to the previously identifiedd GCP, it won't be considered valid. 'delta' denotes the minimum distance acceptable between two identified GCPs. This was done to make sure that no GCP is counted more than once.

threshold: The OpenCV function 'cv2.matchTemplate' when used with 'cv2.TM_CCOEFF_NORMED' returns a number between 0 and 1 indicating the confidence by which the two patches being compared matched successfully. A threshold is thus needed to prevent misidentification of other objects in the image as GCPs. (default :0.8, found experimentally; changing his parameter not recommended)

check: Used to count the number of GCPs found in an image.

angle: The difference (in degrees) between two subsequent rotated versions of the template.

# How to run the code?

Download the dataset and 'template.jpg' file available in the repository. This file contains our groundtruth, which is simply a 40x40 cutout from the 'DSC02209.JPG' image. 
Change all the paths to files according to your machine.
Update the list called 'names' with the filenames of the images under test.
For a finer identification, one can change the 'angle' parameter (default 30 deg).
Run.

# Expected output

The console will show the number of points identified and the co-ordinates of the inner corner of GCP for every rotation and every image.
In case of detection, the image will be saved with a red square box around the identified GCP and a green point inside it indicating the inner corner. 
A csv file called 'output.csv' will be created and saved specifying the image name and the co-ordinates identified inside it.
Before re-running the code, make sure that you delete 'output.csv' file.

# My results

My outputs can be found in the repository (outputs.csv). To summarize:
1. The GCP was detected successfully in all the positive images.
2. No GCP was detected in any negative image.
3. Along with the correct GCP, a couple of images were also marked with one location in image which resembles a GCP, but is actually not.

# Limitations of the model

1. The point being designated as the inner point of GCP is currently the centre of the identified area. Although it approximates the location well, it needs to be developed.
2. The model is scale variant, i.e. can fail if the images are taken from a drastically different height.

# Other possibilities

1. If the dataset is considerably large, then a Haar Cascade based model can work better. Haar Cascades need many variants of the positive and negative template versions to train on, but can produce fine results as Haar Cascades are scale and rotation invariant.
2. Corner matching techniques like SIFT and Harris corners might also be given a try.

