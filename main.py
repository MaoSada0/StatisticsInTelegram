import json

class colors:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

def openD():
    with open('result.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

def func(data, nickname):

    countTextMessages = 0
    countAudioMessages = 0
    countVideoMessages = 0
    countStickerMessages = 0
    countAnother = 0

    chats_and_stats = []

    if 'chats' in data and 'list' in data['chats']:
        for chat in data['chats']['list']:

            if("name" in chat):
                if chat['type'] == 'personal_chat':
                    new_chat = "Диалог с " + str(chat['name'])
                else:
                    new_chat = "Чат: " + str(chat['name'])
            else:
                new_chat = chat['type']

            new_stats2024 = {"countTextMessages": 0, "countAudioMessages": 0, "countVideoMessages": 0, "countStickerMessages": 0, "countAnother": 0, "all": 0}
            new_stats2023 = {"countTextMessages": 0, "countAudioMessages": 0, "countVideoMessages": 0, "countStickerMessages": 0, "countAnother": 0, "all": 0}
            new_stats2022 = {"countTextMessages": 0, "countAudioMessages": 0, "countVideoMessages": 0, "countStickerMessages": 0, "countAnother": 0, "all": 0}
            new_stats2021 = {"countTextMessages": 0, "countAudioMessages": 0, "countVideoMessages": 0, "countStickerMessages": 0, "countAnother": 0, "all": 0}
            new_stats2020 = {"countTextMessages": 0, "countAudioMessages": 0, "countVideoMessages": 0, "countStickerMessages": 0, "countAnother": 0, "all": 0}
            new_stats2019 = {"countTextMessages": 0, "countAudioMessages": 0, "countVideoMessages": 0, "countStickerMessages": 0, "countAnother": 0, "all": 0}

            new_stats = [new_stats2024, new_stats2023, new_stats2022, new_stats2021, new_stats2020, new_stats2019]


            for message in chat['messages']:
                if('from' in message and message['from'] == nickname):
                    if ('date' in message):
                        year = int((message['date'])[:4], 10)

                    if ('text' in message and len(message['text']) >= 1):
                        countTextMessages += 1
                    elif ("media_type" in message and message['media_type'] == 'video_message'):
                        countVideoMessages += 1
                    elif ("media_type" in message and message['media_type'] == 'sticker'):
                        countStickerMessages += 1
                    elif ("media_type" in message and message['media_type'] == 'voice_message'):
                        countAudioMessages += 1
                    else:
                        countAnother += 1


                    if(year >= 2019 and year <= 2024):
                        new_stats[2024 - year]["countTextMessages"] += countTextMessages
                        new_stats[2024 - year]["countAudioMessages"] += countAudioMessages
                        new_stats[2024 - year]["countVideoMessages"] += countVideoMessages
                        new_stats[2024 - year]["countStickerMessages"] += countStickerMessages
                        new_stats[2024 - year]["countAnother"] += countAnother

                    countTextMessages = 0
                    countAudioMessages = 0
                    countVideoMessages = 0
                    countStickerMessages = 0
                    countAnother = 0

            for i in range(0, 5):
                new_stats[i]["all"] = new_stats[i]["countTextMessages"] + new_stats[i]["countAudioMessages"] + new_stats[i]["countVideoMessages"] + new_stats[i]["countStickerMessages"] + new_stats[i]["countAnother"]

            chats_and_stats.append([new_chat, new_stats])

        year2019 = []
        year2020 = []
        year2021 = []
        year2022 = []
        year2023 = []
        year2024 = []

        years = [year2024, year2023, year2022, year2021, year2020, year2019]

        for chat, stats in chats_and_stats:
            for i, year_stats in enumerate(stats, start=0):
                if (year_stats['all'] != 0):
                    temp = [chat, year_stats]
                    years[i].append(temp)

        count = 1
        k = 0
        sum = 0

        for x in years:
            count = 1
            print(colors.RED + "Год: " + str(2024 - k) + colors.END)
            k += 1
            x = sorted(x, key=lambda x: x[1]['all'], reverse=True)
            #print(x)
            sum = 0
            for values in x:
                if(values[1]['all'] > 1):
                    print(f"Топ {count}", end=" ")
                    print(f"{values[0]}: {values[1]['all']}" + ((70 - len(str(values[0])) - len(str(values[1]['all'])) - len(str(count))) * " ") + f"(из них - гс: {values[1]['countAudioMessages']} | "
                          f"кружочков: {values[1]['countVideoMessages']} | текст"
                          f"овых: {values[1]['countTextMessages']} | стикеров: {values[1]['countStickerMessages']})")
                    count += 1
                sum += values[1]['all']

            print(colors.GREEN + "Общая сумма сообщений: " + str(sum) + colors.END)

        count = 1
        k = 0
        sum = 0

        with open('output.txt', 'w', encoding='utf-8') as file:
            for x in years:
                count = 1
                file.write("Год: " + str(2024 - k) + "\n")
                k += 1
                x = sorted(x, key=lambda x: x[1]['all'], reverse=True)
                sum = 0
                for values in x:
                    if values[1]['all'] > 10:
                        file.write(f"Топ {count} {values[0]}: {values[1]['all']}\n")
                        count += 1
                    sum += values[1]['all']

                file.write(f"Общая сумма сообщений: {sum}\n\n")


if __name__ == "__main__":

    data = openD()
    nickname = input("Введи свой никнейм: ")
    func(data, nickname)

