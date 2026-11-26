scoreboard players add @s rpg_dt_mel 1
scoreboard players set @s rpg_dt_melt 70
execute store result score #s rpg_dt run data get entity @a[tag=rpg.dt.me,limit=1] SelectedItemSlot
execute if score #s rpg_dt = @s rpg_dt_slot run scoreboard players add @s rpg_dt_same 1
execute unless score #s rpg_dt = @s rpg_dt_slot run function rpg:daath_fight/mind/fresh
scoreboard players operation @s rpg_dt_slot = #s rpg_dt
execute if score @s rpg_dt_same matches 22.. if entity @s[tag=!rpg.dt.loop] run function rpg:daath_fight/mind/loop
