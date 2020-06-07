
# this is where the data will go
data_dir="./vs"
# include timestamp in image
include_timestamp=True

image_width=1280
image_height=720

# 0 to 100 jpeg compression quality
image_quality=30

# maximum number of frames per second to capture
max_fps=5.0

# rotate images 90 degrees before image feature detection
rotate_on_detection=True

# show labels on the videos (you must run object detection for this to work)
show_labels=True

# send alerts when person detected during a certain time of day
send_alerts=True
# if a person is detected between 22 and 6 UTC, send a phone alert.
alert_armed_h0 = 22.0 # alarm on
alert_armed_h1 = 6.0  # alarm off
minimum_spacing_between_calls=1.0  # wait at least one hour until we make another call

