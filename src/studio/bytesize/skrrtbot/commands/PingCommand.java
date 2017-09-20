package studio.bytesize.skrrtbot.commands;

import net.dv8tion.jda.core.events.message.MessageReceivedEvent;
import studio.bytesize.skrrtbot.Command;
import studio.bytesize.skrrtbot.util.CommandHelper;

public class PingCommand implements Command {
    private final String HELP = "USAGE: /ping\nWill say 'PONG!'";

    public boolean called(String[] args, MessageReceivedEvent event) {
        return true;
    }

    public void action(String[] args, MessageReceivedEvent event) {
        CommandHelper.sendTagMessage("PONG!", event);
    }

    public String help() {
        return HELP;
    }

    public void executed(boolean success, MessageReceivedEvent event) {
        return;
    }
}