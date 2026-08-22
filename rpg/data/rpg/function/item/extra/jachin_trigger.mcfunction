# 雅斤［立柱］—— 由 rpg:advancement/item/jachin 在右键使用时触发
advancement revoke @s only rpg:item/jachin
execute if entity @s[level=..0] run playsound minecraft:entity.villager.no player @s
execute if entity @s[level=1..] run function rpg:item/extra/jachin_cast
