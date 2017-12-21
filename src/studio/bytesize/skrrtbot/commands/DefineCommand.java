package studio.bytesize.skrrtbot.commands;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import net.dv8tion.jda.core.events.message.MessageReceivedEvent;
import studio.bytesize.skrrtbot.Command;
import studio.bytesize.skrrtbot.util.CommandHelper;

import java.io.BufferedReader;
import java.io.FileReader;
import java.net.URL;
import java.net.URLEncoder;
import java.util.*;

public class DefineCommand implements Command {
    private final String HELP = "USAGE: /define <text>\nWill provide definition of given word or phrase";

    private static final HashMap<String, String> hshmp = new HashMap<>();
    static {
        try {
            BufferedReader br = new BufferedReader(new FileReader("definitions.txt"));

            System.out.println("DefineCommand.java");

            String line = br.readLine();
            while (line != null)
            {
                String key = line;
                line = br.readLine();

                System.out.println("KEY: " + key + ", VAL: " + line + "\n\n");

                hshmp.put(key, line);
                line = br.readLine();
            }

            for (Map.Entry<String, String> entry : hshmp.entrySet()) {
                String key = entry.getKey();
                Object value = entry.getValue();
                System.out.println(key + " | " + value + "\n");
            }

        } catch(Exception e) {

        }
    }

    public boolean called(String[] args, MessageReceivedEvent event) {
        return true;
    }

    public void action(String[] args, MessageReceivedEvent event) {
        if(args.length == 0) {
            CommandHelper.sendTagMessage("You didn't tell me what to define...", event);
            return;
        }

        String str = "";
        for(String a : args) {
            str += a + " ";
        }

        for (Map.Entry<String, String> entry : hshmp.entrySet()) {
            String key = entry.getKey();
            String value = entry.getValue();
            if(str.toLowerCase().contains(key)) {
                CommandHelper.sendTagMessage(value, event);
                return;
            }
        }

        try {
            URL url = new URL("http://api.urbandictionary.com/v0/define?term=" + URLEncoder.encode(str, "UTF-8"));
            Scanner s = new Scanner(url.openStream());

            ObjectMapper mapper = new ObjectMapper();

            String ss = s.nextLine();

            System.out.println(ss);

            JsonNode rootNode = mapper.readTree(ss);

            JsonNode listNode = rootNode.path("list");
            if(listNode.has(0)) {
                int i = 0;

                ArrayList<Integer> upvotes = new ArrayList<>();

                while(listNode.has(i)) {
                    upvotes.add(listNode.path(i).path("thumbs_up").asInt());
                    i++;
                }

                int max = Collections.max(upvotes);

                listNode = listNode.path(upvotes.indexOf(max)).path("definition");
                CommandHelper.sendTagMessage(listNode.asText(), event);
                System.out.println(listNode.asText());
            } else {
                System.out.println(str.toLowerCase());
                CommandHelper.sendTagMessage("I don't know the definition for that.", event);
            }



        } catch (Exception e) {
            CommandHelper.sendTagMessage(e.getMessage(),event);
        }

    }

    public String help() {
        return HELP;
    }

    public void executed(boolean success, MessageReceivedEvent event) {
        return;
    }
}