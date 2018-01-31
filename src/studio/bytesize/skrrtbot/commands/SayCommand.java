package studio.bytesize.skrrtbot.commands;

import net.dv8tion.jda.core.events.message.MessageReceivedEvent;
import studio.bytesize.skrrtbot.util.Help;
import studio.bytesize.skrrtbot.util.CommandHelper;

public class SayCommand implements Command {
    public boolean called(String[] args, MessageReceivedEvent event) {
        return true;
    }

    public void action(String[] args, MessageReceivedEvent event) {
        String str = "";

        if(args.length == 0) {
            CommandHelper.sendTagMessage("You didn't tell me what to say...", event);
            return;
        }

        for(String a : args) {
            str += a + " ";
        }

        CommandHelper.sendMessage(str.substring(0, str.length() - 1), event);
    }

    public String help() {
        return Help.str("say <text>\nWill repeat whatever text is provided.");
    }

    public void executed(boolean success, MessageReceivedEvent event) {
        return;
    }
}