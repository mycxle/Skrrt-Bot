package studio.bytesize.skrrtbot.commands;

import net.dv8tion.jda.core.events.message.MessageReceivedEvent;
import studio.bytesize.skrrtbot.Command;
import studio.bytesize.skrrtbot.Help;
import studio.bytesize.skrrtbot.util.CommandHelper;

public class HexCommand implements Command {
    public boolean called(String[] args, MessageReceivedEvent event) {
        return true;
    }

    public void action(String[] args, MessageReceivedEvent event) {
        if(args.length == 0) {
            CommandHelper.sendTagMessage("You didn't provide any text...", event);
            return;
        }

        String str = "";
        for(String a : args) {
            str += a + " ";
        }
        str = str.substring(0, str.length() - 1);

        String hxStr = "";
        for(int i = 0; i < str.length(); i++) {
            char c = str.charAt(i);
            hxStr += Integer.toHexString(c) + " ";
        }
        hxStr = hxStr.substring(0, hxStr.length() - 1);

        CommandHelper.sendTagMessage(hxStr, event);
    }

    public String help() {
        return Help.str("hex <text>\nConverts given text to hexadecimal.");
    }

    public void executed(boolean success, MessageReceivedEvent event) {
        return;
    }
}