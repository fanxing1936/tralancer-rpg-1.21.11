scoreboard players add #boss_slot1 rpg_boss_slot 0
scoreboard players add #boss_slot2 rpg_boss_slot 0
scoreboard players add #boss_slot3 rpg_boss_slot 0
scoreboard players add #boss_slot4 rpg_boss_slot 0
execute as @e[type=minecraft:evoker,tag=boss] at @s run function rpg:entities/warden/bossbar_entity
execute as @e[type=minecraft:vindicator,tag=devil2,tag=boss] at @s run function rpg:entities/warden/bossbar_entity
