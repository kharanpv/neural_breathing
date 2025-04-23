from Network import *

network_string = "1i-2;2-3,12;3-4,12;4-5,12;5-6,12;6-7,12;7-8,12;8-9,12;9-10,12;10-11,12;11-12;12oN4"
network = create_network_from_string(network_string)

network_input = '111111'
network_output = simulate_network(network, network_input)
print(network_output)