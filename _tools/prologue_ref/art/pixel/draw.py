"""Build the prologue player equipment at native resolution.

Run with Python and Pillow/Numpy. The three demon outfits are authored at
fixed pixel coordinates. Lucifer samples the Full Metal Armor mesh UVs and
matches gold trim to the player elytra. Every output obeys the supplied vanilla mask.
"""
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
ART = HERE.parent
MASK_FILES = {"humanoid": "vanilla_humanoid_iron.png", "leggings": "vanilla_leggings_iron.png", "wings": "vanilla_wings_elytra.png"}

# Fixed ramps run from colored outline to upper-left specular highlight.
RAMPS = {
    "shell": ["#151B0C", "#303B13", "#5A6B1E", "#869B35", "#B5D957"],
    "vein": ["#334313", "#566D22", "#7B9D38", "#B5D957", "#D6EF91"],
    "fly": ["#242C24", "#41493C", "#6A6F60", "#929783", "#BBC0AC"],
    "silk": ["#29132F", "#40204C", "#5B2C6F", "#9C4EA8", "#D97AD9"],
    "bronze": ["#38220F", "#5E3A16", "#A8743A", "#CA975C", "#E3BF83"],
    "gold": ["#624207", "#89630C", "#B7950B", "#E6A23C", "#F5D982"],
    "leather": ["#23180F", "#3C281B", "#5A3A22", "#805633", "#AD7C4A"],
    "black": ["#100C0A", "#1A1410", "#2D231B", "#45362A", "#67513C"],
    "feather": ["#4B4A42", "#747267", "#A4A295", "#C7C3B3", "#E0DCCA"],
    "ancient_gold": ["#594718", "#79602C", "#A18748", "#BEA365", "#D5BF87"],
    "snake": ["#002B12", "#00491C", "#165F34", "#39764F", "#669675"],
}
RAMPS = {k: [tuple(bytes.fromhex(c[1:])) + (255,) for c in v] for k, v in RAMPS.items()}

# Standard Minecraft cube-unwrapped faces: side, front, side, back, top.
FACES = {
    "head": [(0,8,8,8), (8,8,8,8), (16,8,8,8), (24,8,8,8), (8,0,8,8)],
    "body": [(16,20,4,12), (20,20,8,12), (28,20,4,12), (32,20,8,12), (20,16,8,4)],
    "arm": [(40,20,4,12), (44,20,4,12), (48,20,4,12), (52,20,4,12), (44,16,4,4)],
    "leg": [(0,20,4,12), (4,20,4,12), (8,20,4,12), (12,20,4,12), (4,16,4,4)],
}

# Fixed source UV coordinates traced through the unpacked Full Metal Armor mesh.
# Each four hex digits encodes one (x,y) source pixel in its original 64x64 tile.
LUCIFER_UV = {
    ('head', 0): (
        '08090709060905090309020901090009',
        '080b070b060b050b030b020b010b000b',
        '080c070c060c050c030c020c010c000c',
        '080d070d060d050d030d020d010d000d',
        '080f070f060f050f030f020f010f000f',
        '08100710061005100310021001100010',
        '08110711061105110311021101110011',
        '08130713061305130313021301130013',
    ),
    ('head', 1): (
        '09090a090c090d090e090f0911091209',
        '090b0a0b0c0b0d0b0e0b0f0b110b120b',
        '090c0a0c0c0c0d0c0e0c0f0c110c120c',
        '090d0a0d0c0d0d0d0e0d0f0d110d120d',
        '090f0a0f0c0f0d0f0e0f0f0f110f120f',
        '09100a100c100d100e100f1011101210',
        '09110a110c110d110e110f1111111211',
        '09130a130c130d130e130f1311131213',
    ),
    ('head', 2): (
        '1c091b09190918091709160914091309',
        '1c0b1b0b190b180b170b160b140b130b',
        '1c0c1b0c190c180c170c160c140c130c',
        '1c0d1b0d190d180d170d160d140d130d',
        '1c0f1b0f190f180f170f160f140f130f',
        '1c101b10191018101710161014101310',
        '1c111b11191118111711161114111311',
        '1c131b13191318131713161314131313',
    ),
    ('head', 3): (
        '1d091e09200921092209230925092609',
        '1d0b1e0b200b210b220b230b250b260b',
        '1d0c1e0c200c210c220c230c250c260c',
        '1d0d1e0d200d210d220d230d250d260d',
        '1d0f1e0f200f210f220f230f250f260f',
        '1d101e10201021102210231025102610',
        '1d111e11201121112211231125112611',
        '1d131e13201321132213231325132613',
    ),
    ('head', 4): (
        '09080a080c080d080e080f0811081208',
        '09070a070c070d070e070f0711071207',
        '09060a060c060d060e060f0611061206',
        '09050a050c050d050e050f0511051205',
        '09030a030c030d030e030f0311031203',
        '09020a020c020d020e020f0211021202',
        '09010a010c010d010e010f0111011201',
        '09000a000c000d000e000f0011001200',
    ),
    ('body', 0): (
        '041a041a041a041a',
        '3701041a032e012e',
        '37020219001a012f',
        '0419021a001b0130',
        '051a031b011c0131',
        '051b031c011d0133',
        '041a041d021e001f',
        '041a041e021f0020',
        '041a051f03200136',
        '041a041a03370137',
        '041a3c1903380138',
        '041a3c1a03390139',
    ),
    ('body', 1): (
        '041a041a041a041a041a041a041a041a',
        '062e072e380139013b013c010e2e0f2e',
        '06160716380239023b023c020e160f16',
        '0618071809180a180b180c180e180f18',
        '0619071909190a190b190c190e190f19',
        '061b071b091b0a1b0b1b0c1b0e1b0f1b',
        '061c071c091c0a1c0b1c0c1c0e1c0f1c',
        '061d071d091d0a1d0b1d0c1d0e1d0f1d',
        '061e071e091e0a1e0b1e0c1e0e1e0f1e',
        '061f071f091f0a1f0b1f0c1f0e1f0f1f',
        '0638073809383d1f3f1f0c380e380f38',
        '0639073909393d203f200c390e390f39',
    ),
    ('body', 2): (
        '041a041a041a041a',
        '142e122e041a3101',
        '142f151a13193102',
        '1430151b131a1119',
        '1431141c121b101a',
        '1433141d121c101b',
        '151f131e111d041a',
        '1520131f111e041a',
        '14361220101f041a',
        '14371237041a041a',
        '14381238381e041a',
        '14391239381f041a',
    ),
    ('body', 3): (
        '041a041a041a041a041a041a041a041a',
        '162e172e192e1a2e1b2e1c2e1e2e1f2e',
        '162f172f192f1a2f1b2f1c2f1e2f1f2f',
        '1630173019301a301b301c301e301f30',
        '1631173119311a311b311c311e311f31',
        '1633173319331a331b331c331e331f33',
        '1634173419341a341b341c341e341f34',
        '1635173519351a351b351c351e351f35',
        '1636173619361a361b361c361e361f36',
        '1637173719371a371b371c371e371f37',
        '1638173819383d213f211c381e381f38',
        '1639173919393d223f221c391e391f39',
    ),
    ('body', 4): (
        '0617071736013501330132010e170f17',
        '0615071509150a150b150c150e150f15',
        '062b072b092b0a2b0b2b0c2b0e2b0f2b',
        '0629072909290a290b290c290e290f29',
    ),
    ('arm', 0): (
        '1401160118011a01',
        '3106330634061a03',
        '3107330734071a04',
        '3108330834081a05',
        '310a330a340a1a07',
        '041a041a041a041a',
        '041a041a041a041a',
        '041a041a041a041a',
        '2f1431143314041a',
        '2f1531153315041a',
        '2f1631163316041a',
        '201822182418041a',
    ),
    ('arm', 1): (
        '041a041a041a1b01',
        '30062e062d061b03',
        '30072e072d071b04',
        '30082e082d081b05',
        '300a2e0a2d0a1b07',
        '041a041a041a041a',
        '041a041a041a041a',
        '041a041a041a041a',
        '041a34142d14041a',
        '041a041a2d15041a',
        '041a041a2d16041a',
        '041a041a1e181d18',
    ),
    ('arm', 2): (
        '1c011e0120012201',
        '1c031e0320032203',
        '1c041e0420042204',
        '1c051e0520052205',
        '1c071e0720072207',
        '041a041a041a041a',
        '041a041a041a041a',
        '041a041a041a041a',
        '041a38143a143c14',
        '041a38153a153c15',
        '041a38163a163c16',
        '041a2a182c182e18',
    ),
    ('arm', 3): (
        '1301041a041a041a',
        '1303390637063606',
        '1304390737073607',
        '1305390837083608',
        '1307390a370a360a',
        '041a041a041a041a',
        '041a041a041a041a',
        '041a041a041a041a',
        '041a36143514041a',
        '041a3615041a041a',
        '041a3616041a041a',
        '28182718041a041a',
    ),
    ('arm', 4): (
        '30052e052d051a00',
        '30032e032d031800',
        '30012e012d011600',
        '041a041a041a1400',
    ),
    ('leg', 0): (
        '382a392a3b2a3c2a',
        '382b392b3b2b3c2b',
        '382b392b3b2b3c2b',
        '382c392c3b2c3c2c',
        '382d392d3b2d3c2d',
        '041a041a041a041a',
        '2b3e041a041a041a',
        '2b3e323a313a303a',
        '2b3d323b313b303b',
        '2b3c323c313c303c',
        '2b3c323c313c303c',
        '2b3b041a041a041a',
    ),
    ('leg', 1): (
        '372a352a041a041a',
        '372b352b041a041a',
        '372b352b041a041a',
        '372c352c041a041a',
        '372d352d041a041a',
        '041a041a041a041a',
        '263b273b293b2a3b',
        '263b273b293b2a3b',
        '263c273c293c2a3c',
        '263d273d293d2a3d',
        '263d273d293d2a3d',
        '263e273e293e2a3e',
    ),
    ('leg', 2): (
        '382339233b233c23',
        '382439243b243c24',
        '382439243b243c24',
        '382539253b253c25',
        '382639263b263c26',
        '041a041a041a041a',
        '041a041a041a253e',
        '3b3a3a3a393a383a',
        '3b3b3a3b393b383b',
        '3b3c3a3c393c383c',
        '3b3c3a3c393c383c',
        '041a041a041a253b',
    ),
    ('leg', 3): (
        '041a041a3f2a3d2a',
        '041a041a3f2b3d2b',
        '041a041a3f2b3d2b',
        '041a041a3f2c3d2c',
        '041a041a3f2d3d2d',
        '041a041a041a041a',
        '2f3e2e3e2d3e2c3e',
        '3c3a3d3a3e3a3f3a',
        '3c3b3d3b3e3b3f3b',
        '3c3c3d3c3e3c3f3c',
        '3c3c3d3c3e3c3f3c',
        '2f3b2e3b2d3b2c3b',
    ),
    ('leg', 4): (
        '3c273c29273a263a',
        '3b273b2936393739',
        '3927392936383738',
        '3827382936373737',
    ),
}


def projected_face(part, width, height, face):
    atlas = Image.open(ART.parent / "models/out/lucifer/atlas.png").convert("RGBA")
    source = np.asarray(atlas)[0:64,64:128]
    opaque = np.argwhere(source[:,:,3] == 255)
    output = Image.new("RGBA", (width, height))
    for y, row in enumerate(LUCIFER_UV[(part, face)]):
        coordinates = bytes.fromhex(row)
        for x in range(width):
            u, v = coordinates[x*2:x*2+2]
            color = atlas.getpixel((64+u,v))
            if color[3] == 0:
                # Fill the vanilla-required coverage with its nearest original texel.
                sy, sx = opaque[np.argmin(np.sum((opaque-[v,u])**2, axis=1))]
                color = atlas.getpixel((64+int(sx),int(sy)))
            output.putpixel((x,y), color)
    return output


def ramp_fill(image, rect, material, bias=0):
    x,y,w,h=rect
    colors=RAMPS[material]
    for v in range(h):
        for u in range(w):
            # A broad upper-left face, shadowed bottom and single-pixel bevel.
            level = 2
            if u == 0 or v == 0: level = 3
            if u == w-1 or v == h-1: level = 0
            if u == w-2 or v == h-2: level = 1
            if u == 1 and v == 1: level = 4
            image.putpixel((x+u,y+v),colors[max(0,min(4,level+bias))])


def line(draw, points, material, level=3):
    draw.line(points, fill=RAMPS[material][level], width=1)


def humanoid(character, layer):
    material = {"beelzebub":"shell", "belial":"silk", "mammon":"black"}[character]
    output = Image.new("RGBA", (64,32), RAMPS[material][1])
    for part,faces in FACES.items():
        for face,rect in enumerate(faces):
            ramp_fill(output,rect,material, -1 if face in (2,3) else 0)
    draw=ImageDraw.Draw(output)
    accent={"beelzebub":"vein", "belial":"bronze", "mammon":"gold"}[character]
    # Crown band and center inset remain visible through the helmet cutouts.
    for base in (0,8,16,24):
        line(draw,[(base,9),(base+7,9)],accent,2)
        line(draw,[(base+1,8),(base+6,8)],accent,4)
    line(draw,[(11,8),(11,11),(12,11),(12,8)],accent,3)
    for part in ("body","arm","leg"):
        for face,(x,y,w,h) in enumerate(FACES[part][:4]):
            if character == "beelzebub":
                # Nested shell plates and bright, slender insect channels.
                for row in (2,5,8):
                    line(draw,[(x,y+row),(x+w//2,y+row+1),(x+w-1,y+row)],"shell",0)
                    line(draw,[(x+1,y+row-1),(x+w-2,y+row-1)],"shell",3)
                line(draw,[(x+w//2,y+1),(x+w//2,y+h-2)],"vein",2)
                draw.point((x+w//2,y+3), fill=RAMPS['vein'][4])
                draw.point((x+w//2,y+h-2),fill=RAMPS["vein"][0])
                draw.point((x+w//2,y+h-3),fill=RAMPS["vein"][1])
                if part == "body" and face == 1:
                    for dx in (1,w-2): draw.point((x+dx,y+1),fill=RAMPS['vein'][3])
                    for yy in (y+3,y+6):
                        line(draw,[(x,yy),(x+2,yy+1),(x+5,yy+1),(x+7,yy)],"fly",2)
                        draw.point((x+1,yy),fill=RAMPS['fly'][4])
            elif character == "belial":
                # Silk pleats beneath bronze collar, breastplate and cuffs.
                line(draw,[(x+1,y+2),(x+1,y+h-2)],"silk",3)
                line(draw,[(x+w-2,y+3),(x+w-2,y+h-2)],"silk",1)
                if part == "body":
                    line(draw,[(x,y),(x+w//2,y+3),(x+w-1,y)],"bronze",3)
                    line(draw,[(x,y+1),(x+w//2,y+4),(x+w-1,y+1)],"bronze",1)
                    draw.point((x+w//2,y+5),fill=RAMPS["bronze"][0])
                    line(draw,[(x,y+7),(x+w-1,y+7)],"bronze",2)
                    for dx in range(1,w-1,2): draw.point((x+dx,y+8),fill=RAMPS['bronze'][4])
                    if face == 1:
                        line(draw,[(x+1,y+4),(x+1,y+6),(x+6,y+6),(x+6,y+4)],"bronze",2)
                        draw.rectangle((x+2,y+4,x+5,y+5),fill=RAMPS['silk'][0])
                        draw.point((x+2,y+4),fill=RAMPS['silk'][4])
                        draw.point((x+5,y+4),fill=RAMPS['silk'][4])
                else:
                    for yy in (y+1,y+8,y+10): line(draw,[(x,yy),(x+w-1,yy)],"bronze",2)
                    draw.point((x+1,y+9),fill=RAMPS['silk'][4])
            else:
                # Heavy gold armor, chest chain and coin belt over leather.
                if part == "body":
                    ramp_fill(output,(x,y,w,7),"gold", -1 if face in (2,3) else 0)
                    line(draw,[(x,y+8),(x+w-1,y+8)],"leather",3)
                    line(draw,[(x,y+9),(x+w-1,y+9)],"gold",1)
                    for dx in range(1,w,3): draw.point((x+dx,y+9),fill=RAMPS['gold'][4])
                    if face == 1:
                        for dx in (1,5):
                            draw.rectangle((x+dx,y+4,x+dx+1,y+6),fill=RAMPS['leather'][2])
                            draw.point((x+dx,y+4),fill=RAMPS['leather'][4])
                            draw.point((x+dx,y+5),fill=RAMPS["leather"][3])
                            draw.point((x+dx,y+6),fill=RAMPS["leather"][0])
                            draw.point((x+dx+1,y+6),fill=RAMPS["leather"][1])
                            draw.point((x+dx+1,y+5),fill=RAMPS['gold'][4])
                        line(draw,[(x+1,y+1),(x+3,y+2),(x+6,y+1)],"gold",4)
                        draw.rectangle((x+2,y+8,x+5,y+10),fill=RAMPS['gold'][3])
                        draw.rectangle((x+3,y+9,x+4,y+9),fill=RAMPS['black'][0])
                        draw.point((x+2,y+8),fill=RAMPS['gold'][4])
                else:
                    ramp_fill(output,(x,y,w,4),"gold", -1 if face in (2,3) else 0)
                    line(draw,[(x,y+7),(x+w-1,y+7)],"leather",2)
                    line(draw,[(x,y+9),(x+w-1,y+9)],"gold",3)
                    draw.point((x+1,y+5),fill=RAMPS['black'][4])
    return output


def lucifer(layer):
    atlas=Image.open(ART.parent / "models/out/lucifer/atlas.png").convert("RGBA")
    output=Image.new("RGBA",(64,32),atlas.getpixel((68,26)))
    for part,faces in FACES.items():
        for face,(x,y,w,h) in enumerate(faces):
            output.paste(projected_face(part,w,h,face),(x,y))
    # The actor's feather tips and the player elytra have separate gold palettes.
    # Transfer the four trim shades in shadow-to-highlight order.
    actor_gold = [(115, 81, 28), (124, 94, 45), (160, 128, 71), (181, 152, 90)]
    source = np.asarray(output)
    matched = source.copy()
    for rgb, elytra_color in zip(actor_gold, RAMPS["ancient_gold"]):
        matched[(source == (*rgb, 255)).all(axis=2)] = elytra_color
    return Image.fromarray(matched)


def wings(character):
    output=Image.new("RGBA",(64,32))
    material={"lucifer":"feather", "beelzebub":"fly", "belial":"silk", "mammon":"black"}[character]
    ramp_fill(output,(22,0,24,22),material)
    draw=ImageDraw.Draw(output)
    # Wing front resides on the large, tapered island at x31..45.
    for y in range(22):
        for x in range(31,46):
            level=max(0,min(4,3-(x-35)//4-(y//10)))
            output.putpixel((x,y),RAMPS[material][level])
    if character == "lucifer":
        for start in (32,35,38,41):
            line(draw,[(start,1),(start+2,8),(start+3,17),(start+3,21)],"feather",0)
            line(draw,[(start+1,2),(start+3,8),(start+4,17)],"feather",4)
        for y in range(16,22):
            for x in range(35,46):
                if y >= 17+(x%3): output.putpixel((x,y),RAMPS['ancient_gold'][min(4,1+(x+y)%4)])
        line(draw,[(35,3),(36,6),(36,9)],"snake",1)
        for yy in range(3,8): draw.point((35 if yy<5 else 36,yy),fill=RAMPS["snake"][yy-3])
        draw.point((44,21),fill=RAMPS["ancient_gold"][0])
    elif character == "beelzebub":
        for end in (37,41,45):
            line(draw,[(35,3),(end,10),(45,21)],"shell",1)
            line(draw,[(36,3),(end+1,10),(45,20)],"fly",4)
        for yy in (7,12,17): line(draw,[(36,yy),(44,yy+2)],"fly",1)
        draw.point((35,3),fill=RAMPS['vein'][3])
    elif character == "belial":
        line(draw,[(35,2),(43,7),(45,14),(45,21)],"bronze",3)
        for yy in (8,14,20):
            line(draw,[(35,3),(39,yy-1),(45,yy)],"bronze",2)
            draw.point((40,yy-1),fill=RAMPS['bronze'][4])
        line(draw,[(39,9),(40,12),(41,14)],"silk",4)
    else:
        line(draw,[(35,2),(43,7),(45,14),(45,21)],"gold",3)
        line(draw,[(35,3),(38,12),(41,20)],"leather",2)
        line(draw,[(35,3),(41,10),(45,14)],"gold",1)
        for x,y in ((40,19),(44,19),(44,14)):
            draw.rectangle((x,y,x+1,y+1),fill=RAMPS['gold'][2])
            draw.point((x,y),fill=RAMPS['gold'][4])
    line(draw,[(22,11),(22,21)],"ancient_gold" if character=="lucifer" else {"beelzebub":"shell","belial":"bronze","mammon":"gold"}[character],2)
    return output


def main():
    records=[]
    for character in ("lucifer","beelzebub","belial","mammon"):
        for layer in MASK_FILES:
            image = wings(character) if layer=="wings" else lucifer(layer) if character=="lucifer" else humanoid(character,layer)
            template=Image.open(ART/"refs"/MASK_FILES[layer]).convert("RGBA")
            mask=template.getchannel("A").point(lambda a:255 if a else 0)
            image.putalpha(mask)
            # Transparent RGB also clears so downstream tools see empty pixels.
            pixels=np.asarray(image).copy();pixels[pixels[:,:,3]==0]=0
            image=Image.fromarray(pixels)
            assert image.size==(64,32)
            assert set(image.getchannel("A").tobytes()) <= {0,255}
            assert image.getchannel("A").tobytes()==mask.tobytes()
            filename=f"{character}_{layer}.png"
            image.save(HERE/filename)
            records.append((filename,len({tuple(p) for p in np.asarray(image).reshape(-1,4)}-{(0,0,0,0)}),sum(a>0 for a in mask.tobytes())))
    print("Built 12 equipment textures")
    for record in records: print(*record)

if __name__=="__main__": main()
