package studio.bytesize.skrrtbot.commands;

import net.dv8tion.jda.core.events.message.MessageReceivedEvent;
import studio.bytesize.skrrtbot.Command;
import studio.bytesize.skrrtbot.Rand;
import studio.bytesize.skrrtbot.util.CommandHelper;

public class ChooseCommand implements Command {
    private final String HELP = "USAGE: /choose <choice 1> or <choice 2> or <choice 3>\nWill pick from the choices provided. Unlimited amount of choices allowed.";

    public boolean called(String[] args, MessageReceivedEvent event) {
        return true;
    }

    public void action(String[] args, MessageReceivedEvent event) {
        String str = "";



        for(String a : args) {
            str += a + " ";
        }

        str = str.toLowerCase();
        String[] choices = str.split(" or ");

        if(choices.length <= 1) {
            CommandHelper.sendTagMessage("You need to give me 2 or more choices...", event);
            return;
        }

        CommandHelper.sendTagMessage("I choose " + choices[Rand.getRand(0, choices.length-1)], event);
    }

    public String help() {
        return HELP;
    }

    public void executed(boolean success, MessageReceivedEvent event) {
        return;
    }
}
