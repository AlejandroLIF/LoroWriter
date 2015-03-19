
class procedureDirectory:
	def __init__(self, identifier, parent=None):
		self.identifier = identifier	#directory identifier
		self.parent = parent	#pointer to the directory's parent
		self.variables = {}	#current directory's variable table
		self.directories = {}	#current directory's children
	
	def __str__(self):
		return self.to_string();
	
	def to_string(self, string=''):
		string = str(self.identifier) + "{\n"
		
		if(self.variables):
			string = string + "variables:\n"
			for identifier in self.variables:
				string = string + str(identifier) + " : " + str(self.variables[identifier]) + "\n"
		
		if(self.directories):
			string = string + "\ndirectories:\n"
			for identifier in self.directories:
				string = string + str(self.directories[identifier])
		string = string + "}\n\n"
		return string
	
	def get_variable(self, identifier):
		currDirr = self
		while(currDirr):
			if identifier in self.variables:
				return self.variables[identifier]
			currDirr = currDirr.parent
		return None
		
	def add_variable(self, identifier, variable):
		if identifier in self.variables:
			print "ERROR! Variable \"", str(identifier), " already exists in scope \"", str(self.identifier), "\"!"
			return False
		else:
			self.variables[identifier] = variable
			return True
	
	def rem_variable(self, identifier):
		if identifier in self.variables:
			del self.variables[identifier]
			return True
		else:
			return False
	
	def list_all_variables(self):
		currDirr = self
		string = ""
		while(currDirr):
			string = string + str(currDirr.identifier) + "{\n"
			if(currDirr.variables):
				for identifier in currDirr.variables:
					string = string + str(identifier) + " : " + str(currDirr.variables[identifier]) + "\n"
			string = string + "}\n"
			currDirr = currDirr.parent
		return string
	
	def get_directory(self, identifier):
		if identifier in self.directories:
			return self.directories[identifier]
		else:
			return None
			
	def add_directory(self, directory):
		identifier = directory.identifier
		if identifier in self.directories:
			print "Error! Directory \"", str(identifier)," already exists in scope \"", str(self.identifier), "\"!"
			return False
		else:
			self.directories[identifier] = directory
			return True
	
	def rem_directory(self, identifier):
		if identifier in self.directories:
			del self.directories[identifier]
			return True
		else:
			return False


'''
" BEGIN TEST ROUTINE"
glob = procedureDirectory("global");
glob.add_variable("foo", 5);
glob.add_variable("bar", 6);
method1 = procedureDirectory("method1", glob);
method1.add_variable("var", "a string");
method1.add_variable("foo", 1);
method2 = procedureDirectory("method2", glob);
method2.add_variable("var", 3.14);
method2.add_variable("bar", 2);
glob.add_directory(method1);
glob.add_directory(method2);

print glob
print method1.list_all_variables();
print method2.list_all_variables();
print glob.get_variable("foo");
print method1.get_variable("foo");
'''
