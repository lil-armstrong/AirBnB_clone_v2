#!/usr/bin/python3
from cmd import Cmd
from models.base_model import BaseModel
from models.user import User
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
import models
import signal
import re
import sys
import json
storage = models.storage

"""Console module is the entry point of the command interpreter"""


class HBNBCommand (Cmd):
    """
    Class definition of the command interpreter

    Attributes:
        prompt(str): The command prompt.
    """
    __classes = {
        "BaseModel",
        "User",
        "City",
        "Amenity",
        "State",
        "Review",
        "Place",
    }

    prompt = "(hbnb) "
    file = "cmd.json"
    _interrupted = False

    def _ctrl_c_handler(self, signal, frame):
        """Ctrl+C interrupt handler"""
        self._interrupted = True

    def precmd(self, line):
        """@Override Cmd.precmd method"""
        if self._interrupted:
            self._interrupted = False
            return ''

        if line == 'EOF':
            return 'quit'

        return self.parse(line)

    def isMissingClass(self, cls):
        """Check if class name is missing"""
        if cls is None:
            print("** class name missing **", file=sys.stderr)
            return True
        return False

    def isValidClass(self, cls):
        """Check is class name is valid"""

        if cls in HBNBCommand.__classes:
            return True

        print("** class doesn't exist **", file=sys.stderr)
        return False

    def isIdMissing(self, id):
        """Check if Id is None"""
        if id is None or len(id) == 0:
            print("** instance id missing **", file=sys.stderr)
            return True
        return False

    def getInstanceByKey(self, key: str):
        """Check if the instance of the class name does exist for the id"""
        objs = storage.all()

        if key in objs:
            return objs[key]

        print("** no instance found **", file=sys.stderr)
        return None

    def do_quit(self, line):
        """Quit command to exit the program.\n"""
        return True

    def do_EOF(self, line):
        """EOF signal to exit the program.\n"""
        return 'quit'

    def emptyline(self):
        """Override Cmd.emptylines method.\n"""
        pass

    def do_help(self, line=""):
        """\x1b[32m\x1b[1mhelp\x1b[0m
\x1b[32m\x1b[1mhelp\x1b[0m\x1b[34m\x1b[1m *\x1b[0m
\x1b[32m\x1b[1mhelp\x1b[0m [\x1b[34m\x1b[1mcommand\x1b[0m...]
Without arguments, shows the list of available commands.
With arguments, shows the help for one or more commands.
Use "\x1b[34m\x1b[1mhelp *\x1b[0m" to show help for all commands at once.
The question mark "\x1b[34m\x1b[1m?\x1b[0m" can be used as an alias for
"\x1b[34m\x1b[1mhelp\x1b[0m".\n"""

        (command, args, ln) = Cmd.parseline(self, line)

        if command is None:
            Cmd.do_help(self, line)
            return False

        commands = set(line.split())
        if "*" in commands:
            commands = self.get_names()
            commands = [i[3:] for i in commands if i.startswith(("do_"))]
            commands.sort()

        for cmd in commands:
            Cmd.do_help(self, cmd)

    def do_create(self, line: str) -> None:
        """Usage: create <class>
Create a new class instance and print its id.\n

Parameters:
  line(str): commandline expression
"""
        try:
            (cmd, args, ln) = Cmd.parseline(self, line)
            if cmd is None:
                self.stdout.write("** class name missing **\n")
                return False

            else:
                if cmd not in HBNBCommand.__classes:
                    self.stdout.write("** class doesn't exist **\n")
                    return False
            cls = eval(cmd)
            parsed_arg = parseArgs(args)

            if isinstance(parsed_arg, (tuple,)):
                instance = cls(*parsed_arg)
            elif isinstance(parsed_arg, (dict)):
                instance = cls(**parsed_arg)
            else:
                cls()
        except Exception as e:
            print(e, file=sys.stderr)
            pass
        else:
            instance.save()
            self.stdout.write("{}\n".format(instance.id))

    def do_show(self, line: str):
        """show model id
Print the string representation of an instance based \
on the class name and id
"""

        (cmd, args, ln) = Cmd.parseline(self, line)
        if (self.isValidClass(cmd) and not self.isMissingClass(cmd)):
            ids = parseArgs(args.replace('id=', r''))

            for id in ids:
                if (not self.isIdMissing(id)):
                    key = storage.makeKey(cmd, id)
                    instance = self.getInstanceByKey(key)
                    if (instance is not None):
                        self.stdout.write("{}\n".format(str(instance)))

    def do_destroy(self, line):
        """Usage: destroy <class> <id> or <class>.destroy(<id>)\n
Delete a class instance based on the model name and id.
"""
        (cmd, args, ln) = Cmd.parseline(self, line)

        if (self.isValidClass(cmd) and not self.isMissingClass(cmd)):
            ids = parseArgs(args.replace('id=', r''))
            for id in ids[:1]:
                if (not self.isIdMissing(id)):
                    key = storage.makeKey(cmd, id)
                    instance = self.getInstanceByKey(key)
                    if (instance is not None):
                        storage.remove(key)
                        storage.save()

    def do_count(self, line: str):
        """Usage: count <class> or <class>.count()\n
Retrieve the number of instances of a given class.
"""
        (cmd, args, ln) = Cmd.parseline(self, line)
        stored = storage.all()
        count = len(stored)

        try:

            if ln:
                count = {}
                models = set(re.split(r'[, ]+', ln))
                for model in models:
                    if model not in HBNBCommand.__classes:
                        raise Exception("** class doesn't exist **")
                    for item in stored.values():
                        if item.__class__.__name__ == model:
                            count[model] = count.get(model, 0) + 1

        except Exception as e:
            print(e, file=sys.stderr)
        else:
            self.stdout.write("{}\n".format(count))

    def do_all(self, line: str):
        """Usage: all or all <class> or <class>.all()
Display string representations of all instances of a given class. 
If no class is specified, displays all instantiated objects.
"""
        (cmd, args, ln) = Cmd.parseline(self, line)
        stored = storage.all()
        found = []
        if ln:
            models = set(re.split(r'[, ]+', ln))
            for model in models:
                if model not in HBNBCommand.__classes:
                    print("** class doesn't exist **", file=sys.stderr)
                else:
                    for obj in stored.values():
                        if model == obj.__class__.__name__:
                            found.append(str(obj))
        else:
            found = [v for v in stored.values()]
        for f in found:
            print([f])

    def do_update(self, line: str):
        """update
Usage: update <class name> <id> <attribute name> "<attribute value>"
Updates an instance based on the class name and id by adding or updating \
attribute.
"""
        try:
            (cmd, args, ln) = Cmd.parseline(self, line)

            if (not self.isMissingClass(cmd)):
                if (self.isValidClass(cmd)):
                    if (not self.isIdMissing(args)):
                        parg = parseArgs(args)
                        if isinstance(parg, (tuple,)):
                            (id, *attrib) = parg
                        else:
                            id = parg.pop('id')
                            attrib = parg

                        key = storage.makeKey(cmd, id)
                        instance = self.getInstanceByKey(key)

                        if (instance is not None):
                            if len(attrib) == 0:
                                raise ValueError(
                                    "** attribute name missing **\n")
                            if isinstance(attrib, (list)):
                                index = 2
                                while index <= len(attrib):
                                    [key, value] = attrib[index-2: index]
                                    index = index + 2

                                    instance.update(key, value)
                            else:
                                for k, v in attrib:
                                    instance.update(k, v)
        except Exception as e:
            print("[**do_update**]", e, file=sys.stderr)
            return False
        else:
            storage.save()

    def do_fake(self, line: str):
        """Fake command"""
        (cmd, args, ln) = Cmd.parseline(self, line)
        print((cmd, parseArgs(args), ln), )

    def parse(self, line: str):
        """Custom commandline parser"""
        pattern = re.compile(r"([A-Za-z]?=*\S*)\.([A-Za-z]?=*\S*)\((.*)[,]*\)")
        match = pattern.search(line)
        return_value = line
        # get list of supported cmd commands
        names = self.get_names()
        # commands = line.strip().split(".")
        # Handle dotted command
        if match and len(match.groups()) >= 2:
            # mtd, *args = mtd.split("(")
            try:
                (cls, mtd, args) = match.groups()

                # keyworded argument
                if mtd in [x[3:] for x in names
                           if x.startswith("do_")]:
                    command = "{} {} {}".format(mtd, cls, args)

                    return_value = command
            except Exception as e:
                print("[**parse**] ({})".format(e), file=sys.stderr)
                pass

        return return_value


def parseArgs(arg: str):
    """ Parses commandline arguments as tuple or dict
    If arguments are of the format `<key>`=`<value>`\
        return a dictionary of key value pairs
    else
    return `tuple`

    Returns:
        (`dict` | `tuple`)
    """

    regex = re.compile(
        r"(?P<key>\S+)=(?P<quote>['\"]?)(?P<value>(\S+|\d+)?)(?P=quote)")
    matches = list(re.finditer(regex, arg))

    if len(matches) > 0:
        result = dict()
        for match in matches:
            key = match.group('key')
            value = match.group('value')
            result[key] = value.replace("_", " ")
        return result
    else:
        result = []
        nonkeyed_pattern = re.compile(r'[, ]+')
        nonkeyed_args = nonkeyed_pattern.split(arg)

        for text in nonkeyed_args:
            if text:
                text = text[0].replace("'", "").replace('"', '') \
                    + text[1:len(text)-1].replace('_', ' ')\
                    .replace('"', r'\"').replace("'", "\'")\
                    + text[len(text)-1].replace("'", "").replace('"', '')
                result.append(text.replace('_', ' '))
        return tuple(result)


def isValidInt(text: str) -> bool:
    """ Check if string is an integer """
    pattern = re.compile(r"^-?\d+$")
    return bool(pattern.match(text))


def isValidFloat(num: str) -> bool:
    """ Check if string is a float """
    pattern = re.compile(r"^-?\d+(?:\.\d+)?$")
    return bool(pattern.match(num))


def isValidBool(value: str) -> bool:
    """ Check if string is a boolean """
    return value.lower() in ['true', 'false']


if __name__ == '__main__':
    HBNBCommand().cmdloop()
