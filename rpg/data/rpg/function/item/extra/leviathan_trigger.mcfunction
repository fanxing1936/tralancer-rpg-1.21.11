# 利维坦［沉锚］—— 由 rpg:advancement/item/leviathan 在右键使用时触发
advancement revoke @s only rpg:item/leviathan
execute if entity @s[level=..1] run playsound minecraft:entity.villager.no player @s
execute if entity @s[level=2..] run function rpg:item/extra/leviathan_cast
