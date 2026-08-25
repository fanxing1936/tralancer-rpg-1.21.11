function rpg:inquest/tool/place/lantern
clear @a[tag=rpg.rite.user,distance=..6,limit=1] minecraft:paper[minecraft:custom_data~{rpg_lantern:1b}] 1
tag @a[tag=rpg.rite.user,distance=..6] add rpg.rite.chooser
tag @a[tag=rpg.rite.user,distance=..6] remove rpg.rite.user
function rpg:inquest/outcome/seal
