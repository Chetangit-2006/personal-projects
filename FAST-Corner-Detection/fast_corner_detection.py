import cv2
import numpy as np
import time

THRESHOLD = 20
N = 12

CIRCLE = [
    (-3, 0), (-3, 1), (-2, 2), (-1, 3),
    (0, 3), (1, 3), (2, 2), (3, 1),
    (3, 0), (3, -1), (2, -2), (1, -3),
    (0, -3), (-1, -3), (-2, -2), (-3, -1)
]

print("FAST Corner Detection Project")
print("Code started successfully!")

def fast_corner_test(gray, x, y, threshold=20):

    h, w = gray.shape

    # Ignore image boundary
    if x < 3 or x >= w - 3 or y < 3 or y >= h - 3:
        return False

    center = int(gray[y, x])

    brighter = center + threshold
    darker = center - threshold

    # Check 4 pixels first
    test_pixels = [0, 4, 8, 12]

    bright = 0
    dark = 0

    for i in test_pixels:

        dx, dy = CIRCLE[i]
        value = int(gray[y + dy, x + dx])

        if value >= brighter:
            bright += 1

        if value <= darker:
            dark += 1

    # Reject if it is clearly not a corner
    if bright < 3 and dark < 3:
        return False

    # Check all 16 pixels
    states = []

    for dx, dy in CIRCLE:

        value = int(gray[y + dy, x + dx])

        if value >= brighter:
            states.append(1)

        elif value <= darker:
            states.append(-1)

        else:
            states.append(0)

    # Check continuous pixels
    states = states + states

    max_bright = 0
    max_dark = 0

    current_bright = 0
    current_dark = 0

    for state in states:

        if state == 1:
            current_bright += 1
            current_dark = 0

        elif state == -1:
            current_dark += 1
            current_bright = 0

        else:
            current_bright = 0
            current_dark = 0

        max_bright = max(max_bright, current_bright)
        max_dark = max(max_dark, current_dark)

    return max_bright >= N or max_dark >= N

def detect_fast(gray, threshold=20):

    h, w = gray.shape

    corners = []

    for y in range(3, h - 3):

        for x in range(3, w - 3):

            if fast_corner_test(gray, x, y, threshold):
                corners.append((x, y))

    return corners
img = cv2.imread("test_image.jpg")

if img is None:
    print("Image not found!")
    exit()

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

corners = detect_fast(gray, THRESHOLD)

print("Number of corners:", len(corners))

def fast_corner_test(gray, x, y, threshold=20):

    h, w = gray.shape

    if x < 3 or x >= w - 3 or y < 3 or y >= h - 3:
        return False

    center = int(gray[y, x])

    brighter = center + threshold
    darker = center - threshold

    test_pixels = [0, 4, 8, 12]

    bright = 0
    dark = 0

    for i in test_pixels:

        dx, dy = CIRCLE[i]
        value = int(gray[y + dy, x + dx])

        if value >= brighter:
            bright += 1

        if value <= darker:
            dark += 1

    if bright < 3 and dark < 3:
        return False

    states = []

    for dx, dy in CIRCLE:

        value = int(gray[y + dy, x + dx])

        if value >= brighter:
            states.append(1)

        elif value <= darker:
            states.append(-1)

        else:
            states.append(0)

    states = states + states

    max_bright = 0
    max_dark = 0

    current_bright = 0
    current_dark = 0

    for state in states:

        if state == 1:
            current_bright += 1
            current_dark = 0

        elif state == -1:
            current_dark += 1
            current_bright = 0

        else:
            current_bright = 0
            current_dark = 0

        max_bright = max(max_bright, current_bright)
        max_dark = max(max_dark, current_dark)

    return max_bright >= N or max_dark >= N

def detect_fast(gray, threshold=20):

    h, w = gray.shape

    corners = []

    for y in range(3, h - 3):

        for x in range(3, w - 3):

            if fast_corner_test(gray, x, y, threshold):
                corners.append((x, y))

    return corners

def non_maximum_suppression(gray, corners):

    if len(corners) == 0:
        return []

    scores = []

    # Calculate strength of every detected corner
    for x, y in corners:

        center = int(gray[y, x])
        score = 0

        for dx, dy in CIRCLE:
            value = int(gray[y + dy, x + dx])
            score += abs(value - center)

        scores.append((score, x, y))

    # Strongest corners first
    scores.sort(reverse=True)

    selected = []

    # Minimum distance between corners
    min_distance = 5

    for score, x, y in scores:

        keep = True

        for sx, sy in selected:

            distance = (x - sx) ** 2 + (y - sy) ** 2

            if distance < min_distance ** 2:
                keep = False
                break

        if keep:
            selected.append((x, y))

    return selected
# Read image
img = cv2.imread("test_image.jpg")

# Check if image was found
if img is None:
    print("ERROR: test_image.jpg not found!")
    exit()

# Convert image to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Detect FAST corners
corners = detect_fast(gray, THRESHOLD)
corners = non_maximum_suppression(gray, corners)

# Print number of corners
print("Number of corners detected:", len(corners))

# Draw detected corners
for x, y in corners:

    cv2.circle(
        img,
        (x, y),
        3,
        (0, 0, 255),
        1
    )

cv2.imwrite("FAST_output.jpg", img)
# Show the result
cv2.imshow("FAST Corner Detection", img)

# Wait until a key is pressed
cv2.waitKey(0)

# Close the window
cv2.destroyAllWindows()

