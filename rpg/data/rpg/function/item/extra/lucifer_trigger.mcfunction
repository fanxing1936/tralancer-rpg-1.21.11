# 路西法［原罪］—— 由 rpg:advancement/item/lucifer 在蓄力长枪时触发。
# using_item 在蓄力期间每刻都会响，所以这里压一道 30 刻的冷却，
# 否则按住右键会把经验一路抽干。
advancement revoke @s only rpg:item/lucifer
execute if entity @s[scores={rpg_luci_use=1..}] run return 0
execute if entity @s[level=..1] run playsound minecraft:entity.villager.no player @s
execute if entity @s[level=2..] run function rpg:item/extra/lucifer_cast
