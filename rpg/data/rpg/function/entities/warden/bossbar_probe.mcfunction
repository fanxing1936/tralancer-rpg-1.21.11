execute on vehicle run return 0
execute if score @s rpg_boss_slot matches 1 run scoreboard players set #boss_slot1 rpg_boss_slot 0
execute if score @s rpg_boss_slot matches 1 run bossbar set minecraft:devil players @a[tag=rpg.bossbar.none]
execute if score @s rpg_boss_slot matches 2 run scoreboard players set #boss_slot2 rpg_boss_slot 0
execute if score @s rpg_boss_slot matches 2 run bossbar set minecraft:devil2 players @a[tag=rpg.bossbar.none]
execute if score @s rpg_boss_slot matches 3 run scoreboard players set #boss_slot3 rpg_boss_slot 0
execute if score @s rpg_boss_slot matches 3 run bossbar set minecraft:devil3 players @a[tag=rpg.bossbar.none]
execute if score @s rpg_boss_slot matches 4 run scoreboard players set #boss_slot4 rpg_boss_slot 0
execute if score @s rpg_boss_slot matches 4 run bossbar set minecraft:devil4 players @a[tag=rpg.bossbar.none]
kill @s
