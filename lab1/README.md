# 460-Lab1

Lab: Network Simulation

In this lab, you will learn about network simulation using a packet-level, event-driven simulator. You will use the simulator to setup some basic networks and verify its accuracy with respect to delay and loss. You will also examine the basic queueing theory result that delay grows exponentially as utilization approaches 100%.
Simulator

I have written a simple network simulator called Bene. This simulator includes a basic event scheduler, plus objects for nodes, links, and packets. The simulator allows you to setup basic networks with static routes and send packets between any pair of connected nodes.

Please see the Bene Wiki for documentation.
Two Nodes

Use the simulator to setup a simple network consisting of two nodes and and one bidirectional link:

network

Note that to do this in the simulator, you must create a unidirectional link from n1 to n2, and another one from n2 to n1.

Using this network, test the following scenarios:

    Set the bandwidth of the links to 1 Mbps, with a propagation delay of 1 second. Send one packet with 1000 bytes from n1 to n2 at time 0.

    Set the bandwidth of the links to 100 bps, with a propagation delay of 10 ms. Send one packet witih 1000 bytes from n1 to n2 at time 0.

    Set the bandwidth of the links to 1 Mbps, with a propagation delay of 10 ms. Send three packets from n1 to n2 at time 0 seconds, then one packet at time 2 seconds. All packets should have 1000 bytes.

For each scenario, print the time each packet was created, its identifier, and the time it was received
Three Nodes

Use the simulator to setup a simple network consisting of three nodes and two links. Using this network, test the following scenarios:

    Two fast links

    network

    Node A transmits a stream of 1 kB packets to node C. How long does it take to transfer a 1 MB file, divided into 1 kB packets, from A to C? Which type of delay dominates?

    If both links are upgraded to a rate of 1 Gbps, how long does it take to transfer a 1 MB file from A to C?

    One fast link and one slow link

    network

    Node A transmits 1000 packets, each of size 1 kB, to node C. How long would it does it take to transfer a 1 MB file, divided into 1 kB packets, from A to C?

Note that 1 kB = 103 bytes and 1 MB = 106 bytes. These problems are the same as in the first homework, so you should get the same answers in both cases.

To get the right answers, be sure that each packet is sent just as the previous one leaves the first node. You can do this for packet i
by calculating (i−1)

times the transmission delay for single packet, and then scheduling this packet to be sent that much time in the future:

Sim.scheduler.add(delay=calculatedDelay, event=p,
handler=n1.send_packet)

Queueing Theory

Explore whether the simulator can validate basic queueing theory by varying the rate at which packets are generated and measuring the queueing delay for each packet. Queueing theory says that for an M/D/1 queue, the delay should go to infinity as the utilization of the system goes to 1. Recall that the "M" in M/D/1 refers to an exponential distribution on the arrival process, the "D" refers to a deterministic service time, and the "1" refers to a single queue.

Choose a utilization between 0 and 100%, run a simulation, and collect the results. Repeat for utilizations of 10% to 90%, plus 95% and 98% of the maximum link rate. The maximum rate is given by your packet length and link speed. The code in examples/delay.py shows how to generate packets with an exponential distribution.

Each experiment should write its output to a file. Write a Python script that parses the output files from each experiment and produces a line graph of the average queueing delay as a function of link utilization. On the same graph, plot the theoretical queueing delay for the link using the equation w = 1/(2μ) x ρ/(1-ρ). Your graph should look similar to this:

combined-box

Your plots must use Python and pandas. You can use the sample plotting code as a starting point for plotting.
Report

Write a formal, scientific report that includes the following:

    Two Nodes: For each of the three scenarios, show the following: (a) your network configuration (similar to the text files in the networks folder), (b) the output of the simulation, and (c) the calculations you used to verify the output is correct.

    Three Nodes: For each of the scenarios, show (a) your network configuration, (b) the last 5 lines of the simulation output, and (c) the calculations you used to verify the output is correct.

    Queueing Theory: Show the network configuration, explain which loads you generated to send packets, and describe the data you collected. Then show the graph you created and discuss how well the simulator matches the theoretical result.

Be sure that your report is written in a scientific style, with complete sentences and paragraphs that flow together. Your report should be written as if you are explaining your work to another CS student, and they need all of the details of what you did so that they can replicate your experiments.

Your report can be any length, as long as you thoroughly describe your project and results. The paper must use 11 point type, single spacing, and one column per page.

You must use LaTex to write your report. This will make it easy for you to include code and graphs and give them a consistent style. You will also be able to easily regenerate your report whenever you change your graphs, without having to copy and paste them each time. You can use this template for your report.

LaTeX is a useful publishing tool in the academic world, as it automatically formats a paper in many commonly-used conference and journal styles. If I need to send a paper to a different venue, changing one line in a LaTeX file will reformat the paper for submisison to this venue. LaTeX handles all of the formatting you would otherwise have to do by hand -- margins, section headings, placement of figures, and more. I also find it helps me to focus on content, rather than style, when I am writing a paper.

To help you learn LaTeX, I suggest using the WikiBooks LaTex reference.
Submission

Your code and should be located in a directory called lab1 in the top level:

bene/
  src/
  examples/
  lab1/

Turn in a tarball that includes all of your code (for the simulator, experiments, graphing, etc), and a PDF of your report:

tar -czvf bene.tgz bene

using Learning Suite.
Grading

This lab is worth 100 points, and will be graded using the following rubric:

    Two Nodes: 30 points, 10 points per scenario

    Three Nodes: 20 points, 10 points per scenario.

    Queueing Theory: 50 points.

Each part will be graded on the following scale:

    50% for partial work that indicates substantial effort was made
    70% - 80% for C quality work
    80% - 90% for B quality work
    90% - 100% for A quality work

To get full points, the report must be complete and written with a scientific style.
Creative Commons License

