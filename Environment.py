import logging

from AbstractSyntaxTreeNode import AbstractSyntaxTreeNode


class Environment:
    logger = logging.getLogger(__name__)

    def __init__(self, index):
        """
        Initializes an Environment object.

        Args:
            index (int): The index of the environment.
        """
        self.index = index
        self.map_variables = {}
        self.parent = None

    def set_environmental_parameters(self, parent_env, key, value):
        """
        Sets the environmental parameters.

        Args:
            parent_env (Environment): The parent environment.
            key: The key of the variable.
            value: The value of the variable.
        """
        self.map_variables[key] = value
        if isinstance(key, AbstractSyntaxTreeNode) and isinstance(value, AbstractSyntaxTreeNode):
            pass
        else:
            pass
        self.parent = parent_env

    def get_environment_index(self):
        """
        Returns the index of the environment.

        Returns:
            int: The index of the environment.
        """
        return self.index

    def get_value(self, key):
        """
        Returns the value of a variable.

        Args:
            key: The key of the variable.

        Returns:
            The value of the variable, or None if not found.
        """
        if key in self.map_variables.keys():
            value = self.map_variables[key]
            self.logger.info("found in cur env id {}".format(self.index))
            if isinstance(value, AbstractSyntaxTreeNode):
                self.logger.info("value: {}".format(value.value))
            return value
        else:
            self.logger.info("not found in cur env")
            return None
