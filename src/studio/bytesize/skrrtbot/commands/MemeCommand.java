package studio.bytesize.skrrtbot.commands;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import net.dv8tion.jda.core.events.message.MessageReceivedEvent;
import studio.bytesize.skrrtbot.Command;
import studio.bytesize.skrrtbot.Help;
import studio.bytesize.skrrtbot.util.CommandHelper;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.net.URLEncoder;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class MemeCommand implements Command {
    private static HashMap<String, Integer> memeNames = new HashMap<>();

    static {
        memeNames.put("boromir", 61579);
        memeNames.put("batman", 438680);
        memeNames.put("aliens", 101470);
        memeNames.put("interesting", 61532);
        memeNames.put("fry", 61520);
        memeNames.put("everywhere", 347390);
        memeNames.put("skeleton", 4087833);
        memeNames.put("leonardo", 5496396);
        memeNames.put("firstworld", 61539);
        memeNames.put("braceyourselves", 61546);
        memeNames.put("brian", 61585);
        memeNames.put("yuno", 61527);
        memeNames.put("wouldbegreat", 563423);
        memeNames.put("wonka", 61582);
        memeNames.put("oprah", 28251713);
        memeNames.put("kermit", 16464531);
        memeNames.put("boardroom", 1035805);
        memeNames.put("doge", 8072285);
        memeNames.put("picardfacepalm", 1509839);
        memeNames.put("successkid", 61544);
        memeNames.put("gotanymoreof", 13424299);
        memeNames.put("grumpycat", 405658);
        memeNames.put("allthethings", 61533);
        memeNames.put("thirdworldskeptic", 101288);
        memeNames.put("morpheus", 100947);
        memeNames.put("blackwat", 14230520);
        memeNames.put("picardwtf", 245898);
        memeNames.put("rockdriving", 21735);
        memeNames.put("philosoraptor", 61516);
        memeNames.put("yoda", 14371066);
        memeNames.put("drevil", 40945639);
        memeNames.put("faceyoumake", 9440985);
        memeNames.put("confessionbear", 100955);
        memeNames.put("disastergirl", 97984);
        memeNames.put("eviltoddler", 235589);
        memeNames.put("findingneverland", 6235864);
        memeNames.put("onlyonearoundhere", 259680);
        memeNames.put("grandma", 61556);
        memeNames.put("toodamnhigh", 61580);
        memeNames.put("10guy", 101440);
        memeNames.put("thirdworldsuccess", 101287);
        memeNames.put("spongebob", 101511);
        memeNames.put("sealion", 13757816);
        memeNames.put("maury", 444501);
        memeNames.put("anditsgone", 766986);
        memeNames.put("laughingmen", 922147);
        memeNames.put("sparta", 195389);
        memeNames.put("notime", 442575);
        memeNames.put("heardyou", 101716);
        memeNames.put("skepticalbaby", 101711);
        memeNames.put("saythatagain", 124212);
        memeNames.put("keanu", 61583);
        memeNames.put("patrick", 61581);
        memeNames.put("badpundog", 12403754);
        memeNames.put("waithere", 109765);
        memeNames.put("sohotrightnow", 21604248);
        memeNames.put("backinmyday", 718432);
        memeNames.put("steveharvey", 143601);
        memeNames.put("belikebill", 56225174);
        memeNames.put("awkwardpenguin", 61584);
        memeNames.put("losestheirminds", 1790995);
        memeNames.put("rickandcarl", 11557802);
        memeNames.put("archer", 10628640);
        memeNames.put("spongegar", 68690826);
        memeNames.put("scumbagsteve", 61522);
        memeNames.put("imagination", 163573);
        memeNames.put("killyourself", 172314);
        memeNames.put("trophy", 3218037);
        memeNames.put("civilwar", 28034788);
        memeNames.put("pepperidgefarm", 1232104);
        memeNames.put("nobodycares", 6531067);
        memeNames.put("buyaboat", 1367068);
        memeNames.put("unclesam", 89655);
        memeNames.put("arthurfist", 74191766);
        memeNames.put("taken", 228024);
        memeNames.put("lookatme", 29617627);
        memeNames.put("buddyjesus", 17699);
        memeNames.put("puffin", 7761261);
        memeNames.put("jackiechanwtf", 412211);
        memeNames.put("spiderman", 1366993);
        memeNames.put("overlyattached", 100952);
        memeNames.put("heygirl", 389834);
        memeNames.put("petergriffin", 356615);
        memeNames.put("takemymoney", 176908);
        memeNames.put("goodfellas", 47235368);
        memeNames.put("gollum", 681831);
        memeNames.put("wolfofwallstreet", 17496002);
        memeNames.put("ermahgerd", 101462);
        memeNames.put("notgoingtohappen", 10364354);
        memeNames.put("hidethepain", 27813981);
        memeNames.put("memberberries", 78381262);
        memeNames.put("suddenclarity", 100948);
        memeNames.put("chapelle", 36061805);
        memeNames.put("cutecat", 8279814);
        memeNames.put("obiwan", 409403);
        memeNames.put("peterparker", 107773);
        memeNames.put("suprisedkoala", 27920);
        memeNames.put("mvp", 15878567);
        memeNames.put("kevinhart", 265789);
        memeNames.put("gandalf", 673439);
    }

    public boolean called(String[] args, MessageReceivedEvent event) {
        return true;
    }

    public void action(String[] args, MessageReceivedEvent event) {
        if(args.length <= 1) {
            CommandHelper.sendTagMessage("Please provide the name of the meme, \"top text\" and \"bottom text\"...", event);
            return;
        }

        try {
            BufferedReader br = new BufferedReader(new FileReader("imgflip.txt"));
            try {
                String username = br.readLine();
                String password = br.readLine();
                int template;

                try {
                    template = memeNames.get(args[0].toLowerCase());
                } catch(Exception e) {
                    CommandHelper.sendTagMessage("That is not a valid meme. Check the list: \"/help meme\"...", event);
                    return;
                }

                String str = "";
                boolean dun = false;
                for(String s : args) {
                    if(dun) str += s + " ";
                    if(!dun) dun = true;
                }

                String regexString = Pattern.quote("\"") + "(.*?)" + Pattern.quote("\"");
                Pattern pattern = Pattern.compile(regexString);
                Matcher matcher = pattern.matcher(str);
                ArrayList<String> text = new ArrayList<>();

                while(matcher.find()) {
                    String textInBetween = matcher.group(1);
                    text.add(textInBetween);
                }

                if(text.size() == 1 && text.get(0).length() == 0) {
                    CommandHelper.sendTagMessage("You didn't provide any text..", event);
                    return;
                } else if(text.size() == 2 && text.get(0).length() == 0 && text.get(1).length() == 0) {
                    CommandHelper.sendTagMessage("You didn't provide any text..", event);
                    return;
                }

                String u = "https://api.imgflip.com/caption_image?username=" + username + "&password=" +
                        password + "&template_id=" + template + "&text0=" + URLEncoder.encode(text.get(0), "UTF-8");
                if(text.size() > 1) u += "&text1=" + URLEncoder.encode(text.get(1), "UTF-8");

                URL url = new URL(u);
                HttpURLConnection httpcon = (HttpURLConnection) url.openConnection();
                httpcon.addRequestProperty("User-Agent", "Mozilla/4.0");

                InputStream stream = httpcon.getInputStream();
                BufferedReader reader = new BufferedReader(new InputStreamReader(stream));
                StringBuilder out = new StringBuilder();
                String line;
                while((line = reader.readLine()) != null) {
                    out.append(line);
                }
                reader.close();

                String ss = out.toString();
                ObjectMapper mapper = new ObjectMapper();
                JsonNode rootNode = mapper.readTree(ss);
                JsonNode dataNode = rootNode.path("data").path("url");
                CommandHelper.sendTagMessage(dataNode.asText(), event);
            } finally {
                br.close();
            }
        } catch(Exception e) {
            CommandHelper.sendTagMessage(e.getMessage(), event);
        }
    }

    public String help() {
        String memeList = "";
        for(String s : memeNames.keySet()) {
            memeList += s + ", ";
        }
        return Help.str("meme <name of meme> \"top text\" \"bottom text\"\nWill generate you your very own meme! Text must be inside quotes.\nMEME NAMES: " + memeList.substring(0, memeList.length() - 2));
    }

    public void executed(boolean success, MessageReceivedEvent event) {
        return;
    }
}