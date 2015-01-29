producer.py track.py
spark-submit --master local[4] pyStream.py Txts rects
python show.py
