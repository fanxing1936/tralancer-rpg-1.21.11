scoreboard players operation #d rpg_fg = @s damage_timing
scoreboard players operation #d rpg_fg -= @s damage_action
execute if score #d rpg_fg matches ..0 run return 0
execute if entity @s[type=minecraft:player] run function rpg:forge/hit/hurt_player
tag @s add rpg.fg.v
execute on attacker if entity @s[type=minecraft:player] run tag @s add rpg.fg.atk
execute if entity @a[tag=rpg.fg.atk,limit=1] run function rpg:forge/hit/apply
tag @a[tag=rpg.fg.atk] remove rpg.fg.atk
tag @s remove rpg.fg.v
