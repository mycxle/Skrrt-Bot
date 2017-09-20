package studio.bytesize.skrrtbot.util;

import net.dv8tion.jda.core.events.message.MessageReceivedEvent;

public class CommandHelper {
    public static String getUserTag(MessageReceivedEvent event) {
        return "<@!" + event.getMember().getUser().getId() + ">";
    }

    public static void sendMessage(String msg, MessageReceivedEvent event) {
        event.getTextChannel().sendMessage(msg).complete();
    }

    public static void sendTagMessage(String msg, MessageReceivedEvent event) {
        sendMessage(getUserTag(event) + " " + msg, event);
    }
}
