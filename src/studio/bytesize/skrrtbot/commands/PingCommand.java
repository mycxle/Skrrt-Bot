package studio.bytesize.skrrtbot.commands;

import net.dv8tion.jda.core.events.message.MessageReceivedEvent;
import studio.bytesize.skrrtbot.util.Help;
import studio.bytesize.skrrtbot.util.CommandHelper;

public class PingCommand implements Command {
    public boolean called(String[] args, MessageReceivedEvent event) {
        return true;
    }

    public void action(String[] args, MessageReceivedEvent event) {
        CommandHelper.sendTagMessage("PONG!", event);
    }

    public String help() {
        return Help.str("ping\nWill say 'PONG!'");
    }

    public void executed(boolean success, MessageReceivedEvent event) {
        return;
    }
}