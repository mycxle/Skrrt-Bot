package studio.bytesize.skrrtbot.commands;

import net.dv8tion.jda.core.events.message.MessageReceivedEvent;
import studio.bytesize.skrrtbot.Command;
import studio.bytesize.skrrtbot.Help;
import studio.bytesize.skrrtbot.Main;
import studio.bytesize.skrrtbot.util.CommandHelper;

public class HelpCommand implements Command {
    public boolean called(String[] args, MessageReceivedEvent event) {
        return true;
    }

    public void action(String[] args, MessageReceivedEvent event) {
        if(args.length == 0) {
            String str = "";
            for(String s : Main.commands.keySet()) {
                str += (s + ", ");
            }
            str = str.substring(0, str.length() - 2);

            CommandHelper.sendTagMessage("Commands: " + str, event);
            return;
        } else {
            String commandName = args[0];

            if(Main.commands.containsKey(commandName)) {
                CommandHelper.sendTagMessage(Main.commands.get(commandName).help(), event);
            } else {
                CommandHelper.sendTagMessage("There is no command called \"" + commandName + "\"...", event);
            }
        }
    }

    public String help() {
        return Help.str("help <command>\nGives help on given command. If no command is given, lists all commands.");
    }

    public void executed(boolean success, MessageReceivedEvent event) {
        return;
    }
}