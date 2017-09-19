package studio.bytesize.skrrtbot;

import java.io.BufferedReader;
import java.io.FileReader;

public class Secret {
    public static String BOT_TOKEN;

    public static String getToken() {
        try {
            BufferedReader br = new BufferedReader(new FileReader("token.txt"));
            try {
                StringBuilder sb = new StringBuilder();
                String line = br.readLine();

                while (line != null) {
                    sb.append(line);
                    sb.append(System.lineSeparator());
                    line = br.readLine();
                }
                BOT_TOKEN = sb.toString();
                BOT_TOKEN = BOT_TOKEN.substring(0, BOT_TOKEN.length() - 2);
            } finally {
                br.close();
            }
        } catch(Exception e) {
            e.printStackTrace();
        }

        System.out.println(BOT_TOKEN);

        return BOT_TOKEN;
    }
}
