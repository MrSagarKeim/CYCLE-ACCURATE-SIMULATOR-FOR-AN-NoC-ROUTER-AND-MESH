import matplotlib.pyplot as plt

with open('logs.txt', 'r') as file:
    lines = file.read()

countfilt_pe0_and_d = 0;
countfilt_pe1_and_c = 0;
countfilt_pe2_and_a = 0;
countfilt_pe3_and_b = 0;

# considering (a to b) and (b to a) as same/single connection
countfilt_a_and_b = 0;
countfilt_b_and_c = 0;
countfilt_c_and_d = 0;
countfilt_d_and_a = 0;

line = lines.split("\n");
for current_line in line:
    if (current_line[1:7] == "ROUTER" and current_line[11] == 'G'):
        current_router = current_line[8];
        if (current_line[30:37] == "Pe Port"):
            if (current_router == '0'):
                countfilt_pe0_and_d += 1;
            elif (current_router == '1'):
                countfilt_pe1_and_c += 1;
            elif (current_router == '2'):
                countfilt_pe2_and_a += 1;
            else:
                countfilt_pe3_and_b += 1;
        else:
            if (current_router == '0'):
                if (current_line[30:34] == "East"):
                    countfilt_c_and_d += 1;
                else:
                    countfilt_d_and_a += 1;
            elif (current_router == '1'):
                if (current_line[30:34] == "West"):
                    countfilt_c_and_d += 1;
                else:
                    countfilt_b_and_c += 1;
            elif (current_router == '2'):
                if (current_line[30:34] == "East"):
                    countfilt_a_and_b += 1;
                else:
                    countfilt_d_and_a += 1;
            else:
                if (current_line[30:34] == "West"):
                    countfilt_a_and_b += 1;
                else:
                    countfilt_b_and_c += 1;
    elif (current_line[1:3] == "PE" and current_line[7:15] == "Received"):
        peno = current_line[4];
        if (peno == '0'):
            countfilt_pe0_and_d += 1;
        elif (peno == '1'):
            countfilt_pe1_and_c += 1;
        elif (peno == '2'):
            countfilt_pe2_and_a += 1;
        else:
            countfilt_pe3_and_b += 1;

connections = ["pe0 and D", "pe1 and C", "pe2 and A", "pe3 and B", "A and B", "B and C", "C and D", "D and A"]
filts_transferred = [countfilt_pe0_and_d, countfilt_pe1_and_c, countfilt_pe2_and_a, countfilt_pe3_and_b,
                     countfilt_a_and_b, countfilt_b_and_c, countfilt_c_and_d, countfilt_d_and_a]
plt.bar(connections, filts_transferred)
plt.xlabel("Connections -->")
plt.ylabel("Number of filts transferred -->")
plt.title("Graph showing No. of filts transferred as a function of connections")
plt.show()

