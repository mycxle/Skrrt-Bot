package studio.bytesize.skrrtbot.commands;

import net.dv8tion.jda.core.events.message.MessageReceivedEvent;
import studio.bytesize.skrrtbot.Command;
import studio.bytesize.skrrtbot.Help;
import studio.bytesize.skrrtbot.Rand;
import studio.bytesize.skrrtbot.util.CommandHelper;

public class RollCommand implements Command {
    public boolean called(String[] args, MessageReceivedEvent event) {
        return true;
    }

    public void action(String[] args, MessageReceivedEvent event) {
        if(args.length == 0) {
            CommandHelper.sendTagMessage("You didn't provide any dice info...", event);
            return;
        }

        String str = "";
        for(String a : args) {
            str += a + " ";
        }
        str = str.toLowerCase();

        String[] choices = str.split(" ");
        int total = 0;

        try {
            if(choices.length == 1) {
                total = Rand.getRand(1, Integer.parseInt(choices[0]));
                CommandHelper.sendTagMessage("You rolled a " + choices[0] + "-sided die. Your roll: " + total, event);
            } else if(choices.length == 2) {
                for(int i = 0; i < Integer.parseInt(choices[0]); i++) {
                    total += Rand.getRand(1, Integer.parseInt(choices[1]));
                }
                CommandHelper.sendTagMessage("You rolled " + choices[0] + " " + choices[1] + "-sided dice. Your roll: " + total, event);
            }
        } catch(Exception e) {
            CommandHelper.sendTagMessage(e.getMessage(), event);
        }
    }

    public String help() {
        return Help.str("roll <n sides> OR <n dice> <n sides>\nRolls dice. Give the number of sides OR the number of dice and the number of sides.");
    }

    public void executed(boolean success, MessageReceivedEvent event) {
        return;
    }
}