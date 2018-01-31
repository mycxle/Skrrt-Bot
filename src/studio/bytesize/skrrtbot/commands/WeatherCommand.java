package studio.bytesize.skrrtbot.commands;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import net.dv8tion.jda.core.events.message.MessageReceivedEvent;
import studio.bytesize.skrrtbot.util.Help;
import studio.bytesize.skrrtbot.util.CommandHelper;

import java.io.BufferedReader;
import java.io.FileReader;
import java.net.URL;
import java.net.URLEncoder;
import java.util.Scanner;

public class WeatherCommand implements Command {
    public boolean called(String[] args, MessageReceivedEvent event) {
        return true;
    }

    public void action(String[] args, MessageReceivedEvent event) {
        if(args.length == 0) {
            CommandHelper.sendTagMessage("You didn't provide a location...", event);
            return;
        }

        String str = "";
        for(String s : args) {
            str += s;
        }

        try {
            BufferedReader br = new BufferedReader(new FileReader("openweathermap.txt"));
            try {
                StringBuilder sb = new StringBuilder();
                String line = br.readLine();

                while(line != null) {
                    sb.append(line);
                    sb.append(System.lineSeparator());
                    line = br.readLine();
                }

                String APIKEY = sb.toString();
                APIKEY = APIKEY.substring(0, APIKEY.length() - 2);

                String surl = "http://api.openweathermap.org/data/2.5/weather?APPID=" + APIKEY + "&units=imperial&q=" + URLEncoder.encode(str, "UTF-8");
                if(str.contains("maine")) {
                    surl = "http://api.openweathermap.org/data/2.5/weather?APPID=" + APIKEY + "&units=imperial&q=" + URLEncoder.encode("maine, us", "UTF-8");
                }

                URL url = new URL(surl);
                Scanner s = new Scanner(url.openStream());
                ObjectMapper mapper = new ObjectMapper();
                String ss = s.nextLine();

                JsonNode rootNode = mapper.readTree(ss);
                JsonNode weatherNode = rootNode.path("weather").path(0).path("description");
                JsonNode country = rootNode.path("sys").path("country");
                JsonNode city = rootNode.path("name");
                JsonNode temp = rootNode.path("main").path("temp");

                String msg = "Right now " + city.asText() + ", " + country.asText() + " is " + temp.asText() + "°F and has " + weatherNode.asText() + ".";

                CommandHelper.sendTagMessage(msg, event);
            } finally {
                br.close();
            }
        } catch(Exception e) {
            CommandHelper.sendTagMessage("Please enter an actual location...", event);
        }
    }

    public String help() {
        return Help.str("weather <location>\nWill give you weather information for given location.");
    }

    public void executed(boolean success, MessageReceivedEvent event) {
        return;
    }
}