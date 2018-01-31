package studio.bytesize.skrrtbot.commands;

import net.dv8tion.jda.core.events.message.MessageReceivedEvent;
import studio.bytesize.skrrtbot.Command;
import studio.bytesize.skrrtbot.Help;
import studio.bytesize.skrrtbot.util.CommandHelper;

public class BinaryCommand implements Command {
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

        byte[] bytes = str.getBytes();
        StringBuilder binary = new StringBuilder();
        for(byte b : bytes) {
            int val = b;
            for(int i = 0; i < 8; i++) {
                binary.append((val & 128) == 0 ? 0 : 1);
                val <<= 1;
            }
            binary.append(' ');
        }

        CommandHelper.sendTagMessage("" + binary, event);
    }

    public String help() {
        return Help.str("binary <text>\nConverts given text to binary.");
    }

    public void executed(boolean success, MessageReceivedEvent event) {
        return;
    }
}