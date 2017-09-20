package studio.bytesize.skrrtbot.commands;

import net.dv8tion.jda.core.events.message.MessageReceivedEvent;
import studio.bytesize.skrrtbot.Command;
import studio.bytesize.skrrtbot.util.CommandHelper;

import java.util.HashMap;

public class LeetCommand implements Command {
    private final String HELP = "USAGE: /leet <text>\nWill convert text to leetspeak";

    private static final HashMap<String, String> leet = new HashMap<String, String>();
    static {
        leet.put("a", "@");
        leet.put("b", "8");
        leet.put("c", "(");
        leet.put("d", "|)");
        leet.put("e", "3");
        leet.put("f", "|=");
        leet.put("g", "6");
        leet.put("h", "4");
        leet.put("i", "1");
        leet.put("j", "_|");
        leet.put("k", "|<");
        leet.put("l", "1");
        leet.put("m", "|\\\\/|");
        leet.put("n", "|\\\\|");
        leet.put("o", "0");
        leet.put("p", "¶");
        leet.put("q", "9");
        leet.put("r", "Я");
        leet.put("s", "$");
        leet.put("t", "7");
        leet.put("u", "|_|");
        leet.put("v", "\\\\/");
        leet.put("w", "\\\\/\\\\/");
        leet.put("x", "><");
        leet.put("y", "`/");
        leet.put("z", "2");
    }

    public boolean called(String[] args, MessageReceivedEvent event) {
        return true;
    }

    public void action(String[] args, MessageReceivedEvent event) {
        if(args.length == 0) {
            CommandHelper.sendTagMessage("You didn't provide any text...", event);
            return;
        }

        String str = "";
        for(String a : args) {
            str += a + " ";
        }
        str = str.toLowerCase();

        for(String s : leet.keySet()) {
            str = str.replace(s, leet.get(s));
        }

        CommandHelper.sendTagMessage(str, event);
    }

    public String help() {
        return HELP;
    }

    public void executed(boolean success, MessageReceivedEvent event) {
        return;
    }
}