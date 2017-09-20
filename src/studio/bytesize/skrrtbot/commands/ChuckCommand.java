package studio.bytesize.skrrtbot.commands;

import com.google.gson.Gson;
import net.dv8tion.jda.core.events.message.MessageReceivedEvent;
import org.jsoup.Jsoup;
import studio.bytesize.skrrtbot.Command;
import studio.bytesize.skrrtbot.util.CommandHelper;

import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.Reader;
import java.net.URL;
import java.util.Scanner;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class ChuckCommand implements Command {
    private final String HELP = "USAGE: /chucknorris\nWill tell you a Chuck Norris joke";

    public boolean called(String[] args, MessageReceivedEvent event) {
        return true;
    }

    public void action(String[] args, MessageReceivedEvent event) {
        try {
            URL url = new URL("http://api.icndb.com/jokes/random");
            Scanner s = new Scanner(url.openStream());

            String regexString = Pattern.quote("\"joke\": \"") + "(.*?)" + Pattern.quote("\",");
            Pattern pattern = Pattern.compile(regexString);
            // text contains the full text that you want to extract data

            Matcher matcher = pattern.matcher(s.nextLine());

            while (matcher.find()) {
                String textInBetween = matcher.group(1); // Since (.*?) is capturing group 1
                textInBetween = textInBetween.replace("&quot;", "\"");
                textInBetween = textInBetween.replace("&amp;", "&");
                System.out.println(textInBetween);
                CommandHelper.sendTagMessage(textInBetween, event);
            }
        }
        catch(Exception ex) {
            // there was some connection problem, or the file did not exist on the server,
            // or your URL was not in the right format.
            // think about what to do now, and put it here.
            ex.printStackTrace(); // for now, simply output it.
        }
    }

    public String help() {
        return HELP;
    }

    public void executed(boolean success, MessageReceivedEvent event) {
        return;
    }

    public class ChuckObj {
        String joke;
    }
}