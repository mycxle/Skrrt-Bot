package studio.bytesize.skrrtbot.commands;

import net.dv8tion.jda.core.events.message.MessageReceivedEvent;
import studio.bytesize.skrrtbot.Command;
import studio.bytesize.skrrtbot.util.CommandHelper;

public class OctalCommand implements Command {
    private final String HELP = "USAGE: /octal message to convert to octal";

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
        System.out.println(str);

        String octStr = "";

        for (int i = 0; i < str.length(); i++){
            char c = str.charAt(i);
            String tmp = Integer.toOctalString(c);
            if(tmp.length() == 2) {
                tmp = "0" +tmp;
            }
            octStr += tmp + " ";
        }

        octStr = octStr.substring(0, octStr.length() - 1);

        CommandHelper.sendTagMessage(octStr, event);
    }

    public String help() {
        return HELP;
    }

    public void executed(boolean success, MessageReceivedEvent event) {
        return;
    }
}