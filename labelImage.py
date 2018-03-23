import sys, json, numpy as np, tensorflow as tf, os


#Read data from stdin
#def read_in():
    #lines = sys.stdin.readlines()
    #Since our input would only be having one line, parse our JSON data from that
    #return json.loads(lines[0])

#os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

def main():
    #get our data as an array from read_in()
    #lines = read_in()

    #create a numpy array

	# change this as you see fit
	image_path = sys.argv[1]
	# Read in the image_data
	image_data = tf.gfile.FastGFile(image_path, 'rb').read()

	# Loads label file, strips off carriage return
	label_lines = [line.rstrip() for line 
	                   in tf.gfile.GFile("retrained_labels.txt")]

	# Unpersists graph from file
	with tf.gfile.FastGFile("retrained_graph.pb", 'rb') as f:
	    graph_def = tf.GraphDef()
	    graph_def.ParseFromString(f.read())
	    tf.import_graph_def(graph_def, name='')

	with tf.Session() as sess:
	    # Feed the image_data as input to the graph and get first prediction
	    softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
	    
	    predictions = sess.run(softmax_tensor, \
	             {'DecodeJpeg/contents:0': image_data})
	    
	    # Sort to show labels of first prediction in order of confidence
	    top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]
	    counter = 0
	    print('{')
	    for node_id in top_k:
	    	counter += 1
	        human_string = label_lines[node_id]
	        score = predictions[0][node_id]
	        if counter < len(top_k):
	        	print('"%s" : %.5f,' % (human_string, score))
	        else:
	        	print('"%s" : %.5f' % (human_string, score))
	    print('}')
#start process
if __name__ == '__main__':
    main()