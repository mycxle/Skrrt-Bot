package studio.bytesize.skrrtbot.commands;

import net.dv8tion.jda.core.events.message.MessageReceivedEvent;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import studio.bytesize.skrrtbot.Command;
import studio.bytesize.skrrtbot.Help;
import studio.bytesize.skrrtbot.Rand;
import studio.bytesize.skrrtbot.util.CommandHelper;

import java.io.InputStream;
import java.net.URL;
import java.net.URLConnection;

public class ComicCommand implements Command {
    private String cah = "http://explosm.net/comics/random/";
    private String xkcd = "https://c.xkcd.com/random/comic/";
    private String smbc = "http://www.smbc-comics.com/random.php";
    private String oatmeal = "http://theoatmeal.com/feed/random";

    public boolean called(String[] args, MessageReceivedEvent event) {
        return true;
    }

    public void action(String[] args, MessageReceivedEvent event) {
        String str;
        if(args.length == 0) {
            str = "random";
        } else {
            str = args[0];
        }

        if(str.equals("random")) {
            int i = Rand.getRand(0, 3);
            switch(i) {
                case 0:
                    str = "cah";
                    break;
                case 1:
                    str = "xkcd";
                    break;
                case 2:
                    str = "smbc";
                    break;
                case 3:
                    str = "oatmeal";
                    break;
                default:
                    break;
            }
        }

        try {
            Document doc;
            String src;

            if(str.equals("cah")) {
                doc = Jsoup.connect(cah).get();
                src = "http:" + doc.select("#main-comic").attr("src");
            } else if(str.equals("xkcd")) {
                doc = Jsoup.connect(xkcd).get();
                src = "http:" + doc.select("#comic").select("img").first().attr("src");
            } else if(str.equals("smbc")) {
                URLConnection con = new URL(smbc).openConnection();
                con.connect();

                InputStream is = con.getInputStream();
                is.close();

                doc = Jsoup.connect(con.getURL().toString()).get();
                src = "https://www.smbc-comics.com" + doc.select("#cc-comic").attr("src");
            } else if(str.equals("oatmeal")) {
                doc = Jsoup.connect(oatmeal).get();
                src = doc.select("#comic").select("img").first().attr("src");
            } else {
                CommandHelper.sendTagMessage("That's not a valid comic name...", event);
                return;
            }
            CommandHelper.sendTagMessage(src, event);
        } catch(Exception e) {
            CommandHelper.sendTagMessage(e.getMessage(), event);
        }
    }

    public String help() {
        return Help.str("comic <name>\nWill post a random comic from the strip indicated." +
                "\nCOMIC NAMES:\ncah - Cyanide & Happiness\nxkcd - XKCD\nsmbc - Saturday Morning Breakfast Cereal" +
                "\noatmeal - The Oatmeal\nrandom - chooses randomly from above list");
    }

    public void executed(boolean success, MessageReceivedEvent event) {
        return;
    }
}