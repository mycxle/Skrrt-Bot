package studio.bytesize.skrrtbot.commands;

import net.dv8tion.jda.core.events.message.MessageReceivedEvent;
import studio.bytesize.skrrtbot.Command;
import studio.bytesize.skrrtbot.Rand;
import studio.bytesize.skrrtbot.util.CommandHelper;

public class CoinCommand implements Command {
    private final String HELP = "USAGE: /coin\nFlips a coin.";

    public boolean called(String[] args, MessageReceivedEvent event) {
        return true;
    }

    public void action(String[] args, MessageReceivedEvent event) {
        CommandHelper.sendTagMessage("The coin landed on " + (Rand.getRand(0, 1) == 1 ? "heads" : "tails"), event);
    }

    public String help() {
        return HELP;
    }

    public void executed(boolean success, MessageReceivedEvent event) {
        return;
    }
}
