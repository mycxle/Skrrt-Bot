package studio.bytesize.skrrtbot;

import net.dv8tion.jda.core.events.message.MessageReceivedEvent;
import net.dv8tion.jda.core.hooks.ListenerAdapter;

public class BotListener extends ListenerAdapter {
    public void onMessageReceived(MessageReceivedEvent e) {
        if(e.getMessage().getContent().startsWith(Main.PREFIX) && e.getMessage().getAuthor().getId() != e.getJDA().getSelfUser().getId()) {
            Main.handleCommand(Main.parser.parse(e.getMessage().getContent(), e));
           //  Main.handleCommand(Main.parser.parse(e.getMessage().getContent().toLowerCase(), e)); <--- OLD VERSION
        }
    }
}