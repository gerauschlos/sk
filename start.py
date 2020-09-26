from bot import bot
import yaml

if __name__ == "__main__":
    with open("config.yaml") as f:
        token = yaml.load(f, Loader=yaml.FullLoader)["discord"]["token"]

    bot.run(token)
