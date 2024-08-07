from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import torch
from torch_geometric.data import Data
from .utils.data_utils import construct_node_feature
from .utils.dag_utils import return_order_info

# class OrderedData(Data):
#     def __init__(self, edge_index=None, x=None, y=None, \
#                  tt_pair_index=None, tt_dis=None, \
#                  rc_pair_index=None, is_rc=None, \
#                  forward_level=None, forward_index=None, backward_level=None, backward_index=None):
#         super().__init__()
#         self.edge_index = edge_index
#         self.tt_pair_index = tt_pair_index
#         self.x = x
#         self.y = y
#         self.tt_dis = tt_dis
#         self.forward_level = forward_level
#         self.forward_index = forward_index
#         self.backward_level = backward_level
#         self.backward_index = backward_index
#         self.rc_pair_index = rc_pair_index
#         self.is_rc = is_rc
    
#     def __inc__(self, key, value, *args, **kwargs):
#         if 'index' in key or 'face' in key:
#             return self.num_nodes
#         else:
#             return 0

#     def __cat_dim__(self, key, value, *args, **kwargs):
#         if key == 'forward_index' or key == 'backward_index':
#             return 0
#         elif key == "edge_index" or key == 'tt_pair_index' or key == 'rc_pair_index':
#             return 1
#         else:
#             return 0
        
class OrderedData(Data):
    def __init__(self, edge_index=None, x=None, y=None, \
                 tt_pair_index=None, tt_dis=None, \
                 forward_level=None, forward_index=None, backward_level=None, backward_index=None):
        super().__init__()
        self.edge_index = edge_index
        self.tt_pair_index = tt_pair_index
        self.x = x
        self.y = y
        self.tt_dis = tt_dis
        self.forward_level = forward_level
        self.forward_index = forward_index
        self.backward_level = backward_level
        self.backward_index = backward_index
    
    def __inc__(self, key, value, *args, **kwargs):
        if 'index' in key or 'face' in key:
            return self.num_nodes
        else:
            return 0

    def __cat_dim__(self, key, value, *args, **kwargs):
        if key == 'forward_index' or key == 'backward_index':
            return 0
        elif key == "edge_index" or key == 'tt_pair_index' or key == 'connect_pair_index':
            return 1
        else:
            return 0
# def parse_pyg_mlpgate(x, edge_index, tt_dis, tt_pair_index, \
#                       y, rc_pair_index, is_rc, \
#                       num_gate_types=3):
#     x_torch = construct_node_feature(x, num_gate_types)

#     tt_pair_index = torch.tensor(tt_pair_index, dtype=torch.long)
#     tt_pair_index = tt_pair_index.t().contiguous()
#     rc_pair_index = torch.tensor(rc_pair_index, dtype=torch.long)
#     rc_pair_index = rc_pair_index.t().contiguous()
#     tt_dis = torch.tensor(tt_dis)
#     is_rc = torch.tensor(is_rc, dtype=torch.float32).unsqueeze(1)

#     edge_index = torch.tensor(edge_index, dtype=torch.long)
    
#     if len(edge_index) == 0:
#         edge_index = edge_index.t().contiguous()
#         forward_index = torch.LongTensor([i for i in range(len(x))])
#         backward_index = torch.LongTensor([i for i in range(len(x))])
#         forward_level = torch.zeros(len(x))
#         backward_level = torch.zeros(len(x))
#     else:
#         edge_index = edge_index.t().contiguous()
#         forward_level, forward_index, backward_level, backward_index = return_order_info(edge_index, x_torch.size(0))

#     graph = OrderedData(x=x_torch, edge_index=edge_index, 
#                         rc_pair_index=rc_pair_index, is_rc=is_rc,
#                         tt_pair_index=tt_pair_index, tt_dis=tt_dis, 
#                         forward_level=forward_level, forward_index=forward_index, 
#                         backward_level=backward_level, backward_index=backward_index)
#     graph.use_edge_attr = False

#     # add reconvegence info
#     # graph.rec = torch.tensor(x[:, 3:4], dtype=torch.float)
#     # graph.rec_src = torch.tensor(x[:, 4:5], dtype=torch.float)
#     # add gt info
#     # add indices for gate types
#     graph.gate = torch.tensor(x[:, 1:2], dtype=torch.float)
#     graph.prob = torch.tensor(y).reshape((len(x), 1))

#     return graph


def parse_pyg_mlpgate(x, edge_index, tt_dis, tt_pair_index, is_pi, \
                        prob, no_edges, connect_label, connect_pair_index, \
                        backward_level, forward_index, forward_level, \
                        no_nodes, backward_index, \
                        ):
    
    # x_torch = construct_node_feature(x, num_gate_types)
    # print(x_torch)
    x_torch = torch.LongTensor(x)
    # print(x_torch)

    tt_pair_index = torch.tensor(tt_pair_index, dtype=torch.long)
    # tt_pair_index = tt_pair_index.t().contiguous()

    # rc_pair_index = torch.tensor(rc_pair_index, dtype=torch.long)
    # rc_pair_index = rc_pair_index.t().contiguous()

    tt_dis = torch.tensor(tt_dis)
    # print(tt_sim)

    # is_rc = torch.tensor(is_rc, dtype=torch.float32).unsqueeze(1)

    edge_index = torch.tensor(edge_index, dtype=torch.long).contiguous()
    
    connect_pair_index = torch.tensor(connect_pair_index, dtype=torch.long).contiguous()
    connect_label = torch.tensor(connect_label)
    
    forward_level = torch.tensor(forward_level)
    backward_level = torch.tensor(backward_level)

    forward_index = torch.tensor(forward_index)
    backward_index = torch.tensor(backward_index)
    
    if len(connect_pair_index) == 0 or connect_pair_index.shape[1] == 0:
        connect_pair_index = connect_pair_index.reshape((2, 0))

    # graph = OrderedData(x=x_torch, edge_index=edge_index, 
    #                     rc_pair_index=rc_pair_index, is_rc=is_rc,
    #                     tt_pair_index=tt_pair_index, tt_dis=tt_dis, 
    #                     forward_level=forward_level, forward_index=forward_index, 
    #                     backward_level=backward_level, backward_index=backward_index)
    graph = OrderedData(x=x_torch, edge_index=edge_index, y=None,
                        tt_pair_index=tt_pair_index, tt_dis=tt_dis, 
                        forward_level=forward_level, forward_index=forward_index, 
                        backward_level=backward_level, backward_index=backward_index)
    graph.use_edge_attr = False
    graph.connect_label = connect_label
    graph.connect_pair_index = connect_pair_index

    # add reconvegence info
    # graph.rec = torch.tensor(x[:, 3:4], dtype=torch.float)
    # graph.rec_src = torch.tensor(x[:, 4:5], dtype=torch.float)
    # add gt info
    # add indices for gate types
    graph.gate = torch.tensor(x[:, 1:2], dtype=torch.float)
    graph.prob = torch.tensor(prob).reshape((len(x)))

    return graph
