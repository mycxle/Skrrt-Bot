package studio.bytesize.skrrtbot.commands;

import net.dv8tion.jda.core.events.message.MessageReceivedEvent;
import studio.bytesize.skrrtbot.Command;
import studio.bytesize.skrrtbot.Help;
import studio.bytesize.skrrtbot.Rand;
import studio.bytesize.skrrtbot.util.CommandHelper;

public class ChooseCommand implements Command {
    public boolean called(String[] args, MessageReceivedEvent event) {
        return true;
    }

    public void action(String[] args, MessageReceivedEvent event) {
        String str = "";
        for(String a : args) {
            str += a + " ";
        }
        String[] choices = str.split(" or ");

        if(choices.length <= 1) {
            CommandHelper.sendTagMessage("You need to give me 2 or more choices...", event);
            return;
        }

        CommandHelper.sendTagMessage("I choose " + choices[Rand.getRand(0, choices.length - 1)], event);
    }

    public String help() {
        return Help.str("choose <choice1> or <choice2> or <choice3>\nWill pick from the provided choices. Unlimited amount of choices allowed.");
    }

    public void executed(boolean success, MessageReceivedEvent event) {
        return;
    }
}