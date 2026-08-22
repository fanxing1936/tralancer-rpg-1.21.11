# 熔火之锤［熔流］—— 由 rpg:advancement/item/forge 在右键使用时触发。
advancement revoke @s only rpg:item/forge
execute if entity @s[level=..1] run playsound minecraft:entity.villager.no player @s
execute if entity @s[level=2..] run function rpg:item/epic/forge_cast
