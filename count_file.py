import os

def count_number(input_images):
  img_list = os.listdir(input_images)
  number = len(img_list)
  return number
