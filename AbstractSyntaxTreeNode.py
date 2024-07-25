class AbstractSyntaxTreeNode:
    def standard(self, root):
        # Check if root is None
        if root == None:
            return None

        # Recursively call standard() on root's children
        root.children = self.standard(root.children)

        # Recursively call standard() on root's sibling
        if root.sib != None:
            root.sib = self.standard(root.sib)

        nextsib = root.sib;

        # Match root's type
        match root.type:
            case "let":
                # Check if root's children's type is "="
                if root.children.type == "=":
                    equal = root.children
                    P_Node = equal.sib
                    X_Node = equal.children
                    E_Node = X_Node.sib

                    # Create new nodes for lambda and gamma
                    lam_Node = AbstractSyntaxTreeNode("lambda")
                    gam_Node = AbstractSyntaxTreeNode("gamma")

                    # Build the new tree structure
                    gam_Node.children = lam_Node
                    lam_Node.sib = E_Node
                    X_Node.sib = P_Node
                    lam_Node.children = X_Node
                    gam_Node.sib = nextsib

                    return gam_Node
                else:
                    root.sib = nextsib
                    return root

            case "where":
                # Check if root's children's sibling's type is "="
                if root.children.sib.type == "=":
                    P_Node = root.children
                    equal = P_Node.sib
                    X_Node = equal.children
                    E_Node = X_Node.sib

                    # Create new nodes for lambda and gamma
                    lam_Node = AbstractSyntaxTreeNode("lambda")
                    gam_Node = AbstractSyntaxTreeNode("gamma")

                    # Build the new tree structure
                    gam_Node.children = lam_Node
                    lam_Node.sib = E_Node
                    lam_Node.children = X_Node
                    X_Node.sib = P_Node
                    P_Node.sib = None
                    gam_Node.sib = nextsib

                    return gam_Node
                else:
                    root.sib = nextsib
                    return root

            case "function_form":
                P_Node = root.children
                V = P_Node.sib
                Vs = V.sib

                # Create a new root node and set its children
                newRoot = AbstractSyntaxTreeNode("=")
                newRoot.children = P_Node

                # Create a lambda node
                lam_Node = AbstractSyntaxTreeNode("lambda")
                P_Node.sib = lam_Node
                lam_Node.previous = P_Node

                # Build the new tree structure
                while Vs.sib != None:
                    lam_Node.children = V
                    lam_Node = AbstractSyntaxTreeNode("lambda")
                    V.sib = lam_Node
                    lam_Node.previous = V
                    V = Vs
                    Vs = Vs.sib

                lam_Node.children = V
                V.sib = Vs
                Vs.previous = V

                newRoot.sib = nextsib

                return newRoot

            case "within":
                # Check if root's children's type is "=" and its sibling's type is "="
                if root.children.type == "=" and root.children.sib.type == "=":
                    eq1 = root.children
                    eq2 = eq1.sib
                    X1 = eq1.children
                    E1 = X1.sib
                    X2 = eq2.children
                    E2 = X2.sib

                    # Create a new root node and set its children
                    newRoot = AbstractSyntaxTreeNode("=")
                    newRoot.children = X2

                    # Create gamma and lambda nodes
                    gamma = AbstractSyntaxTreeNode("gamma")
                    lam_Node = AbstractSyntaxTreeNode("lambda")

                    # Build the new tree structure
                    X2.sib = gamma
                    gamma.previous = X2
                    gamma.children = lam_Node
                    lam_Node.sib = E1
                    E1.previous = lam_Node
                    lam_Node.children = X1
                    X1.sib = E2
                    E2.previous = X1
                    E1.sib = None
                    newRoot.sib = nextsib

                    return newRoot
                else:
                    root.sib = nextsib
                    return root

            case "and":
                eq = root.children

                # Create a new root node and set its children
                newRoot = AbstractSyntaxTreeNode("=")
                comma = AbstractSyntaxTreeNode(",")
                tau = AbstractSyntaxTreeNode("tau")

                newRoot.children = comma
                comma.sib = tau
                tau.previous = comma

                # Build the new tree structure
                X_Node = eq.children
                E_Node = X_Node.sib

                comma.children = X_Node
                tau.children = E_Node

                eq = eq.sib
                while eq != None:
                    X_Node.sib = eq.children
                    eq.children.previous = X_Node
                    E_Node.sib = eq.children.sib
                    eq = eq.sib
                    X_Node = X_Node.sib
                    E_Node = E_Node.sib

                X_Node.sib = None
                E_Node.sib = None
                newRoot.sib = nextsib

                return newRoot

            case "rec":
                eq = root.children
                X_Node = eq.children
                E_Node = X_Node.sib

                # Create a new root node and set its children
                new_root = AbstractSyntaxTreeNode("=")
                new_root.children = X_Node

                # Create a copy of X_Node
                copy_X = X_Node.createCopy()
                gamma = AbstractSyntaxTreeNode("gamma")
                X_Node.sib = gamma
                gamma.previous = X_Node

                # Create Y* and lambda nodes
                y_star = AbstractSyntaxTreeNode("Y*")
                gamma.children = y_star
                lambda_ = AbstractSyntaxTreeNode("lambda")
                y_star.sib = lambda_
                lambda_.previous = y_star

                # Build the new tree structure
                lambda_.children = copy_X
                copy_X.sib = E_Node
                E_Node.previous = copy_X
                new_root.sib = nextsib

                return new_root

            case "@":
                E1 = root.children
                N = E1.sib
                E2 = N.sib

                # Create a new root node and set its children
                new_root = AbstractSyntaxTreeNode("gamma")
                gamma_l = AbstractSyntaxTreeNode("gamma")

                new_root.children = gamma_l
                gamma_l.sib = E2
                gamma_l.children = N
                N.sib = E1
                E1.sib = None
                new_root.sib = nextsib

                return new_root

            case _:
                return root

        return root

    def __init__(self, type):
        self.type = type
        self.value = None
        self.sourceLineNumber = -1
        self.children = None
        self.sib = None
        self.previous = None
        self.indentation = 0

    def print_tree(self):
        if self.children:
            self.children.print_tree()
        if self.sib:
            self.sib.print_tree()

    def print_tree_to_cmd(self):
        for i in range(self.indentation):
            print(".", end="")
        if self.value is not None:
            print("<"+str(self.type.split(".")[1]) +":" + str(self.value)+">")
        else:
            print(str(self.type))

        if self.children:
            self.children.indentation = self.indentation + 1
            self.children.print_tree_to_cmd()
        if self.sib:
            self.sib.indentation = self.indentation
            self.sib.print_tree_to_cmd()

    def print_tree_to_file(self, file):
        for i in range(self.indentation):
            file.write(".")
        if self.value is not None:
            file.write("<"+str(self.type.split(".")[1])+":"+str(self.value)+">" + "\n")
        else:
            file.write(str(self.type) + "\n")

        if self.children:
            self.children.indentation = self.indentation + 1
            self.children.print_tree_to_file(file)
        if self.sib:
            self.sib.indentation = self.indentation
            self.sib.print_tree_to_file(file)

    def createCopy (self):
        node = AbstractSyntaxTreeNode(self.type)
        node.value = self.value
        node.sourceLineNumber = self.sourceLineNumber
        node.children = self.children
        node.sib = self.sib
        node.previous = self.previous
        return node

