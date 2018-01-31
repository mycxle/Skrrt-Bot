package studio.bytesize.skrrtbot.commands;

import net.dv8tion.jda.core.events.message.MessageReceivedEvent;
import studio.bytesize.skrrtbot.util.Help;
import studio.bytesize.skrrtbot.util.Rand;
import studio.bytesize.skrrtbot.util.CommandHelper;

public class RockPaperScissorsCommand implements Command {
    public boolean called(String[] args, MessageReceivedEvent event) {
        return true;
    }

    public void action(String[] args, MessageReceivedEvent event) {
        if(args.length == 0) {
            CommandHelper.sendTagMessage("You didn't make a choice...", event);
            return;
        }

        String choice = args[0];
        if(!choice.equals("rock") && !choice.equals("paper") && !choice.equals("scissor") && !choice.equals("scissors")) {
            CommandHelper.sendTagMessage("You made an invalid choice. Please choose only rock, paper, or scissors...", event);
            return;
        }

        if(choice.equals("scissor")) {
            choice = "scissors";
        }

        String first = "", second;
        int i = Rand.getRand(0, 2);
        if(i == 0) {
            first = "rock";
        } else if(i == 1) {
            first = "paper";
        } else if(i == 2) {
            first = "scissors";
        }
        second = choice;

        String msg = "You chose " + second + ". I chose " + first + ". ";

        if(first.equals(second)) {
            msg += "It's a tie!";
        } else if(first.equals("scissors")) {
            if(second.equals("paper")) msg += "Scissors wins! ✌";
            else msg += "Rock wins! ✊";
        } else if(first.equals("rock")) {
            if(second.equals("scissors")) msg += "Rock wins! ✊";
            else msg += "Paper wins! ✋";
        } else if(first.equals("paper")) {
            if(second.equals("rock")) msg += "Paper wins! ✋";
            else msg += "Scissors wins! ✌";
        }

        CommandHelper.sendTagMessage(msg, event);
    }

    public String help() {
        return Help.str("rockpaperscissors <choice>\nPlay the classic game 'Rock Paper Scissors'.");
    }

    public void executed(boolean success, MessageReceivedEvent event) {
        return;
    }
}