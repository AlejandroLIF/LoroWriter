#Begin class Variable
class Variable:
    def __init__(self, Name='0', Type=int, Address='0'):
        self.Name = Name
        self.Type = Type
        self.Address = Address
        
    def __str__(self):
        return "{}\t{}\t{}".format(str(self.Name), str(self.Type), str(self.Address))
#End class Variable

#Begin class procedureDirectory
class procedureDirectory:
    def __init__(self, identifier, parent=None):
        self.identifier = identifier    #directory identifier
        self.parent = parent    #pointer to the directory's parent
        self.parameters = {}     #current directory's parameter table
        self.variables = {}     #current directory's variable table
        self.directories = {}   #current directory's children
        self.nextIndex = 0      #used in calculating the next available memory address vor an added variable
        self.constants = {}     #stores the value of constants
    
    def __str__(self):
        return self.to_string()
    
    def to_string(self,):
        string = str(self.identifier) + "{\n"
        
        if(self.parameters):
            string = string + "parameters:\n"
            for identifier in self.parameters:
                string = string + str(self.parameters[identifier])
                #Append the constant value to constant variables
                try:
                    string = string + " := " + str(self.constants[identifier])
                except KeyError:
                    pass
                string = string + "\n"

        if(self.variables):
            string = string + "variables:\n"
            for identifier in self.variables:
                string = string + str(self.variables[identifier])
                #Append the constant value to constant variables
                try:
                    string = string + " := " + str(self.constants[identifier])
                except KeyError:
                    pass
                string = string + "\n"
        
        if(self.directories):
            string = string + "\ndirectories:\n"
            for identifier in self.directories:
                string = string + str(self.directories[identifier])
        string = string + "}\n\n"
        return string

    def get_parameter(self, identifier):
        currDir = self
        while currDir:
            if identifier in currDir.parameters:
                return currDir.parameters[identifier]
            currDir = currDir.parent
        return None
        
    def get_variable(self, identifier):
        currDir = self
        while currDir:
            if identifier in currDir.variables:
                return currDir.variables[identifier]
            currDir = currDir.parent
        return None
        
    def add_parameter(self, identifier, variableType):
        if identifier in self.parameters:
            print "Error! Variable \"{}\" already exists in current scope as \"{}\"!".format(str(identifier), str(self.parameters[identifier]))
            return False
        else:
            self.parameters[identifier] = Variable(identifier, variableType, self.next_address(variableType))
            return True
            
    def add_variable(self, identifier, variableType):
        if identifier in self.variables:
            print "Error! Variable \"{}\" already exists in current scope as \"{}\"!".format(str(identifier), str(self.variables[identifier]))
            return False
        else:
            self.variables[identifier] = Variable(identifier, variableType, self.next_address(variableType))
            return True
    
    def add_temp(self, variableType):
        identifier = "temp_{}_{}".format(str(variableType), self.nextIndex + 1)
        if self.add_variable(identifier, variableType):
            return self.variables[identifier]
        else:
            return False
        
    def add_const(self, variableType, variableValue):
        identifier = "const_{}_{}".format(str(variableType), self.nextIndex + 1)
        if self.add_variable(identifier, variableType):
            self.constants[identifier] = variableValue
            return self.variables[identifier]
        else:
            return False
    
    #TODO:  This function returns the next-available memory location that may store a variable of type variableType
    #       it is a prototype placeholder and must be updated once the virtual machine's memory structure is defined.
    def next_address(self, variableType):
        self.nextIndex += 1
        return "{}_{}".format(str(variableType), str(self.nextIndex))
    
    def rem_parameter(self, identifier):
        if identifier in self.parameters:
            del self.parameters[identifier]
            return True
        else:
            return False    
            
    def rem_variable(self, identifier):
        if identifier in self.variables:
            del self.variables[identifier]
            return True
        else:
            return False

    def list_all_parameters(self):
        currDirr = self
        string = ""
        while(currDirr):
            string = string + str(currDirr.identifier) + "{\n"
            if(currDirr.parameters):
                for identifier in currDirr.parameters:
                    string = string + str(currDirr.parameters[identifier]) + "\n"
            string = string + "}\n"
            currDirr = currDirr.parent
        return string
    
    def list_all_variables(self):
        currDirr = self
        string = ""
        while(currDirr):
            string = string + str(currDirr.identifier) + "{\n"
            if(currDirr.variables):
                for identifier in currDirr.variables:
                    string = string + str(currDirr.variables[identifier]) + "\n"
            string = string + "}\n"
            currDirr = currDirr.parent
        return string
    
    def get_directory(self, identifier):
        if identifier in self.directories:
            return self.directories[identifier]
        else:
            return None
            
    def add_directory(self, identifier):
        if identifier in self.directories:
            print "Error! Directory \"{}\" already exists in scope: \"{}\"!".format(str(identifier), str(self.identifier))
            return False
        else:
            self.directories[identifier] = procedureDirectory(identifier, self)
            return True
    
    def rem_directory(self, identifier):
        if identifier in self.directories:
            del self.directories[identifier]
            return True
        else:
            return False
#End class procedureDirectory

#Test routine
if __name__ == '__main__':
    glob = procedureDirectory("global");
    glob.add_variable("foo", int)
    glob.add_variable("bar", int)
    
    glob.add_directory("method 1")
    glob = glob.get_directory("method 1")
    glob.add_variable("var", str)
    glob.add_variable("foo", int)
    glob = glob.parent
    
    glob.add_directory("method 2")
    glob = glob.get_directory("method 2")
    glob.add_variable("var", float)
    glob.add_variable("bar", int)
    glob = glob.parent
    
    glob.add_directory("method 1")

    print glob
    print glob.get_directory("method 1").list_all_variables()
    print glob.get_directory("method 2").list_all_variables()
    print 'global foo is: ', glob.get_variable("foo")
    print 'method 1 foo is: ',glob.get_directory("method 1").get_variable("foo")
    print 'method 2 foo is: ', glob.get_directory("method 2").get_variable("foo")
    
