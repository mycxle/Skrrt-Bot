package studio.bytesize.skrrtbot;

import net.dv8tion.jda.core.AccountType;
import net.dv8tion.jda.core.JDA;
import net.dv8tion.jda.core.JDABuilder;
import studio.bytesize.skrrtbot.commands.*;

import java.io.BufferedReader;
import java.io.FileReader;
import java.util.HashMap;

public class Main {
    public static JDA jda;
    public static CommandParser parser = new CommandParser();
    public static HashMap<String, Command> commands = new HashMap<>();
    public static String PREFIX = "/";

    public static void main(String[] args) {
        try {
            BufferedReader br = new BufferedReader(new FileReader("prefix.txt"));
            String line = br.readLine();
            System.out.println(line);
            PREFIX = line;
        } catch (Exception e) {

        }

        try {
            jda = new JDABuilder(AccountType.BOT).addEventListener(new BotListener()).setToken(Secret.getToken()).buildBlocking();
        } catch (Exception e) {
            e.printStackTrace();
        }

        commands.put("ping", new PingCommand());
        commands.put("say", new SayCommand());
        commands.put("8ball", new EightBallCommand());
        commands.put("choose", new ChooseCommand());
        commands.put("help", new HelpCommand());
        commands.put("coin", new CoinCommand());
        commands.put("leet", new LeetCommand());
        commands.put("chucknorris", new ChuckCommand());
        commands.put("define", new DefineCommand());
        commands.put("comic", new ComicCommand());
        commands.put("rockpaperscissors", new RockPaperScissorsCommand());
        commands.put("meme", new MemeCommand());
        commands.put("weather", new WeatherCommand());
        commands.put("binary", new BinaryCommand());
        commands.put("hex", new HexCommand());
        commands.put("octal", new OctalCommand());
        commands.put("roll", new RollCommand());
        commands.put("translate", new TranslateCommand());
        commands.put("prefix", new PrefixCommand());
    }

    public static void handleCommand(CommandParser.CommandContainer cmd) {
        if(commands.containsKey(cmd.invoke)) {
            boolean safe = commands.get(cmd.invoke).called(cmd.args, cmd.e);

            if(safe) {
                commands.get(cmd.invoke).action(cmd.args, cmd.e);
                commands.get(cmd.invoke).executed(safe, cmd.e);
            } else {
                commands.get(cmd.invoke).executed(safe, cmd.e);
            }
        }
    }
}
