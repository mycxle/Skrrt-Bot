package studio.bytesize.skrrtbot.commands;

import net.dv8tion.jda.core.events.message.MessageReceivedEvent;
import studio.bytesize.skrrtbot.Command;

public class SayCommand implements Command {
    private final String HELP = "USAGE: ~!say";

    public boolean called(String[] args, MessageReceivedEvent event) {
        return true;
    }

    public void action(String[] args, MessageReceivedEvent event) {
        String str = "";

        for(String a : args) {
            str += a + " ";
        }

        event.getTextChannel().sendMessage(str.substring(0, str.length() - 1)).complete();
    }

    public String help() {
        return HELP;
    }

    public void executed(boolean success, MessageReceivedEvent event) {
        return;
    }
}
