import asyncio
import hashlib
import json
import sys
import urllib
import urllib.parse
from secrets.secrets import Secrets

import qrcode
from PIL import Image, ImageDraw, ImageFont
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.colormasks import (RadialGradiantColorMask,
                                            SolidFillColorMask)
from qrcode.image.styles.moduledrawers import (CircleModuleDrawer,
                                               RoundedModuleDrawer,
                                               SquareModuleDrawer)

from bot.bot import Bot
from database.database import Database
from database.tables.btype import Btype
from database.tables.department import Department
from database.tables.employee import Employee
from database.tables.floor import Floor
from database.tables.request import Request
from database.tables.zone import Zone
from session.session import Session

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


db = Database()


#async def main():
#    url_android = "https://www.rustore.ru/catalog/app/com.itrack.ohanamytishhi946647"
#    url_ios = "https://apps.apple.com/ru/app/ohana-fit/id1367392036"
#    #url = urllib.parse.quote(params, encoding="utf-8")
#    qr = qrcode.QRCode(
#        version=1,
#        error_correction=qrcode.constants.ERROR_CORRECT_H,
#        box_size=3,
#        border=2,
#    )
#    
#    #logo = Image.open('favicon.ico')
#    qr.add_data(url_android)
#    qr.make(fit=True)
#    
#    img = qr.make_image(
#        image_factory=StyledPilImage,
#        back_color="black",
#        module_drawer=RoundedModuleDrawer(),
#        color_mask=RadialGradiantColorMask(),
#        embeded_image_path="favicon.ico"
#    )
#    
#    img.save(f"android.png")
#
#
#    qr2 = qrcode.QRCode(
#        version=1,
#        error_correction=qrcode.constants.ERROR_CORRECT_H,
#        box_size=3,
#        border=2,
#    )
#    
#    #logo = Image.open('favicon.ico')
#    qr2.add_data(url_ios)
#    qr2.make(fit=True)
#    
#    img2 = qr2.make_image(
#        image_factory=StyledPilImage,
#        back_color="black",
#        module_drawer=RoundedModuleDrawer(),
#        color_mask=RadialGradiantColorMask(),
#        embeded_image_path="favicon.ico"
#    )
#    
#    img2.save(f"ios.png")
async def main():
    for link, club_name in [
        ["https://club.myfitt.ru/join/ohana-msk", "Новомосковский"],
        ["https://club.myfitt.ru/join/ohana-vlk", "Волковский"],
        ["https://club.myfitt.ru/join/ohana-nkr", "Некрасовка"],
        ["https://club.myfitt.ru/join/ohana-bun", "Бунинская"]
    ]:
        
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=3,
            border=6,
        )

        #logo = Image.open('favicon.ico')
        qr.add_data(link)
        qr.make(fit=True)

        img = qr.make_image(
            image_factory=StyledPilImage,
            back_color="black",
            module_drawer=RoundedModuleDrawer(),
            color_mask=RadialGradiantColorMask(),
            embeded_image_path="favicon.ico"
        )

        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype(font="arial.ttf", size=15, encoding="UTF-8")

        #draw.text(xy=(15, 2), text=f"Клуб: {club_name}", fill="black", align="center", font=font)
        draw.text(xy=(35, 2), text=f"{link.split('/')[-1]}", fill="black", align="center", font=font)

        img.save(f"{link.split('/')[-1]}.png")

if __name__ == '__main__':
    asyncio.run(main=main())