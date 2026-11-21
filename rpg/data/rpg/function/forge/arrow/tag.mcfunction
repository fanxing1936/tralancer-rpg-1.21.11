tag @s add rpg.fg.a
scoreboard players operation @s rpg_fg_eo = #me rpg_fg
execute store result score #ad rpg_fg run data get entity @s damage 100
scoreboard players operation #ad rpg_fg *= #fac rpg_fg
scoreboard players operation #ad rpg_fg /= #100 rpg_fg
execute store result entity @s damage double 0.01 run scoreboard players get #ad rpg_fg
execute if data entity @s {crit:1b} as @a if score @s rpg_fg_id = #me rpg_fg run scoreboard players set @s rpg_fg_crit 1
execute if score #met rpg_fg matches 1 run tag @s add rpg.fg.meteor
