python producer.py track.avi&
python show.py&
spark-submit --master local[4] pyStream.py file:///home/VideoStream/Txts file:///home/VideoStream/rects

