import csv
import matplotlib.pyplot as plt

def get_coords(csv_file_obj, x_index , y1_index, y2_index,device_name_index,device_name):
	x_coords= list()
	y1_coords=list()
	y2_coords=list()

	reader= csv.reader(csv_file_obj)
	for row in reader:
			if (row[device_name_index]==device_name):
				x_coords.append(float(row[x_index]))
				y1_coords.append(float(row[y1_index]))
				y2_coords.append(float(row[y1_index]))


	return x_coords, y1_coords, y2_coords


def from_csv(csv_file_path, x_index, y1_index, y2_index,device_name_index,device_name):

	with open(csv_file_path, 'rb') as csv_file_obj:
		coords_tuple = get_coords(csv_file_obj,x_index,y1_index,y2_index,device_name_index,device_name)


	


	x_coords= coords_tuple[0]
	y1_coords=coords_tuple[1] 
	y2_coords=coords_tuple[2]

 	wiggle_room=3


	plt.figure(1)
	plt.title("Sensor Data")	

	
	plt.subplot(211)
	plt.xlabel('Time')
	plt.ylabel('Voltage')

	plt.axis([x_coords[0]-wiggle_room, x_coords[-1]+wiggle_room, y1_coords[0]-wiggle_room, y1_coords[-1]+wiggle_room])
	plt.plot(x_coords, y1_coords, 'bo')

	plt.subplot(212)
	plt.xlabel('Time')
	plt.ylabel('Current')


	plt.axis(  [  x_coords[0]-wiggle_room,  x_coords[-1]+wiggle_room,  y2_coords[0]-wiggle_room,  y2_coords[-1]+wiggle_room]  )
	plt.plot(x_coords, y1_coords, 'r^')
	plt.show()
