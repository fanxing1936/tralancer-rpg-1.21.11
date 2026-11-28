# 站岗的圣卫每刻（as/at 它）
execute if entity @s[tag=rpg.tw.guard] if entity @a[tag=rpg.dm.wanted,distance=..16,gamemode=!spectator] run tag @s add rpg.tw.fight
execute if entity @s[tag=rpg.lm.awake] run tag @s add rpg.tw.fight
execute if entity @s[tag=rpg.tw.guard,tag=rpg.tw.fight] unless score @s rpg_tg_st matches 1.. unless entity @a[tag=rpg.dm.wanted,distance=..24] run function rpg:town/life/guard_calm
execute if entity @s[tag=!rpg.tw.fight,nbt={NoAI:0b}] run data merge entity @s {NoAI:1b}
