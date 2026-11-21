scoreboard players operation #t rpg_fg = #d rpg_fg
scoreboard players operation #t rpg_fg *= #25 rpg_fg
scoreboard players operation @a[tag=rpg.fg.atk,limit=1] rpg_fg_blh += #t rpg_fg
execute as @a[tag=rpg.fg.atk,scores={rpg_fg_blh=400..}] run function rpg:forge/stone/blood_heal
