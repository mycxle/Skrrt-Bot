package studio.bytesize.skrrtbot.commands;

import net.dv8tion.jda.core.events.message.MessageReceivedEvent;
import studio.bytesize.skrrtbot.util.Help;
import studio.bytesize.skrrtbot.util.CommandHelper;

public class OctalCommand implements Command {
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

        String octStr = "";
        for(int i = 0; i < str.length(); i++) {
            char c = str.charAt(i);
            String tmp = Integer.toOctalString(c);
            if(tmp.length() == 2) {
                tmp = "0" + tmp;
            }
            octStr += tmp + " ";
        }
        octStr = octStr.substring(0, octStr.length() - 1);

        CommandHelper.sendTagMessage(octStr, event);
    }

    public String help() {
        return Help.str("octal <text>\nConverts given text to octal.");
    }

    public void executed(boolean success, MessageReceivedEvent event) {
        return;
    }
}