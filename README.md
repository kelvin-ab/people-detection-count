## Person detection retail 0013  

### Requirements
1. setup https://mosquitto.org/download/
2. setup https://docs.docker.com/docker-for-windows/install/

### How to guide
  unzip people_detction_count.zip  
1. setup socket server  

	    cd people_detction_count/socket
	    docker build -t socket .
	    docker run -it --net="host" socket
2. setup people detection and counter

	    cd people_detction_count/people_detection
	    docker build -t people_detction -f src/people_detction/Dockerfile .  
	    docker run -it --net="host" -v ~/<**PATH TO LOCAL VIDEO FILES**>/videos:/app/videos people_detction
	
If all go well, you will be able to access the result by listening to the socket end ***ws://0.0.0.0:4040/***
 
 #### Socket response format

1. event type -> **image**
   

	    {
	       "event": "image",
	       "data": "base64 image which contains the detection"
	    } 
2. event type -> **count**

	     {
		  "event": "count",
		  "data":  {"channel": "videos/sample_2.mp4", "up": 0, "down": 0}}
	    }

> Sample videos - to which the configuration is set - have been included
> in the zip


