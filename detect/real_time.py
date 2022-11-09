# http://192.168.1.4
#   /cam-lo.jpg
#   /cam-hi.jpg
#   /cam-mid.jpg


from ODT import ObjectDetection


url='http://192.168.31.106/cam-lo.jpg'
#   /cam-hi.jpg
#   /cam-mid.jpg



detector = ObjectDetection()
detector.run_detection()    

