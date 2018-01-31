package studio.bytesize.skrrtbot.commands;

import net.dv8tion.jda.core.events.message.MessageReceivedEvent;
import studio.bytesize.skrrtbot.util.Help;
import studio.bytesize.skrrtbot.util.CommandHelper;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.URL;
import java.net.URLConnection;
import java.net.URLEncoder;
import java.nio.charset.Charset;
import java.util.HashMap;

public class TranslateCommand implements Command {
    private static HashMap<String, String> languages = new HashMap<>();

    static {
        languages.put("afrikaans", "af");
        languages.put("albanian", "sq");
        languages.put("amharic", "am");
        languages.put("arabic", "ar");
        languages.put("armenian", "hy");
        languages.put("azeerbaijani", "az");

        languages.put("basque", "eu");
        languages.put("belarusian", "be");
        languages.put("bengali", "bn");
        languages.put("bosnian", "bs");
        languages.put("bulgarian", "bg");

        languages.put("catalan", "ca");
        languages.put("cebuano", "ceb");
        languages.put("chinese", "zh-CN");
        languages.put("corsican", "co");
        languages.put("croatian", "hr");
        languages.put("czech", "cs");

        languages.put("danish", "da");
        languages.put("dutch", "nl");

        languages.put("english", "en");
        languages.put("esperanto", "eo");
        languages.put("estonian", "et");

        languages.put("finnish", "fi");
        languages.put("french", "fr");
        languages.put("frisian", "fy");

        languages.put("galician", "gl");
        languages.put("georgian", "ka");
        languages.put("german", "de");
        languages.put("greek", "el");
        languages.put("gujarati", "gu");

        languages.put("creole", "ht");
        languages.put("hausa", "ha");
        languages.put("hawaiian", "haw");
        languages.put("hebrew", "iw");
        languages.put("hindi", "hi");
        languages.put("hmong", "hmn");
        languages.put("hungarian", "hu");

        languages.put("icelandic", "is");
        languages.put("igbo", "ig");
        languages.put("indonesian", "id");
        languages.put("irish", "ga");
        languages.put("italian", "it");

        languages.put("japanese", "ja");
        languages.put("javanese", "jw");

        languages.put("kannada", "kn");
        languages.put("kazakh", "kk");
        languages.put("khmer", "km");
        languages.put("korean", "ko");
        languages.put("kurdish", "ku");
        languages.put("kyrgyz", "ky");

        languages.put("lao", "lo");
        languages.put("latin", "la");
        languages.put("latvian", "lv");
        languages.put("lithuanian", "lt");
        languages.put("luxembourgish", "lb");

        languages.put("macedonian", "mk");
        languages.put("malagasy", "mg");
        languages.put("malay", "ms");
        languages.put("malayalam", "ml");
        languages.put("maltese", "mt");
        languages.put("maori", "mi");
        languages.put("marathi", "mr");
        languages.put("mongolian", "mn");
        languages.put("myanmar", "my");

        languages.put("nepali", "ne");
        languages.put("norwegian", "no");
        languages.put("nyanja", "ny");

        languages.put("pashto", "ps");
        languages.put("persian", "fa");
        languages.put("polish", "pl");
        languages.put("portuguese", "pt");
        languages.put("punjabi", "pa");

        languages.put("romanian", "ro");
        languages.put("russian", "ru");

        languages.put("samoan", "sm");
        languages.put("gaelic", "gd");
        languages.put("serbian", "sr");
        languages.put("sesotho", "st");
        languages.put("shona", "sn");
        languages.put("sindhi", "sd");
        languages.put("sinhala", "si");
        languages.put("slovak", "sk");
        languages.put("slovenian", "sl");
        languages.put("somali", "so");
        languages.put("spanish", "es");
        languages.put("sundanese", "su");
        languages.put("swahili", "sw");
        languages.put("swedish", "sv");

        languages.put("tagalog", "tl");
        languages.put("tajik", "tg");
        languages.put("tamil", "ta");
        languages.put("telugu", "te");
        languages.put("thai", "th");
        languages.put("turkish", "tr");

        languages.put("ukrainian", "uk");
        languages.put("urdu", "ur");
        languages.put("uzbek", "uz");

        languages.put("vietnamese", "vi");

        languages.put("welsh", "cy");

        languages.put("xhosa", "xh");

        languages.put("yiddish", "yi");
        languages.put("yoruba", "yo");

        languages.put("zulu", "zu");
    }

    public boolean called(String[] args, MessageReceivedEvent event) {
        return true;
    }

    public void action(String[] args, MessageReceivedEvent event) {
        if(args.length < 2) {
            CommandHelper.sendTagMessage("Please provide the target language and some text to translate...", event);
            return;
        }
        try {
            String str = "";
            for(String a : args) {
                str += a + " ";
            }
            str = str.toLowerCase();

            String[] choices = str.split(" ");

            String query = "";
            for(int i = 1; i < choices.length; i++) {
                query += choices[i] + " ";
            }
            query = query.substring(0, query.length() - 1);

            String tl = choices[0];
            for(String key : languages.keySet()) {
                if(tl.contains(key)) {
                    tl = languages.get(key);
                    break;
                }
            }

            URL url = new URL("http://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl=" + tl + "&dt=t&q="
                    + URLEncoder.encode(query, "UTF-8"));
            URLConnection connection = url.openConnection();
            connection.setRequestProperty("User-Agent", "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.95 Safari/537.11");
            connection.connect();

            BufferedReader r = new BufferedReader(new InputStreamReader(connection.getInputStream(), Charset.forName("UTF-8")));
            StringBuilder sb = new StringBuilder();
            String line;
            while((line = r.readLine()) != null) {
                sb.append(line);
            }

            CommandHelper.sendTagMessage(sb.toString().split("\"")[1], event);
        } catch(Exception e) {
            CommandHelper.sendTagMessage(e.getMessage(), event);
        }
    }

    public String help() {
        return Help.str("translate <language> <text>\nTranslates given text to provided language.");
    }

    public void executed(boolean success, MessageReceivedEvent event) {
        return;
    }
}