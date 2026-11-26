execute store result score #x rpg_dt run data get entity @a[tag=rpg.dt.me,limit=1] Pos[0] 4
execute store result score #z rpg_dt run data get entity @a[tag=rpg.dt.me,limit=1] Pos[2] 4
execute if score #x rpg_dt = @s rpg_dt_px if score #z rpg_dt = @s rpg_dt_pz run scoreboard players add @s rpg_dt_still 10
execute unless score #x rpg_dt = @s rpg_dt_px run scoreboard players set @s rpg_dt_still 0
execute unless score #z rpg_dt = @s rpg_dt_pz run scoreboard players set @s rpg_dt_still 0
scoreboard players operation @s rpg_dt_px = #x rpg_dt
scoreboard players operation @s rpg_dt_pz = #z rpg_dt
