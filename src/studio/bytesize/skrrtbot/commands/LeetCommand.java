package studio.bytesize.skrrtbot.commands;

import net.dv8tion.jda.core.events.message.MessageReceivedEvent;
import studio.bytesize.skrrtbot.Command;
import studio.bytesize.skrrtbot.Help;
import studio.bytesize.skrrtbot.util.CommandHelper;

import java.util.HashMap;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class LeetCommand implements Command {
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

        CommandHelper.sendTagMessage(toLeetCode(str), event);
    }

    public String help() {
        return Help.str("leet <text>\nConverts given text to leetspeak.");
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

        for(int i = 0; i < str.length(); i++) {
            char key = Character.toUpperCase(str.charAt(i));
            Matcher matcher = pattern.matcher(Character.toString(key));
            if(matcher.find()) {
                result.append(key);
                result.append(' ');
            } else {
                result.append(map.get(key));
                result.append(' ');
            }
        }
        return result.toString();
    }
}