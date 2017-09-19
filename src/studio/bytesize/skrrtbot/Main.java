package studio.bytesize.skrrtbot;

import net.dv8tion.jda.core.AccountType;
import net.dv8tion.jda.core.JDA;
import net.dv8tion.jda.core.JDABuilder;
import studio.bytesize.skrrtbot.commands.EightBallCommand;
import studio.bytesize.skrrtbot.commands.PingCommand;
import studio.bytesize.skrrtbot.commands.SayCommand;

import java.util.HashMap;

public class Main {
    public static JDA jda;
    public static CommandParser parser = new CommandParser();
    public static HashMap<String, Command> commands = new HashMap<>();

    public static void main(String[] args) {
        try {
            jda = new JDABuilder(AccountType.BOT).addEventListener(new BotListener()).setToken(Secret.getToken()).buildBlocking();
        } catch (Exception e) {
            e.printStackTrace();
        }

        commands.put("ping", new PingCommand());
        commands.put("say", new SayCommand());
        commands.put("8ball", new EightBallCommand());
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
