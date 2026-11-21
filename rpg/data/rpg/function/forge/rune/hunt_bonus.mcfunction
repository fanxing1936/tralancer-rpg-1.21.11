scoreboard players operation #t rpg_fg = @s rpg_fg_mark
execute as @a[tag=rpg.fg.atk] if score @s rpg_fg_id = #t rpg_fg run scoreboard players add #pct rpg_fg 25
