package studio.bytesize.skrrtbot.commands;

import net.dv8tion.jda.core.events.message.MessageReceivedEvent;
import studio.bytesize.skrrtbot.util.Help;
import studio.bytesize.skrrtbot.util.Rand;
import studio.bytesize.skrrtbot.util.CommandHelper;

public class CoinCommand implements Command {
    public boolean called(String[] args, MessageReceivedEvent event) {
        return true;
    }

    public void action(String[] args, MessageReceivedEvent event) {
        CommandHelper.sendTagMessage("The coin landed on " + (Rand.getRand(0, 1) == 1 ? "heads" : "tails"), event);
    }

    public String help() {
        return Help.str("coin\nFlips a coin.");
    }

    public void executed(boolean success, MessageReceivedEvent event) {
        return;
    }
}
