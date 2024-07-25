
import AbstractSyntaxTreeNode

class Tau:
    ''' This class is used to represent the tau node in the control structures.'''
    def __init__(self, n):
        self.n = n

class Beta:
    ''' This class is used to represent the beta node in the control structures.'''
    def __init__(self):
        pass

class CtrlStruct:
    ''' This class is used to represent the control structures generated from the AST.'''
    def __init__(self, index, delta):
        self.index = index
        self.delta = delta

class LambdaExpression:
    ''' This class is used to represent the lambda expression in the control structures.'''
    def __init__(self, environment_index, lambda_index, tok):
        self.environment_index = environment_index
        self.lambda_index = lambda_index
        self.item = tok

    def print_lambda_expression(self):
        if isinstance(self.item, AbstractSyntaxTreeNode.AbstractSyntaxTreeNode):
            pass
        elif isinstance(self.item, list):
            lam_vars = ""
            for it in self.item:
                lam_vars += it.name + ','
                
class ControlStructureGenerator:
    def __init__(self):
        self.curIdxDelta = 0
        self.queue = []
        self.map_ctrl_structs = {}
        self.current_delta=[]

    def print_ctrl_structs(self):
        ''' 
        This function is used to print the control structures generated from the AST.
        It iterates over the map_ctrl_structs dictionary and prints the key and value of each entry.
        '''
        for key, ctrl_struct in self.map_ctrl_structs.items():
            print("key: " + str(key))
            for obj in ctrl_struct:
                if isinstance(obj, AbstractSyntaxTreeNode.AbstractSyntaxTreeNode):
                    if obj.value is not None:
                        print("value: " +  obj.type + str(obj.value))
                    else:
                        print("value: " +  obj.type )
                elif isinstance(obj, LambdaExpression):
                    pass
                elif isinstance(obj, list):
                    for item in obj:
                        if isinstance(item, AbstractSyntaxTreeNode):
                            pass
                        else:
                            pass
                else:
                    print("I was not Token or LambdaExpression, value: " + str(obj))

    def generate_control_structures(self, root):
        ''' 
        This function is used to generate the control structures from the AST.
        It uses pre-order traversal to generate the control structures.
        '''
        delta = []
        self.current_delta = []
        self.pre_order_traversal(root, delta)
        ctrl_delta = CtrlStruct(self.curIdxDelta, delta)
        self.map_ctrl_structs[0] = self.current_delta.copy()

        while len(self.queue)>0:
            self.current_delta = []
            index, node, delta_queue = self.queue[0]
            self.pre_order_traversal(node, delta_queue)
            ctrl_delta = CtrlStruct(index, delta_queue)
            self.map_ctrl_structs[index] = self.current_delta.copy()
            self.queue.pop(0)

        return self.map_ctrl_structs

    def pre_order_traversal(self, root ,delta):
        ''' 
        This function is used to traverse the AST in pre-order fashion and generate the control structures.
        '''
        match root.type:
            case "lambda":
                self.curIdxDelta += 1
                lambda_exp = None
                if root.children.type == ',':
                    tau_list = []
                    children = root.children.children
                    while children is not None:
                        tau_list.append(children)
                        children = children.sib
                    lambda_exp = LambdaExpression(0, self.curIdxDelta, tau_list)
                else:
                    lambda_exp = LambdaExpression(0, self.curIdxDelta, root.children)

                self.current_delta.append(lambda_exp)
                delta_lambda = []
                self.queue.append((self.curIdxDelta, root.children.sib, delta_lambda))
                return
            case "->":
                delta2 = []
                savedcurIdxDelta2 = self.curIdxDelta + 1
                savedcurIdxDelta3 = self.curIdxDelta + 2
                self.curIdxDelta += 2
                node2 = root.children.sib
                node3 = root.children.sib.sib
                node2.sib = None  # to avoid re-traversal
                self.queue.append((savedcurIdxDelta2, node2, delta2))
                delta3 = []
                self.queue.append((savedcurIdxDelta3, node3, delta3))
                self.current_delta.append(CtrlStruct(savedcurIdxDelta2, delta2))
                self.current_delta.append(CtrlStruct(savedcurIdxDelta3, delta3))
                beta = Beta()
                self.current_delta.append(beta)
                root.children.sib = None
                self.pre_order_traversal(root.children, delta)
                return
            case "gamma":
                self.current_delta.append(root)
                self.pre_order_traversal(root.children, delta)
                if root.children.sib is not None:
                    self.pre_order_traversal(root.children.sib, delta)
                return
            case "tau":
                initial_length = len(self.current_delta)
                node = root.children
                next_node = node.sib
                deltas_tau = []
                counter = 0
                while node is not None:
                    node.sib = None
                    self.pre_order_traversal(node, deltas_tau)
                    node = next_node
                    if node is not None:
                        next_node = node.sib
                    counter += 1
                tau = Tau(counter)
                temp = []
                final_length = len(self.current_delta)
                counter = final_length - initial_length
                for i in range(counter):
                    temp.append(self.current_delta.pop())
                self.current_delta.append(tau)
                for i in range(counter):
                    self.current_delta.append(temp.pop())
                if root.sib is not None:
                    self.pre_order_traversal(root.sib, delta)
                return
            case _:
                self.current_delta.append(root)
                if root.children is not None:
                    self.pre_order_traversal(root.children, delta)
                    if root.children.sib is not None:
                        self.pre_order_traversal(root.children.sib, delta)
                return
            








