loot give @s loot rpg:world/currency
loot give @s loot rpg:world/currency
loot give @s loot rpg:world/currency
loot give @s loot rpg:elite/badge
scoreboard players add @s rpg_ex_xp 10
scoreboard players add @s rpg_bt_total 1
playsound minecraft:entity.player.levelup player @s ~ ~ ~ 0.6 1.4
tellraw @s ["",{"text":"[悬赏]","color":"#D4AF37","bold":true,"italic":false},{"text":"　悬赏完成：货币 ×3、精英徽记 ×1、阅历 +10","color":"gray","bold":false,"italic":false}]
execute if score @s rpg_bt_c1 matches 1 if score @s rpg_bt_c2 matches 1 if score @s rpg_bt_c3 matches 1 unless entity @s[tag=rpg.bt.all] run function rpg:events/bt/all
execute if score @s rpg_bt_total matches 21.. unless entity @s[tag=rpg.wl.malkuth] run function rpg:events/bt/malkuth
execute if predicate {condition:"minecraft:random_chance",chance:0.1} run loot give @s loot rpg:potion/blank_rite
