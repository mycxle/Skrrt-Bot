package studio.bytesize.skrrtbot.commands;

import net.dv8tion.jda.core.events.message.MessageReceivedEvent;
import studio.bytesize.skrrtbot.util.Help;
import studio.bytesize.skrrtbot.util.CommandHelper;

import java.net.URL;
import java.util.Scanner;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class ChuckCommand implements Command {
    public boolean called(String[] args, MessageReceivedEvent event) {
        return true;
    }

    public void action(String[] args, MessageReceivedEvent event) {
        try {
            URL url = new URL("http://api.icndb.com/jokes/random");
            Scanner s = new Scanner(url.openStream());

            String regexString = Pattern.quote("\"joke\": \"") + "(.*?)" + Pattern.quote("\",");
            Pattern pattern = Pattern.compile(regexString);

            Matcher matcher = pattern.matcher(s.nextLine());

            while(matcher.find()) {
                String textInBetween = matcher.group(1);
                textInBetween = textInBetween.replace("&quot;", "\"");
                textInBetween = textInBetween.replace("&amp;", "&");
                CommandHelper.sendTagMessage(textInBetween, event);
            }
        } catch(Exception e) {
            CommandHelper.sendTagMessage(e.getMessage(), event);
        }
    }

    public String help() {
        return Help.str("chucknorris\nWill tell you a Chuck Norris joke.");
    }

    public void executed(boolean success, MessageReceivedEvent event) {
        return;
    }
}