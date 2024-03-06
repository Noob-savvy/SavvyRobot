#  ZeldrisRobot
#  Copyright (C) 2017-2019, Paul Larsen
#  Copyright (C) 2022, IDNCoderX Team, <https://github.com/IDN-C-X/ZeldrisRobot>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with this program. If not, see <http://www.gnu.org/licenses/>.


import contextlib
import os
import re
import urllib
import urllib.parse
import urllib.request
from urllib.error import HTTPError, URLError

import requests
from bs4 import BeautifulSoup
from telegram import InputMediaPhoto, TelegramError, Update
from telegram.ext import CallbackContext

from SavvyRobot import dispatcher
from SavvyRobot.modules.disable import DisableAbleCommandHandler
from SavvyRobot.modules.helper_funcs.alternate import typing_action

opener = urllib.request.build_opener()
useragent = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.38 "
    "Safari/537.36 "
)
# useragent = 'Mozilla/5.0 (Linux; Android 6.0.1; SM-G920V Build/MMB29K) AppleWebKit/537.36 (KHTML, like Gecko)
# Chrome/52.0.2743.98 Mobile Safari/537.36'
opener.addheaders = [("User-agent", useragent)]


@typing_action
def reverse(
    update: Update, context: CallbackContext
):  # sourcery skip: low-code-quality
    if os.path.isfile("okgoogle.png"):
        os.remove("okgoogle.png")

    msg = update.effective_message
    chat_id = update.effective_chat.id
    rtmid = msg.message_id
    args = context.args
    imagename = "okgoogle.png"

    if reply := msg.reply_to_message:
        if reply.sticker:
            file_id = reply.sticker.file_id
        elif reply.photo:
            file_id = reply.photo[-1].file_id
        elif reply.document:
            file_id = reply.document.file_id
        else:
            msg.reply_text("Reply to an image or sticker to lookup.")
            return
        image_file = context.bot.get_file(file_id)
        image_file.download(imagename)
        if args:
            txt = args[0]
            try:
                lim = int(txt)
            except BaseException:
                lim = 2
        else:
            lim = 2
    elif args:
        splatargs = msg.text.split(" ")
        if len(splatargs) == 3:
            img_link = splatargs[1]
            try:
                lim = int(splatargs[2])
            except BaseException:
                lim = 2
        elif len(splatargs) == 2:
            img_link = splatargs[1]
            lim = 2
        else:
            msg.reply_text("/reverse <link> <amount of images to return.>")
            return
        try:
            urllib.request.urlretrieve(img_link, imagename)
        except HTTPError as HE:
            if HE.reason == "Forbidden":
                msg.reply_text(
                    "Couldn't access the provided link, The website might have blocked accessing to the website by "
                    "bot or the website does not existed. "
                )
                return
            if HE.reason == "Not Found":
                msg.reply_text("Image not found.")
                return
        except URLError as UE:
            msg.reply_text(f"{UE.reason}")
            return
        except ValueError as VE:
            msg.reply_text(f"{VE}\nPlease try again using http or https protocol.")
            return
    else:
        msg.reply_markdown(
            "Please reply to a sticker, or an image to search it!\nDo you know that you can search an image with a "
            "link too? `/reverse [picturelink] <amount>`. "
        )
        return

    try:
        search_url = "https://www.google.com/searchbyimage/upload"
        multipart = {
            "encoded_image": (imagename, open(imagename, "rb")),
            "image_content": "",
        }
        response = requests.post(search_url, files=multipart, allow_redirects=False)
        fetch_url = response.headers["Location"]

        if response != 400:
            xx = context.bot.send_message(
                chat_id,
                "Image was successfully uploaded to Google."
                "\nParsing source now. Maybe.",
                reply_to_message_id=rtmid,
            )
        else:
            context.bot.send_message(
                chat_id, "Google told me to go away.", reply_to_message_id=rtmid
            )
            return

        os.remove(imagename)
        match = parse_sauce(f"{fetch_url}&hl=en")
        guess = match["best_guess"]
        if match["override"] and match["override"] != "":
            imgspage = match["override"]
        else:
            imgspage = match["similar_images"]

        if guess and imgspage:
            xx.edit_text(
                f"[{guess}]({fetch_url})\nLooking for images...",
                parse_mode="Markdown",
                disable_web_page_preview=True,
            )
        else:
            xx.edit_text("Couldn't find anything.")
            return

        images = scam(imgspage, lim)
        if len(images) == 0:
            xx.edit_text(
                f"[{guess}]({fetch_url})\n\n[Visually similar images]({imgspage})",
                parse_mode="Markdown",
                disable_web_page_preview=True,
            )
            return

        imglinks = []
        for link in images:
            lmao = InputMediaPhoto(media=str(link))
            imglinks.append(lmao)

        context.bot.send_media_group(
            chat_id=chat_id, media=imglinks, reply_to_message_id=rtmid
        )
        xx.edit_text(
            f"[{guess}]({fetch_url})\n\n[Visually similar images]({imgspage})",
            parse_mode="Markdown",
            disable_web_page_preview=True,
        )
    except TelegramError as e:
        print(e)
    except Exception as exception:
        print(exception)


def parse_sauce(googleurl):
    source = opener.open(googleurl).read()
    soup = BeautifulSoup(source, "html.parser")

    results = {"similar_images": "", "override": "", "best_guess": ""}

    with contextlib.suppress(BaseException):
        for bess in soup.findAll("a", {"class": "PBorbe"}):
            url = "https://www.google.com" + bess.get("href")
            results["override"] = url

    for similar_image in soup.findAll("input", {"class": "gLFyf"}):
        url = "https://www.google.com/search?tbm=isch&q=" + urllib.parse.quote_plus(
            similar_image.get("value")
        )
        results["similar_images"] = url

    for best_guess in soup.findAll("div", attrs={"class": "r5a77d"}):
        results["best_guess"] = best_guess.get_text()

    return results


def scam(imgspage, lim):
    """Parse/Scrape the HTML code for the info we want."""

    single = opener.open(imgspage).read()
    decoded = single.decode("utf-8")
    if int(lim) > 10:
        lim = 10

    imglinks = []
    counter = 0

    pattern = r"^,\[\"(.*[.png|.jpg|.jpeg])\",[0-9]+,[0-9]+\]$"
    oboi = re.findall(pattern, decoded, re.I | re.M)

    for imglink in oboi:
        counter += 1
        imglinks.append(imglink)
        if counter >= int(lim):
            break

    return imglinks


REVERSE_HANDLER = DisableAbleCommandHandler(
    ["reverse", "grs"],
    reverse,
    pass_args=True,
    run_async=True,
)

dispatcher.add_handler(REVERSE_HANDLER)
