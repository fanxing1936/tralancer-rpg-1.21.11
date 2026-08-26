execute if entity @s[tag=rpg.demon.minion.casting,scores={rpg_mn_cast=1..}] run scoreboard players remove @s rpg_mn_cast 10
execute if entity @s[tag=rpg.demon.minion.casting,scores={rpg_mn_cast=..0}] run return run function rpg:minion/resolve_dispatch
execute if entity @s[tag=rpg.demon.minion.casting] run return 0
execute if entity @s[scores={rpg_mn_role=4}] run function rpg:minion/role/hexer_move
execute if entity @s[scores={rpg_mn_cd=1..}] run scoreboard players remove @s rpg_mn_cd 10
execute if entity @s[scores={rpg_mn_role=3}] unless entity @a[distance=..14,gamemode=!spectator,gamemode=!creative,limit=1] run return 0
execute unless entity @s[scores={rpg_mn_role=3}] unless entity @a[distance=..12,gamemode=!spectator,gamemode=!creative,limit=1] run return 0
execute if score #casts rpg_mn_tick matches ..1 if entity @s[scores={rpg_mn_cd=..0}] run function rpg:minion/ability_dispatch
