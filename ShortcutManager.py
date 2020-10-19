import sqlite3
import sys
import os

class CommandHandler:
	def __init__(self):
		# C:\Users\username\AppData\Roaming
		self.platform = sys.platform
		self.file_name = "shortcuts.db"

		if self.platform == "win32" or self.platform == "win64":
			self.db_path = f"{os.path.expanduser('~')}\\AppData\\Roaming\\ShortcutManager\\"
		else:
			self.db_path = f"{os.path.expanduser('~')}\\.config\\ShortcutManager\\"

		self.path = self.db_path+self.file_name

		if not os.path.exists(self.db_path):
			os.mkdir(self.db_path)

		if not os.path.exists(self.path):
			with sqlite3.connect(self.path) as conn:
				c = conn.cursor()
				c.execute("CREATE TABLE IF NOT EXISTS shortcuts (name TEXT, command TEXT)")


	def clear(self, start=False):
		os.system("cls" if self.platform == "win32" or self.platform == "win64" else "clear")
		if start:
			print("Welcome to Kip's shortcut program!")
			print("You can view a list of all commands with the command 'help'\n")

	def exit(self, message=False):
		if message:
			print("Alright! Shutting down!")

		exit()

	def uninstall(self):
		self.clear()
		os.remove(self.path)
		os.rmdir(self.db_path)
		os.remove(sys.argv[0])

		print("Succesfully uninstalled all files")
		input("Press any key to continue... ")

		self.exit()
		
	def help(self):
		self.clear()
		print("[Help]")
		print("1. help")
		print("2. clear")
		print("3. start")
		print("4. shortcut <add|remove|list|help>")
		print("5. uninstall")
		print("6. exit\n")

	def shortcut(self, command):
		if command == "help":
			self.shortcut_help()

		elif command[0:3] == "add":
			self.shortcut_add(command.split(" ", 1)[1])

		elif command[0:6] == "remove":
			self.shortcut_remove(command.split(" ", 1)[1])

		elif command[0:4] == "list":
			self.shortcut_list(command)

		else:
			self.shortcut_help()

	def shortcut_help(self):
		self.clear()
		print("| Subcommand  | Description             | Command                       |")
		print("|-------------|-------------------------|-------------------------------|")
		print("| 1. Add      | Adds a new shortcut     | shortcut add <name> <command> |")
		print("| 2. Remove   | Removes a shortcut      | shortcut remove <name>        |")
		print("| 3. List     | Lists all the shortcuts | shortcut list [-D]            |")
		print("| 4. Help     | Shows this page         | shortcut help                 |")
		print("|-------------|-------------------------|-------------------------------|")
		print("")

	def shortcut_add(self, command):
		self.clear()

		with sqlite3.connect(self.path) as conn:
			c = conn.cursor()

			parts = command.split(" ", 1)
			c.execute("INSERT INTO shortcuts VALUES (?, ?)", (parts[0], parts[1]))
			conn.commit()

		print("Succesfully added the shortcut!\n")

	def shortcut_remove(self, command):
		self.clear()
		with sqlite3.connect(self.path) as conn:
			c = conn.cursor()

			c.execute("DELETE FROM shortcuts WHERE name=?", (command,))
			conn.commit()

		print("Succesfully removed the shortcut\n")

	def shortcut_list(self, command):
		self.clear()

		try:
			options = command.split(" ", 1)[1]
		except:
			options = None

		with sqlite3.connect(self.path) as conn:
			c = conn.cursor()
			c.execute("SELECT * FROM shortcuts")

			result = c.fetchall()

		print("[List of all Shortcuts]")
		for index, shortcut in enumerate(result):
			print(f"{index+1}. {shortcut[0]}   {shortcut[1]}" if options == "-D" else f"{index+1}. {shortcut[0]}")

		print("")

	def start(self, name):
		self.clear()

		with sqlite3.connect(self.path) as conn:
			c = conn.cursor()

			c.execute("SELECT * FROM shortcuts WHERE name=?", (name,))
			result = c.fetchall()

		if len(result) == 0:
			print("We could not find any shortcuts with that name!")
			print("To see a full list of your shortcuts, type the command 'shortcut list'\n")
			return

		print("[Text Result]")
		os.system(result[0][1])
		print()



def main():
	command_handler = CommandHandler()
	command_handler.clear(start=True)

	while True:
		command = str(input(">> "))
		command_handler.clear()

		if command == "clear":
			command_handler.clear(start=True)

		elif command == "exit":
			command_handler.exit(message=True)

		elif command == "help":
			command_handler.help()

		elif command == "uninstall":
			command_handler.uninstall()

		elif command[0:5] == "start":
			command_handler.start(command.split(" ", 1)[1])

		elif command[0:8] == "shortcut":
			command_handler.shortcut(command.split(" ", 1)[1])

		else:
			command_handler.help()



if __name__ == "__main__":
	main()