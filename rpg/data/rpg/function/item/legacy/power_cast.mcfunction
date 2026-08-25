# 朗基努斯 · 王座：只审判最近六秒内被这类圣枪刻过印的目标。
scoreboard players set @s rpg_throne_chg 31
tag @a[tag=rpg.throne.source] remove rpg.throne.source
tag @s add rpg.throne.source
scoreboard players operation #caster rpg_throne_owner = @s rpg_legacy_uid
execute as @e[tag=rpg.throne.mark,distance=..14] if score @s rpg_throne_owner = #caster rpg_throne_owner at @s run function rpg:item/legacy/power_target
particle minecraft:flash{color:16724787} ~ ~1 ~ 0 0 0 0 1
particle minecraft:dust_color_transition{from_color:[0.17,0.17,0.17],to_color:[1.0,0.2,0.0],scale:2} ~ ~1 ~ 1.8 1 1.8 0.05 65 force
playsound minecraft:item.trident.thunder player @a[distance=..28] ~ ~ ~ 0.8 0.8
tag @s remove rpg.throne.source
function rpg:hud/m11
