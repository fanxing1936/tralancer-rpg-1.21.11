
scoreboard players add #boss_ui rpg_boss_slot 1
execute if score #boss_ui rpg_boss_slot matches 2.. run function rpg:entities/warden/bossbar_tick
execute if score #boss_ui rpg_boss_slot matches 2.. run scoreboard players set #boss_ui rpg_boss_slot 0
