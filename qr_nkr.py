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


async def main():
    method = Secrets.BOT_LINK
    
    for club, floor, zone, btype in [
        [Department().nkr, Floor().first, Zone().salesdep, Btype().phone],
        [Department().nkr, Floor().first, Zone().salesdep, Btype().network],
        [Department().nkr, Floor().first, Zone().salesdep, Btype().pcs],
        [Department().nkr, Floor().first, Zone().salesdep, Btype().tvs],
        [Department().nkr, Floor().first, Zone().salesdep, Btype().printer],
        [Department().nkr, Floor().first, Zone().servdep, Btype().phone],
        [Department().nkr, Floor().first, Zone().servdep, Btype().network],
        [Department().nkr, Floor().first, Zone().servdep, Btype().pcs],
        [Department().nkr, Floor().first, Zone().servdep, Btype().tvs],
        [Department().nkr, Floor().first, Zone().servdep, Btype().printer],
        [Department().nkr, Floor().first, Zone().hall, Btype().network],
        [Department().nkr, Floor().first, Zone().hall, Btype().elcash],
        [Department().nkr, Floor().first, Zone().reciep, Btype().network],
        [Department().nkr, Floor().first, Zone().reciep, Btype().pcs],
        [Department().nkr, Floor().first, Zone().reciep, Btype().phone],
        [Department().nkr, Floor().first, Zone().reciep, Btype().accont],
        [Department().nkr, Floor().first, Zone().bar, Btype().network],
        [Department().nkr, Floor().first, Zone().bar, Btype().sound],
        [Department().nkr, Floor().first, Zone().cash, Btype().network],
        [Department().nkr, Floor().first, Zone().cash, Btype().pcs],
        [Department().nkr, Floor().first, Zone().pool, Btype().tablet],
        [Department().nkr, Floor().first, Zone().pool, Btype().sound],
        [Department().nkr, Floor().first, Zone().cash, Btype().network],
        [Department().nkr, Floor().first, Zone().cash, Btype().pcs],
        [Department().nkr, Floor().second, Zone().kidclub, Btype().tablet],
        [Department().nkr, Floor().second, Zone().kidclub, Btype().sound],
        [Department().nkr, Floor().second, Zone().hall, Btype().network],
        [Department().nkr, Floor().second, Zone().hall, Btype().tvs],
        [Department().nkr, Floor().second, Zone().locker, Btype().tvs],
        [Department().nkr, Floor().third, Zone().gym, Btype().sound],
        [Department().nkr, Floor().third, Zone().gym, Btype().tvs],
        [Department().nkr, Floor().third, Zone().ant, Btype().network],
        [Department().nkr, Floor().third, Zone().ant, Btype().pcs],
        [Department().nkr, Floor().third, Zone().ant, Btype().printer],
        [Department().nkr, Floor().mfirst, Zone().spa, Btype().network],
        [Department().nkr, Floor().mfirst, Zone().spa, Btype().pcs],
        [Department().nkr, Floor().mfirst, Zone().spa, Btype().phone],
        [Department().nkr, Floor().mfirst, Zone().hall, Btype().accont],
        [Department().nkr, Floor().mfirst, Zone().marts, Btype().sound],
        [Department().nkr, Floor().mfirst, Zone().marts, Btype().tablet],
        [Department().nkr, Floor().mfirst, Zone().tech, Btype().accont],
        [Department().nkr, Floor().mfirst, Zone().shower, Btype().sound],
        [Department().nkr, Floor().mfirst, Zone().spa, Btype().emptablet],
        [Department().nkr, Floor().mfirst, Zone().spa, Btype().accont]
    ]:
        club_db = await db.select_department_by_sign(sign=club)
        floor_db = await db.select_floor_by_sign(sign=floor)
        zone_db = await db.select_zone_by_sign(sign=zone)
        btype_db = await db.select_btype_by_sign(sign=btype)
        
        # params = f"Клуб: {club}\nЭтаж: {floor}\nЗона: {zone}\nПоломка: {btype}\nОписание: "
        # hash = hashlib.md5((params).encode()).hexdigest()
        print(f"{club}-{floor}-{zone}-{btype}")
        print(f"{club_db}-{floor_db}-{zone_db}-{btype_db}\n")
        params = f"{club_db[0]}-{floor_db[0]}-{zone_db[0]}-{btype_db[0]}\n"
        params_ = urllib.parse.quote(params, encoding="utf-8")
        url = f"{method}?start={params_}"
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=3,
            border=28,
        )
        
        logo = Image.open('favicon.ico')
        qr.add_data(url)
        qr.make(fit=True)
        
        img = qr.make_image(
            image_factory=StyledPilImage,
            back_color="cyan",
            module_drawer=RoundedModuleDrawer(),
            color_mask=RadialGradiantColorMask(),
            embeded_image_path="favicon.ico"
        )
        
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype(font="arial.ttf", size=15, encoding="UTF-8")
        
        # Измененный порядок и расположение текста
        y_position = 0
        line_height = 15
        
        draw.text(xy=(65, y_position), text=f"Клуб: {club}", fill="black", font=font)
        y_position += line_height
        
        draw.text(xy=(65, y_position), text=f"Этаж: {floor}", fill="black", font=font)
        y_position += line_height
        
        draw.text(xy=(65, y_position), text=f"Зона: {zone}", fill="black", font=font)
        y_position += line_height
        
        draw.text(xy=(65, y_position), text=f"Поломка: {btype}", fill="black", font=font)
        
        img.save(f"QR\\nkr\\{club}_{floor}_{zone}_{btype}.png")


if __name__ == '__main__':
    asyncio.run(main=main())