import hexchat

__module_name__ = "ICU"
__module_version__ = "0.1"
__module_description__ = "Relay messages from and to any channels you are in - even across servers."
__module_help_message__ = "/ICU <(add|del) (to|from) #channel> Relay messages between channels."

contexts = { "from": [], "to": [] }

def on_message(word, word_eol, userdata):
    contexts = userdata
    context = hexchat.get_context()
    this_word = word[1]

    for from_context in contexts['from']:
        if context.get_info("channel") == from_context.get_info("channel"):
            for to_context in contexts['to']:
                to_context.command("say <{}> {}".format(word[0], word[1]))

    return hexchat.EAT_NONE

def icu(word, word_eol, userdata):
    if len(word) < 4:
        hexchat.prnt(__module_help_message__)
        return hexchat.EAT_ALL
    
    contexts = userdata
    this_context = hexchat.get_context()
    operation = word[1]
    direction = word[2]
    destination = word[3]
    
    potential_context = hexchat.find_context(channel=destination)
    if potential_context == None:
        hexchat.prnt("Could not find {}.".format(destination))
        return hexchat.EAT_ALL

    if operation == "add":
        if direction == "to":
            contexts["to"].append(potential_context)
        elif direction == "from":
            contexts["from"].append(potential_context)
        this_context.prnt("Added relay {} {}".format(direction, destination))

    if operation == "del":
        if direction == "to":
            contexts["to"].remove(potential_context)
        elif direction == "from":
            contexts["from"].remove(potential_context)
        this_context.prnt("Deleted relay {} {}".format(direction, destination))

    return hexchat.EAT_ALL


hexchat.hook_command("ICU", icu, contexts, help=__module_help_message__)
hexchat.hook_print("Channel Message", on_message, contexts)
hexchat.hook_print("Channel Msg Hilight", on_message, contexts)
hexchat.hook_print("Your Message", on_message, contexts)
