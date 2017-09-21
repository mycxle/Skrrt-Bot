package studio.bytesize.skrrtbot.commands;

import net.dv8tion.jda.core.events.message.MessageReceivedEvent;
import studio.bytesize.skrrtbot.Command;
import studio.bytesize.skrrtbot.util.CommandHelper;

import java.util.HashMap;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

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
        str = str.toUpperCase();

//        for(String s : leet.keySet()) {
//            str = str.replace(s, leet.get(s));
//        }

        CommandHelper.sendTagMessage(toLeetCode(str), event);
    }

    public String help() {
        return HELP;
    }

    public void executed(boolean success, MessageReceivedEvent event) {
        return;
    }

    private String toLeetCode(String str) {
        Pattern pattern = Pattern.compile("[^a-zA-Z]");
        StringBuilder result = new StringBuilder();
        HashMap<Character, String> map = new HashMap<Character, String>();
        map.put('A', "@");
        map.put('B', "ß");
        map.put('C', "©");
        map.put('D', "đ");
        map.put('E', "€");
        map.put('F', "ƒ");
        map.put('G', "6");
        map.put('H', "#");
        map.put('I', "!");
        map.put('J', "¿");
        map.put('K', "X");
        map.put('L', "£");
        map.put('M', "M");
        map.put('N', "r");
        map.put('O', "0");
        map.put('P', "p");
        map.put('Q', "0");
        map.put('R', "®");
        map.put('S', "$");
        map.put('T', "7");
        map.put('U', "µ");
        map.put('V', "v");
        map.put('W', "w");
        map.put('X', "%");
        map.put('Y', "¥");
        map.put('Z', "z");

        for (int i = 0; i < str.length(); i++) {
            char key = Character.toUpperCase(str.charAt(i));
            Matcher matcher = pattern.matcher(Character.toString(key));
            if (matcher.find()) {
                result.append(key);
                result.append(' ');
            } else {
                result.append(map.get(key));
                result.append(' ');
            }
        }
        return result.toString();
        //String[] retval=str.split(" ");
    }
}