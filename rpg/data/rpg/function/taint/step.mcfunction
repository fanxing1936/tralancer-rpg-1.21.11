# 一次结算。魔器加、圣器减，两者都握着时互相抵消。
scoreboard players set @s rpg_taint_t 0

# 圣痕期间沾不上任何东西 —— 反转过的人，脏不了。
execute if entity @s[scores={rpg_holy=1..}] run return 0

execute if entity @s[tag=rpg.h.devil_tag1] run scoreboard players add @s rpg_taint 2
execute if entity @s[tag=rpg.h.devil_weapon_tag1] run scoreboard players add @s rpg_taint 1
# 立约本身就是代价 —— 柱中的东西一直在往里渗。贪婪那一柱渗得更快。
execute if entity @s[tag=rpg.pact] run scoreboard players add @s rpg_taint 1
execute if entity @s[tag=rpg.pact,scores={rpg_pact=7}] run scoreboard players add @s rpg_taint 1
execute if entity @s[tag=rpg.h.holy_weapon_tag1] run scoreboard players remove @s rpg_taint 1
execute if entity @s[scores={rpg_taint=101..}] run scoreboard players set @s rpg_taint 100
execute if entity @s[scores={rpg_taint=..-1}] run scoreboard players set @s rpg_taint 0

# 分档外显。低档只是身上泛起暗纹，越深越明显。
execute if entity @s[scores={rpg_taint=31..60}] at @s run particle dust{color:[0.32,0.16,0.42],scale:1} ~ ~1 ~ 0.35 0.6 0.35 0.01 4
execute if entity @s[scores={rpg_taint=61..90}] at @s run particle dust{color:[0.45,0.10,0.14],scale:2} ~ ~1 ~ 0.4 0.7 0.4 0.02 8
execute if entity @s[scores={rpg_taint=61..90}] at @s run particle sculk_soul ~ ~1.2 ~ 0.3 0.5 0.3 0.01 2

# 濒临魔化：力量上来了，但圣性之物开始灼手。
execute if entity @s[scores={rpg_taint=91..}] run effect give @s minecraft:strength 3 0 true
execute if entity @s[scores={rpg_taint=91..}] at @s run particle soul_fire_flame ~ ~1 ~ 0.4 0.7 0.4 0.01 6
execute if entity @s[scores={rpg_taint=91..},tag=rpg.h.holy_weapon_tag1] run damage @s 2 minecraft:magic
execute if entity @s[scores={rpg_taint=91..},tag=rpg.h.holy_weapon_tag1] run playsound minecraft:block.lava.extinguish player @s ~ ~ ~ 1 1.6

# 满值只报一次 —— 否则每两秒弹一遍标题，没人受得了。
execute if entity @s[scores={rpg_taint=100},tag=!rpg.taint.full] run function rpg:taint/full
execute if entity @s[scores={rpg_taint=..99},tag=rpg.taint.full] run tag @s remove rpg.taint.full
