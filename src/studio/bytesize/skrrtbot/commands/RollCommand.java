package studio.bytesize.skrrtbot.commands;

import net.dv8tion.jda.core.events.message.MessageReceivedEvent;
import studio.bytesize.skrrtbot.Command;
import studio.bytesize.skrrtbot.Rand;
import studio.bytesize.skrrtbot.util.CommandHelper;

public class RollCommand implements Command {
    private final String HELP = "USAGE: /roll [n sides] OR [n dice] [n sides]";

    public boolean called(String[] args, MessageReceivedEvent event) {
        return true;
    }

    public void action(String[] args, MessageReceivedEvent event) {
        if(args.length == 0) {
            CommandHelper.sendTagMessage("Do '/help roll' because you obviously don't know what you're doing...", event);
            return;
        }
        String str = "";

        for(String a : args) {
            str += a + " ";
        }
        int total = 0;
        str = str.toLowerCase();
        String[] choices = str.split(" ");

        try {
            if (choices.length == 1) {
                total = Rand.getRand(1, Integer.parseInt(choices[0]));
                CommandHelper.sendTagMessage("You rolled a " + choices[0] + "-sided die. Your roll: " + total, event);
            } else if (choices.length == 2) {
                for (int i = 0; i < Integer.parseInt(choices[0]); i++) {
                    total += Rand.getRand(1, Integer.parseInt(choices[1]));
                }
                CommandHelper.sendTagMessage("You rolled " + choices[0] + " " + choices[1] + "-sided dice. Your roll: " + total, event);
            }
        } catch (Exception e) {
            CommandHelper.sendTagMessage("Do '/help roll' because you obviously don't know what you're doing...", event);
        }
    }

    public String help() {
        return HELP;
    }

    public void executed(boolean success, MessageReceivedEvent event) {
        return;
    }
}