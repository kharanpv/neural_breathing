import re
import copy

class Connection:
    def __init__(self, start_node, end_node, connection_type):
        self.start_node = start_node
        self.end_node = end_node
        self.connection_type = connection_type.lower()
        
        if self.connection_type not in ['excitatory', 'inhibitory']:
            raise ValueError("Connection type must be either 'excitatory' or 'inhibitory'")

class Node:
    def __init__(self, value, N=1, node_type=None):
        """
        Initialize a Node with value, threshold N, and explicit type.
        
        Args:
            value: 0 or 1
            N: Activation threshold
            node_type: 'input', 'output', or None (regular node)
        """
        if value not in [0, 1]:
            raise ValueError("Node value must be either 0 or 1")
        if node_type not in ['input', 'output', None]:
            raise ValueError("Node type must be 'input', 'output', or None")
            
        self.value = value
        self.N = N
        self.node_type = node_type
        self.incoming_connections = []
        self.outgoing_connections = []
    
    def add_incoming_connection(self, connection):
        if connection.end_node != self:
            raise ValueError("Connection end node doesn't match this node")
        self.incoming_connections.append(connection)
    
    def add_outgoing_connection(self, connection):
        if connection.start_node != self:
            raise ValueError("Connection start node doesn't match this node")
        self.outgoing_connections.append(connection)
    
    def update_value(self):
        if self.node_type == 'input':
            return  # Input nodes keep their driven values
        
        excitatory_activated = 0
        any_inhibitory_activated = False

        for conn in self.incoming_connections:
            if conn.connection_type == 'excitatory' and conn.start_node.value == 1:
                excitatory_activated += 1
            elif conn.connection_type == 'inhibitory' and conn.start_node.value == 1:
                any_inhibitory_activated = True

        if excitatory_activated >= self.N and not any_inhibitory_activated:
            self.value = 1
        else:
            self.value = 0
    
    def __repr__(self):
        type_str = f", type={self.node_type}" if self.node_type else ""
        return f"Node(value={self.value}, N={self.N}{type_str}, {len(self.incoming_connections)} in, {len(self.outgoing_connections)} out)"

def simulate_network(nodes, input_sequence):
    input_nodes = [n for n in nodes if n.node_type == 'input']
    output_nodes = [n for n in nodes if n.node_type == 'output']

    if not input_nodes:
        raise ValueError("No input nodes found")
    if not output_nodes:
        raise ValueError("No output nodes found")

    outputs = []

    for char in input_sequence:
        input_val = int(char)

        # Create a copy of all nodes
        nodes_copy = copy.deepcopy(nodes)
        
        for i, node in enumerate(nodes_copy):
            # Drive input values
            if node.node_type == 'input':
                nodes_copy[i].value = input_val

            else:
                total_inhibitory = sum(nodes[nodes.index(conn.start_node)].value for conn in nodes[i].incoming_connections
                            if conn.connection_type == 'inhibitory')
                
                if total_inhibitory == 0:
                    total_excitatory = sum(nodes[nodes.index(conn.start_node)].value for conn in nodes[i].incoming_connections
                            if conn.connection_type == 'excitatory')
                    
                    new_val = 1 if total_excitatory >= node.N else 0
                    
                else:
                    new_val = 0

                nodes_copy[i].value = new_val
        
        # Update nodes with new values
        nodes = nodes_copy
        output_nodes = [n for n in nodes if n.node_type == 'output']

        # Collect output values
        if len(output_nodes) == 1:
            outputs.append(str(nodes[nodes.index(output_nodes[0])].value))
        else:
            outputs.append(''.join(str(nodes[nodes.index(n)]) for n in output_nodes))

    return ''.join(outputs)

def create_network_from_string(network_str):
    node_pattern = re.compile(r'(?P<num>\d+)(?P<type>[ioIO]?)(?:N(?P<thresh>\d+))?')

    nodes = []
    node_map = {}  # Only source nodes populate this
    edges = []  # (source_num, target_num)

    for defn in network_str.split(';'):
        if not defn.strip():
            continue

        lhs_rhs = defn.split('-')
        lhs_raw = lhs_rhs[0].strip()
        rhs_raw = lhs_rhs[1].strip() if len(lhs_rhs) > 1 else ''

        lhs_match = node_pattern.fullmatch(lhs_raw)
        if not lhs_match:
            raise ValueError(f"Invalid node format on LHS: '{lhs_raw}'")

        src_num = int(lhs_match['num']) - 1
        src_type = {'i': 'input', 'o': 'output'}.get(lhs_match['type'].lower()) if lhs_match['type'] else None
        src_thresh = int(lhs_match['thresh']) if lhs_match['thresh'] else 1

        # Set or update source node info
        node_map[src_num] = {
            'type': src_type,
            'N': src_thresh
        }

        for tgt_str in rhs_raw.split(','):
            tgt_str = tgt_str.strip()
            if not tgt_str:
                continue

            tgt_match = node_pattern.fullmatch(tgt_str)
            if not tgt_match:
                raise ValueError(f"Invalid node format on RHS: '{tgt_str}'")

            tgt_num = int(tgt_match['num']) - 1
            edges.append((src_num, tgt_num))

    # Now we can allocate the node list
    max_index = max(max(node_map.keys(), default=-1), max((t for _, t in edges), default=-1))
    nodes = [None] * (max_index + 1)

    for idx, info in node_map.items():
        nodes[idx] = Node(0, N=info['N'], node_type=info['type'])

    for src_num, tgt_num in edges:
        src_node = nodes[src_num]
        tgt_node = nodes[tgt_num]

        if src_node is None:
            raise ValueError(f"Source node {src_num + 1} is undefined")

        if tgt_node is None:
            raise ValueError(f"Target node {tgt_num + 1} is undefined or missing a source definition")

        conn = Connection(src_node, tgt_node, 'excitatory')
        src_node.add_outgoing_connection(conn)
        tgt_node.add_incoming_connection(conn)

    return nodes