# 别西卜 · 余烬：三段刀罡在同刻展开，不留下会串主人的命名盔甲架。
scoreboard players set @s rpg_ashes_chg 31
tag @a[tag=rpg.ashes.source] remove rpg.ashes.source
tag @s add rpg.ashes.source
execute at @s positioned ^ ^1 ^2 run function rpg:item/legacy/ashes_wave
execute at @s positioned ^-1 ^1 ^4 run function rpg:item/legacy/ashes_wave
execute at @s positioned ^1 ^1 ^6 run function rpg:item/legacy/ashes_wave
tag @s remove rpg.ashes.source
playsound minecraft:item.mace.smash_air player @a[distance=..24] ~ ~ ~ 1 0.55
playsound minecraft:block.fire.extinguish player @a[distance=..20] ~ ~ ~ 0.8 0.8
function rpg:hud/m4
