tag @s add rpg.rite.anchor
scoreboard players operation @s rpg_rite_id = @e[type=minecraft:vindicator,tag=rpg.rite.subject,limit=1] rpg_rite_id
scoreboard players set @s rpg_dm_lord 6
scoreboard players set @s rpg_ex_stage 2
scoreboard players set @s rpg_ex_time 0
scoreboard players set @s rpg_totem 2400
particle flash{color:16777200} ~ ~0.8 ~ 0 0 0 0 1 force
particle end_rod ~ ~0.7 ~ 0.7 0.5 0.7 0.06 45 normal
scoreboard players set @s rpg_ex_stab 50
execute store result score @s rpg_ex_counter run random value 140..220
scoreboard players set @s rpg_ex_kind 0
scoreboard players set @s rpg_ex_ctime 0
scoreboard players set @s rpg_ex_ransom 0
scoreboard players set @s rpg_ex_slots 1
scoreboard players set @s rpg_ex_toolcd 0
execute if entity @a[distance=..10,gamemode=!spectator,scores={rpg_ex_lvl=5..}] run scoreboard players set @s rpg_ex_slots 2
scoreboard players set @s rpg_ex_phase 40
scoreboard players set @s rpg_ex_pressure 0
scoreboard players set @s rpg_ex_wave 0
scoreboard players set @s rpg_ex_wave_kind 0
execute store result score @s rpg_ex_struggle run random value 120..180
