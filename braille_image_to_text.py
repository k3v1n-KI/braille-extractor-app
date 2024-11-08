from collections import Counter
from skimage import io
import numpy as np
import imutils
import cv2
import re

import warnings
warnings.filterwarnings("ignore")


IMAGE_SCALE = 1500
ITERATIONS = 0


def process_image(path):
   # Fetching & scaling image
   image = imutils.resize(io.imread(path), IMAGE_SCALE)

   # Converting to black and white and extracting significant features
   bw = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
   original = image.copy()

   # Binarizing image
   kernel = np.ones((5, 5), np.uint8)
   threshold = cv2.threshold(bw, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
   
   # Eroding and dialating to remove irrelevent information
   for op in [cv2.erode, cv2.dilate]:
     threshold = op(threshold, kernel, iterations=ITERATIONS)
    
   contours = imutils.grab_contours(
     cv2.findContours(
       threshold.copy(),
       cv2.RETR_EXTERNAL,
       cv2.CHAIN_APPROX_SIMPLE
     )
   )
   
   contours = cv2.findContours(threshold.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
   contours = imutils.grab_contours(contours)
   
   return original, contours


def rearrange_contours(contours, original, diameter):
    bounding_boxes = [list(cv2.boundingRect(c)) for c in contours]
    tol = 0.7 * diameter

    # Function to bin coordinates
    def bin_coordinates(index):
        sorted_boxes = sorted(bounding_boxes, key=lambda b: b[index])
        coordinates = [b[index] for b in sorted_boxes]
        min_coord = coordinates[0]

        for b in sorted_boxes:
            if abs(b[index] - min_coord) <= tol:
                b[index] = min_coord
            elif b[index] > min_coord + diameter:
                min_coord = next(e for e in coordinates if e > min_coord + diameter)
        
        return sorted(set(coordinates))

    xs = [bin_coordinates(i) for i in [0, 1]][0]

    contours, bounding_boxes = zip(*sorted(zip(contours, bounding_boxes), key=lambda b: b[1][1] * len(original) + b[1][0]))

    return contours, bounding_boxes, xs


def fetch_dots(contours, diameter):
  questioncontours = []
  for c in contours:
    (_, __, w, h) = cv2.boundingRect(c)
    ar = w / float(h)

    # in order to label the contour as a question, region
    # should be sufficiently wide, sufficiently tall, and
    # have an aspect ratio approximately equal to 1
    if diameter * 0.8 <= w <= diameter * 1.2 and 0.8 <= ar <= 1.2:
      questioncontours.append(c)    
  return questioncontours


def calculate_dot_size(contours):
  boundingBoxes = [list(cv2.boundingRect(c)) for c in contours]
  c = Counter([i[2] for i in boundingBoxes])
  mode = c.most_common(1)[0][0]
  if mode > 1:
    diameter = mode
  else:
    diameter = c.most_common(2)[1][0]
  return diameter


def project_contours(questioncontours, original, boundingBoxes):
  color = (0, 255, 0)
  i = 0
  for q in range(len(questioncontours)):
    cv2.drawContours(original, questioncontours[q], -1, color, 3)
    cv2.putText(original, str(i), (boundingBoxes[q][0] + boundingBoxes[q][2]//2, boundingBoxes[q][1] + boundingBoxes[q][3]//2), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
    i += 1


def spacing(boundingBoxes, diameter):
    space_x = []
    space_y = []
    
    coordinates = [[box[0], box[1]] for box in boundingBoxes]
    
    for i in range(len(coordinates) - 1):
      c_x = coordinates[i + 1][0] - coordinates[i][0]
      c_y = coordinates[i + 1][1] - coordinates[i][1]
      if c_x > (diameter // 2): space_x.append(c_x)
      if c_y > (diameter // 2): space_y.append(c_y)
    return sorted(list(set(space_x))), sorted(list(set(space_y)))


def calculate_spacing(boundingBoxes, diameter, xs):
  horizontal_space, vertical_space = spacing(boundingBoxes, diameter)

  # smallest x-serapation (between two adjacent dots in a letter)

  dist_1 = horizontal_space[0]
  dist_2 = 0
  dist_3 = 0

  for x in horizontal_space:
    if dist_2 > 0 and x > dist_2 * 1.3:
      dist_3 = x
      break
    if dist_2 == 0 and x > dist_1 * 1.3:
      dist_2 = x
      
  linesV = []
  prev = 0 # outside

  linesV.append(min(xs) - (dist_2 - diameter)/2)

  for i in range(1, len(xs)):
    diff = xs[i] - xs[i-1]
    
    if i == 1 and dist_2 * 0.9 < diff:
        linesV.append(min(xs) - dist_2 - diameter / 2)
        prev = 1

    elif dist_1 * 0.8 < diff < dist_1 * 1.2:
        linesV.append(xs[i-1] + (dist_1 + diameter) / 2)
        prev = 1

    elif dist_2 * 0.8 < diff < dist_2 * 1.1:
        linesV.append(xs[i-1] + (dist_2 + diameter) / 2)
        prev = 0

    elif dist_3 * 0.9 < diff < dist_3 * 1.1:
        linesV.extend([
            xs[i-1] + (dist_2 + diameter) / 2 if prev == 1 else xs[i-1] + (dist_1 + diameter) / 2,
            xs[i-1] + (dist_2 + dist_1 + diameter) / 2 if prev == 1 else xs[i-1] + (dist_1 + dist_2 + diameter) / 2
        ])

    elif dist_3 * 1.1 < diff:
        linesV.extend([
            xs[i-1] + (dist_2 + diameter) / 2 if prev == 1 else xs[i-1] + (dist_1 + diameter) / 2,
            xs[i-1] + (dist_2 + dist_1 + diameter) / 2 if prev == 1 else xs[i-1] + (dist_1 + dist_2 + diameter) / 2,
            xs[i-1] + (dist_3 + diameter) / 2 if prev == 1 else xs[i-1] + (dist_1 + dist_3 + diameter) / 2
        ])
        prev = 1 - prev

  linesV.append(max(xs) + diameter * 1.5)
  if len(linesV) % 2 == 0:
    linesV.append(max(xs) + dist_2 + diameter)
    
  return linesV, vertical_space


def map_letters(boundingBoxes, diameter, vertical_space, linesV):
  boxes = list(boundingBoxes)
  boxes.append((100000, 0))

  dots = [[]]
  for y in sorted(list(set(vertical_space))):
    if y > 1.3 * diameter:
      min_y_diameter = y*1.5
      break

  # Fetching dots line by line
  for b in range(len(boxes) - 1):
    if boxes[b][0] < boxes[b+1][0]:
        dots[-1].append(boxes[b][0])
    else:
      if abs(boxes[b+1][1] - boxes[b][1]) < min_y_diameter:
        dots[-1].append(boxes[b][0])
        dots.append([])
      else:
        dots[-1].append(boxes[b][0])
        dots.append([])
        if len(dots)%3 == 0 and not dots[-1]:
          dots.append([])

    
  letters = []
  
  for row in dots:
    letter_row = []
    c = 0
    for i in range(len(linesV) - 1):
        letter_row.append(1 if c < len(row) and linesV[i] < row[c] < linesV[i + 1] else 0)
        c += letter_row[-1]  # Only increment `c` if a dot was matched
    letters.append(letter_row if row else [0] * (len(linesV) - 1))
    
  return letters

def translate(letters):
  # Aplhabets represented by a matrix of darkened dots
  alphabets = {'⠁': '1', '⠃': '13', '⠉': '12', '⠙': '124', '⠑': '14', '⠋': '123',
             '⠛': '1234', '⠓': '134', '⠊': '23', '⠚': '234', '⠅': '15',
             '⠇': '135', '⠍': '125', '⠝': '1245', '⠕': '145', '⠏': '1235',
             '⠟': '12345', '⠗': '1345', '⠎': '235', '⠞': '2345', '⠥': '156',
             '⠧': '1356', '⠺': '2346', '⠭': '1256', '⠽': '12456', '⠵': '1456',
             '⠼': '2456', '`': '6', '⠂': '3', '⠲': '346', '⠶': '356', '`': '26',
             '⠒': '34', '⠄': '5'}

  # Inversing keys and values in alphanets to get a braille dictionary
  braille = {v: k for k, v in alphabets.items()}
  braille_keys = braille.keys()

  letters = np.array([np.array(l) for l in letters])

  ans  = ''

  for r in range(0, len(letters), 3):
    for c in range(0, len(letters[0]), 2):
      f = letters[r:r+3,c:c+2].flatten()
      f = ''.join([str(i + 1) for i,d in enumerate(f) if d == 1])
      if not f:
        if ans[-1] != ' ': ans += ' '
      elif f in braille_keys:
        if f == '6' or f == '26':
          continue
        ans += braille[f]
      else:
        ans += '?'
    if ans[-1] != ' ': ans += ' '
  
  return ans


def driver(path):
    original, contours = process_image(path)

    diameter = calculate_dot_size(contours)
    dotcontours = fetch_dots(contours, diameter)

    questioncontours, boundingBoxes, xs = rearrange_contours(dotcontours, original, diameter)
    project_contours(questioncontours, original, boundingBoxes)

    linesV, vertical_space = calculate_spacing(boundingBoxes, diameter, xs)

    letters = map_letters(boundingBoxes, diameter, vertical_space, linesV)
    return translate(letters)
