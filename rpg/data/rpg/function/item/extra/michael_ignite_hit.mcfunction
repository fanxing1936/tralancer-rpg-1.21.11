# 圣焰炸开。恶魔额外受创并显形；骨中之骨引燃的，对路西法加倍 ——
# 第一次神陨之战的败者，认得这团火。
tag @s remove rpg.mi.fuse
execute if entity @s[tag=rpg.demon] run tag @s add rpg.mi.foe
execute if entity @s[tag=rpg.demon.minion] run tag @s add rpg.mi.foe
execute if entity @s[tag=rpg.mi.pairfuse,tag=rpg.advent,scores={rpg_dm_lord=1}] run tag @s add rpg.mi.morningstar
execute if entity @s[tag=!rpg.mi.foe] run damage @s 6 minecraft:magic
execute if entity @s[tag=rpg.mi.foe,tag=!rpg.mi.morningstar] run damage @s 10 minecraft:magic
execute if entity @s[tag=rpg.mi.morningstar] run damage @s 20 minecraft:magic
data modify entity @s Fire set value 60s
execute if entity @s[tag=rpg.mi.foe] run effect give @s minecraft:glowing 5 0 true
particle flash{color:16724736} ~ ~1.1 ~ 0 0 0 0 1
particle dust_color_transition{from_color:[1.0,0.2,0.0],to_color:[0.3,0.06,0.0],scale:1.6} ~ ~1 ~ 0.4 0.5 0.4 0.05 20
playsound minecraft:entity.blaze.hurt player @a[distance=..16] ~ ~ ~ 0.8 0.6
execute if entity @s[tag=rpg.mi.morningstar] run playsound minecraft:item.trident.thunder player @a[distance=..24] ~ ~ ~ 0.6 1.4
tag @s remove rpg.mi.foe
tag @s remove rpg.mi.pairfuse
tag @s remove rpg.mi.morningstar
