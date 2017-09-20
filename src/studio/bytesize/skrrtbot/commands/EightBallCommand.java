package studio.bytesize.skrrtbot.commands;

import net.dv8tion.jda.core.events.message.MessageReceivedEvent;
import studio.bytesize.skrrtbot.Command;
import studio.bytesize.skrrtbot.Rand;
import studio.bytesize.skrrtbot.util.CommandHelper;

public class EightBallCommand  implements Command {
    private final String HELP = "USAGE: /8ball <question>\nAsk a question and the magic 8-ball will answer it.";

    private final String[] answers = {
            "It is certain",
            "It is decidedly so",
            "Without a doubt",
            "Yes definitely",
            "You may rely on it",
            "As I see it, yes",
            "Most likely",
            "Outlook good",
            "Yes",
            "Signs point to yes",
            "Reply hazy try again",
            "Ask again later",
            "Better not tell you now",
            "Cannot predict right now",
            "Concentrate and ask again",
            "Don't count on it",
            "My reply is no",
            "My sources say no",
            "Outlook not so good",
            "Very doubtful"
    };

    public boolean called(String[] args, MessageReceivedEvent event) {
        return true;
    }

    public void action(String[] args, MessageReceivedEvent event) {
        if(args.length == 0) {
            CommandHelper.sendTagMessage("You didn't ask me a question...", event);
            return;
        }

        CommandHelper.sendTagMessage(answers[Rand.getRand(0, answers.length-1)], event);
    }

    public String help() {
        return HELP;
    }

    public void executed(boolean success, MessageReceivedEvent event) {
        return;
    }
}
