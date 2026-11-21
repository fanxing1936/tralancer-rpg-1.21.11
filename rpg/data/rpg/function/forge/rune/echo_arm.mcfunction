scoreboard players set @a[tag=rpg.fg.atk,limit=1] rpg_fg_hit 0
scoreboard players operation @s rpg_fg_ea = #d rpg_fg
scoreboard players operation @s rpg_fg_ea *= #60 rpg_fg
scoreboard players operation @s rpg_fg_ea /= #100 rpg_fg
execute if score @s rpg_fg_ea matches ..0 run scoreboard players set @s rpg_fg_ea 1
scoreboard players operation @s rpg_fg_eo = @a[tag=rpg.fg.atk,limit=1] rpg_fg_id
scoreboard players set @s rpg_fg_ec 10
