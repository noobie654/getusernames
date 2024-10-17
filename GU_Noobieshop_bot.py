const TelegramBot = require('node-telegram-bot-api');

// Replace with your actual API Token
const token = '7475923472:AAGI5k2w-KglPQiTLQqe1VWrysmVtnSdHIk'; // Bot token

// Create the bot client
const bot = new TelegramBot(token, { polling: true });

// Set the passwords
const BOT_PASSWORDS = ['@Antor1040', '@NoobieNoiso', '@RionMental26']; // List of passwords

// Dictionary to store which users have unlocked the bot
let unlockedUsers = {};

// Start command event handler
bot.onText(/\/start/, (msg) => {
  const chatId = msg.chat.id;
  bot.sendMessage(chatId, 
    `Welcome to GU_Noobieshop Bot! Please get the password from the admin:
Contact Support: [Noobie Support](https://t.me/NoobieXNoiso)
Join our Channel: [Noobie Channel](https://t.me/NoobieShopp)`,
    { parse_mode: 'Markdown' }
  );
});

// Password check event handler
bot.on('message', (msg) => {
  const chatId = msg.chat.id;
  const userId = msg.from.id;
  const text = msg.text;

  // If the user has already unlocked the bot
  if (unlockedUsers[userId]) {
    // User can now enter a group or channel URL to fetch usernames
    bot.sendMessage(chatId, "Please enter the group URL to fetch usernames.");
  } else if (BOT_PASSWORDS.includes(text)) {
    // If the user enters the correct password
    unlockedUsers[userId] = true;
    bot.sendMessage(chatId, "✅ Bot unlocked successfully! Please enter the group or channel URL to fetch usernames:");
  } else {
    // Invalid password
    bot.sendMessage(chatId, "Incorrect password, please try again.");
  }
});

// Cancel action if necessary (you can add this feature with custom keyboard or inline buttons)
// Fetch Usernames from Group or Channel (Not directly supported in node-telegram-bot-api, so this requires Telegram's API)
bot.onText(/http(s?):\/\/t\.me\/(.+)/, async (msg) => {
  const chatId = msg.chat.id;
  const groupUrl = msg.text.trim();
  const userId = msg.from.id;

  if (unlockedUsers[userId]) {
    try {
      const groupUsername = groupUrl.split('/').pop(); // Extract the username from URL
      const members = await bot.getChatMembersCount(groupUsername); // Get the number of members

      if (members > 0) {
        bot.sendMessage(chatId, `Group/Channel has ${members} members.`);
      } else {
        bot.sendMessage(chatId, "No usernames found or unable to retrieve members.");
      }
    } catch (error) {
      bot.sendMessage(chatId, "Invalid group or channel URL.");
    }
  } else {
    bot.sendMessage(chatId, "Please unlock the bot first by typing /start.");
  }
});
