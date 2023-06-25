# Plot part b
import matplotlib.pyplot as plt
with open('logs.txt', 'r') as file:
  # Read all the lines of the file into a list
  lines = file.readlines()

# Iterate over the lines and print them
clock = 0;
data_packet_info = [];
data_latency = [];
for line in lines:
  line_content = line.split(" ");
  if line_content[0] == "[CLOCK]":
    clock = int(line_content[3]);
    #print("clock=",clock);

  elif line_content[0][1:3] == "PE":
    pe = line_content[0][4];
    #print("pe",pe);
  else:
    router = line_content[0][8];
    if len(line_content) > 8:
      # Head Flit 
      source_head = line_content[9][3];
      dest_head = line_content[11][3];
      s = "Packet_from_"+source_head+"_to_"+dest_head;
      if source_head == router:
        data_packet_info.append(s); 
        data_latency.append(clock);
      elif dest_head == router:
        last_index = len(data_packet_info) - 1 - data_packet_info[::-1].index(s)
        data_latency[last_index] = clock - data_latency[last_index];
        data_latency[last_index] += 5; # For rest 5 pe after this
      #print("router ",router,"recived ",source_head,dest_head);
    #print("router",router);

#print("clock",clock,data_packet_info,data_latency);

# Create the plot
plt.bar(data_packet_info, data_latency)
plt.xlabel("Different packets along with source and destination.")
plt.ylabel("Latency (in clock cycles)")
plt.title("Graph showing Latency as function of packets sent")
# Show the plot
plt.show()