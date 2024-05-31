def norm(angle):
  angle = angle % 360
  if angle > 180:
    angle = angle - 360
  return angle

for angle in range(-600,600,20):
  print(angle, norm(angle))


  